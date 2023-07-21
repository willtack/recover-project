# recover-project

Code related to fMRI processing for the RECOVER project, especially the automation of the processing pipeline on Flywheel, located under `automation/`


## How to run the RECOVER pipeline 

1) `git clone` this repository
2) install the Flywheel SDK in your anaconda environment: [instructions here](https://flywheel-io.gitlab.io/product/backend/sdk/branches/master/python/getting_started.html)
3) edit `{workDir}` in `run.sh` (in the automation folder) to your local path and other paths in the python scripts
4) create a "logs" folder under the "automation" folder
5) edit your [crontab](https://www.geeksforgeeks.org/crontab-in-linux-with-examples/) with the lines of code in `cronCommand.sh`
6) change instances of "detre_group/RECOVER to "detre_group/Alice Project"
7) upload the data (will trigger scripts)
