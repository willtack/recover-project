import flywheel
import sys
import os
import json
from datetime import datetime, timedelta, timezone

# Date stuff
date = datetime.now(timezone.utc) - timedelta(hours=1)
date_str = datetime.strftime(datetime.now(), '%m-%d-%Y_%H:%M:%S')

# Flywheel
fw = flywheel.Client()
project = fw.lookup("detre_group/RECOVER")
sessions = [s for s in project.sessions() if s.created > date]
gear = fw.lookup('gears/asllite/0.2.5_0.3.0')
asl_context = project.get_file('aslcontext.tsv')
license_file = project.get_file('license.txt')

# Exit if there are no recent sessions
if len(sessions) == 0:
    print("No recent sessions...")
    exit()

# print("Sleeping for 3 minutes to allow fw-heudiconv to start...")
# sleep(180)

for session in sessions:
    session = session.reload()

    ##### RUN ASL PREPROCESSING ######
    # check if asl has already been run
    for analysis in session.analyses:
        states = [ "complete", "running", "failed"]
        if "asllite" in analysis.label and any(analysis.job['state'] == s for s in states):
            print("Already run or running")
            print(analysis.job['state'])
            exit()

    # Logging stuff
    print(f"Starting up for session {session.label}")
    print("====asl====")
    print(date_str)

    asl = None
    m0 = None
    for acq in session.acquisitions():
        if "LLASL" in acq.label and acq.label.endswith("_ASL"):
            for f in acq.files:
                if f.name.endswith("nii.gz"):
                    print(f.name)
                    asl = acq.get_file(f.name)

        elif "LLASL" in acq.label and acq.label.endswith("M0"):
            for f in acq.files:
                if f.name.endswith("nii.gz"):
                    print(f.name)
                    m0 = acq.get_file(f.name)

    # set inputs and config for gear
    inputs = {"asl": asl, "aslcontext": asl_context, "freesurfer_license": license_file, "m0": m0}
    config = {"LD": 3, "PLD": 2, "asl_fwhm": 3, "dir": True, "fwhm": 8, "labelefficiency": 0.72, "m0scale":10, "m0type": "Separate"}
    print(inputs)
    print(config)

    label=f"asllite_0.2.5_0.3.0_{date_str}_autolaunch"

    try:
        analysis_id = gear.run(analysis_label=label, config=config, inputs=inputs, destination=session)
        print(f"Launching asl analysis with label {label}...")
    except Exception as e:
        print(e)
