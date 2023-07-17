import flywheel
import sys
import os
import logging
import json
from datetime import datetime, timedelta, timezone

# Date stuff
date = datetime.now(timezone.utc) - timedelta(hours=24)
date_str = datetime.strftime(datetime.now(), '%m-%d-%Y_%H:%M:%S')

# Flywheel
fw = flywheel.Client()
project = fw.lookup("detre_group/RECOVER")
sessions = [s for s in project.sessions() if s.created > date]
gear = fw.lookup('gears/bids-fmriprep/1.2.4_20.2.6')
license_file = project.get_file('license.txt')

# Exit if there are no recent sessions
if len(sessions) == 0:
    print("No recent sessions...")
    exit()

#sleep(900) # sleep for 15 minutes (about how long it takes for fw-heudiconv to queue and run)
# Load in data
config_file = "/home/will/Projects/recover-project/automation/fmriprep_config.json"
with open(config_file) as f:
    config = json.load(f)

for session in sessions:
    session = session.reload()

    ##### RUN FMRIPREP ######
    # check if fmriprep has already been run
    for analysis in session.analyses:
        states = [ "complete", "running", "failed"]
        if "fmriprep" in analysis.label and any(analysis.job['state'] == s for s in states):
            print("Already run or running")
            print(analysis.job['state'])
            exit()

    # Logging stuff
    print(f"Starting up for session {session.label}...")
    print("====fmriprep====")
    print(date_str)
    # check if session has been bidsified successfully
    for analysis in session.analyses:
        if 'heudiconv' in analysis.label and analysis.job['state']=='complete':
            # set inputs and config for gear
            inputs = {'freesurfer_license': license_file}

            print(inputs)
            print(config)

            label=f"fmriprep_1.2.4_20.2.6_{date_str}_autolaunch"
            try:
                analysis_id = gear.run(analysis_label=label, config=config, inputs=inputs, destination=session)
                print(f"Launching fmriprep analysis with label {label}...")
            except Exception as e:
                print(e)
                logger.warning(e)
