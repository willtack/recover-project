#!/home/will/anaconda3/bin/python
import flywheel
import sys
import os
import json
from datetime import datetime, timedelta, timezone
# Date stuff
date = datetime.now(timezone.utc) - timedelta(hours=12)
date_str = datetime.strftime(datetime.now(), '%m-%d-%Y_%H:%M:%S')

# Flywheel
fw = flywheel.Client()
project = fw.lookup("detre_group/RECOVER")
sessions = [s for s in project.sessions() if s.created > date]
version='0.1.10'
gear = fw.lookup(f'gears/motorfmri/{version}')

# Exit if there are no recent sessions
if len(sessions) == 0:
    print("No recent sessions...")
    exit()

#print("Sleeping for 15 minutes to allow fw-heudiconv to finish...")
#sleep(900) # sleep for 15 minutes (about how long it takes for fw-heudiconv to queue and run)

for session in sessions:
    session = session.reload()

    ##### RUN TASK ANALYSIS ######
    # check if motorfmri has already been run
    for analysis in session.analyses:
        states = [ "complete", "running", "failed"]
        if "motorfmri" in analysis.label and any(analysis.job['state'] == s for s in states):
            print("Already run or running")
            print(analysis.job['state'])
            exit()

    # Logging stuff
    print(f"Starting up for session {session.label}")
    print("====task-fmri====")
    print(date_str)

    # check if session has been preprocessed successfully
    for analysis in session.analyses:
        if 'fmriprep' in analysis.label and analysis.job['state']=='complete' and analysis.files:
            print("Preprocessed successfully, starting analysis...")
            for file in analysis.files:
                if "bids-fmriprep" in file.name and "zip" in file.name:
                    fmriprepzip = file

            # set inputs and config for gear
            inputs = {"fmriprepdir": fmriprepzip}
            config = {"AROMA": False, "alpha":0.20, "cluster_size_thresh":150, "fwhm":6}
            print(inputs)
            print(config)

            label=f"motorfmri_{version}_{date_str}_autolaunch"

            try:
                analysis_id = gear.run(analysis_label=label, config=config, inputs=inputs, destination=session)
                print(f"Launching fmriprep analysis with label {label}...")
            except Exception as e:
                print(e)
        else:
            print("Preprocessing not complete.")
