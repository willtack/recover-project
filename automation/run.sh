#!/bin/bash
workDir=/home/will/Projects/recover-project/automation
current_date_time=$(date +%m-%d-%Y_%H:%M)
echo $(date) >> ${workDir}/logs/runs.log
# conda activate flywheel
python ${workDir}/launch_heudiconv.py > ${workDir}/logs/gears/${current_date_time}_heudiconv.log
python ${workDir}/launch_fmriprep.py > ${workDir}/logs/gears/${current_date_time}_fmriprep.log
python ${workDir}/launch_motorfmri.py > ${workDir}/logs/gears/${current_date_time}_motorfmri.log
python ${workDir}/launch_asl.py > ${workDir}/logs/gears/${current_date_time}_asl.log
