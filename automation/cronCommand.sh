#
# Put this in crontab

SHELL=/bin/bash
BASH_ENV=~/.bashrc_conda

*/5 * * * * conda actvate flywheel; bash -x /home/will/Projects/recover-project/automation/run.>
