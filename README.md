# recover-project

Code related to fMRI processing for the RECOVER project, especially the automation of the processing pipeline on Flywheel, located under `automation/`


## How to run the RECOVER pipeline 

1) `git clone` this repository
2) install the Flywheel SDK in your anaconda environment: [instructions here](https://flywheel-io.gitlab.io/product/backend/sdk/branches/master/python/getting_started.html)
3) edit `{workDir}` in `run.sh` (in the automation folder) to your local path and other paths in the python scripts
4) create a "logs" folder under the "automation" folder
   - create a "runs" folder and "gears" folder underneath "logs"
6) edit your [crontab](https://www.geeksforgeeks.org/crontab-in-linux-with-examples/) with the lines of code in `cronCommand.sh`
7) change instances of "detre_group/RECOVER to "detre_group/Alice Project"
8) upload the data (will trigger scripts)
   - this is just for testing purposes. in practice, the data will be reaped directly from the scanner as the scan proceeds
   - to upload structured DICOM data (it comes this way when you download from Flywheel GUI, or you can structure it yourself), follow [these instructions](https://docs.flywheel.io/hc/en-us/articles/360034339933-How-to-Import-DICOM-files-Using-the-Flywheel-CLI#). by structured, I mean there is a folder for the group (i.e detre_group), project, subjects, sessions, and acquisitions, nested in that order. DICOMs need to be unzipped to upload this way).
  

The code in the crontab runs every 5 minutes. If no new data is detected, all the `launch_*` scripts exit before doing anything. The logs under gears/ will say ""No recent sessions...".  When new data _is_ uploaded to the Flywheel project, the scripts will launch, check if the gear has been run already (they will exit if it has to prevent any loops or repeated runs). If it hasn't been run it will run. Each subsequent step in the pipeline will also check if the step before has run. 

One common issue is simply if the session name has a space or other special character in it. The first step, bidsification, will fail as this is not BIDs compliant and as a result the rest of the pipeline will not run. If a step in the pipeline fails, it will not run again because of the check. The best solution right now would be to disable the check by commenting it out (e.g. [here]( https://github.com/willtack/recover-project/blob/77cd7f0bb095f330d466bd6ac2ff62be6071a892/automation/launch_motorfmri.py#L31C1-L36)).

Another common issue is if the data in a new session is not organized exactly the same way as previous sessions. They are still tinkering with the protocol so this is to be expected. In this case, you have to edit the heuristic file and update the reference in the code. Create a new file instead of writing over the previous. See this page about how to approach editing a BIDs heuristic file: https://fw-heudiconv.readthedocs.io/en/latest/heuristic.html.



