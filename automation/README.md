`cronCommand.sh` contains lines of code that should be included in the local crontab of whatever computer you want to run the pipeline. If you don't know, a crontab is a list of user-inputted commands that the computers runs on a regular basis. */5 * * * * means the command will run every five minutes. 
(Here is more [info](https://www.geeksforgeeks.org/crontab-in-linux-with-examples/) on cron stuff).

This commands runs the run script, `run.sh`, which launches a python script for every step of the pipeline, BIDsification, preprocessing the BOLD (fMRIPrep), modelling the task activity (motorfmri) and processing the ASL (which is independent of the other three steps).

Each python script checks if there are any recent sessions and quits if not. It also checks if there are any recently run analyses of that kind (i.e. fmriprep won't run if it has been run on the session before). That includes failed sessions just in case a bug is causing the gear to fail. Otherwise it would run a doomed gear every five minutes until you realize what happened.
