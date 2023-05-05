import flywheel
import sys
import os
import logging

from datetime import datetime, timedelta, timezone

#os.system("touch /home/will/Projects/motor-imagery/automation/logs/test.txt")
# Date stuff
date = datetime.now(timezone.utc) - timedelta(hours=1)
#date = datetime.today() - timedelta(hours=24)
#date_str = "{:4d}-{:02d}-{:02d}".format(date.year,date.month,date.day)
#date_str = datetime.strftime(date, '%Y-%m-%d')
date_str = datetime.strftime(datetime.now(), '%m-%d-%Y_%H:%M:%S')

# Flywheel
fw = flywheel.Client()
project = fw.lookup("detre_group/RECOVER")
print(project.label)
sessions = [s for s in project.sessions() if s.created > date]
#(sessions)
gear = fw.lookup('gears/fw-heudiconv/0.2.15_0.4.3')
heuristic = project.get_file('motor_heuristic4.py')

# Exit if there are no recent sessions
if len(sessions) == 0:
    print("No recent sessions...")
    exit()

sleep(1500) # buffer time for dicom classification

for session in sessions:
    session = session.reload()
    print(session.label)
    # check if heudiconv has already been run
    for analysis in session.analyses:
        states = [ "complete", "running", "failed"]
        if "heudiconv" in analysis.label and any(analysis.job['state'] == s for s in states):
            print("Already run or running")
            print(analysis.job['state'])
            exit()

    # Logging stuff
    print("Starting up...")
    print("====fw-heudiconv====")
    print(date_str)

    print(f"Running on {session.label}...")

    ##### RUN HEUDICONV #######
    # set inputs and config for gear
    inputs = {'heuristic': heuristic}
    config = {'action': 'Curate','dry_run': False}

    print(inputs)
    print(config)

    label=f"heudiconv-0.2.15_0.4.3_{date_str}_autolaunch"

    try:
        analysis_id = gear.run(analysis_label=label, config=config, inputs=inputs, destination=session)
        print(f"Launching fw-heudiconv analysis with label {label}...")
    except Exception as e:
        print(e)
        print(e)
