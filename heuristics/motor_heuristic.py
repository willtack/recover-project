import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# structurals
t1w = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_T1w')


# task fMRI
motor = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-motor_bold')

# Field maps
# b0_mag = create_key(
#    'sub-{subject}/ses-{session}/fmap/sub-{subject}_{session}_magnitude{item}')
# b0_phase = create_key(
#    'sub-{subject}/ses-{session}/fmap/sub-{subject}_{session}_phasediff')
# pe_rev = create_key(
#     'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-multishell_dir-j_epi')
# bold_tu = create_key(
#     'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_dir-j_epi')


def infotodict(seqinfo):

    last_run = len(seqinfo)

    info = {t1w:[], motor:[]}

# sometimes patients struggle with a task the first time around (or something
# else goes wrong and often some tasks are repeated. This function accomodates
# the variable number of task runs
    def get_both_series(key1, key2, s):
         if len(info[key1]) == 0:
             info[key1].append(s.series_id)
         else:
             info[key2].append(s.series_id)

# this doesn't need to be a function but using it anyway for aesthetic symmetry
# with above function
    def get_series(key, s):
            info[key].append(s.series_id)

    for s in seqinfo:
        protocol = s.protocol_name.lower()
        if "t1_mprage" in protocol:
            get_series(t1w,s)
        elif "motor" in protocol:
            get_series(motor,s)

    return info


def AttachToProject():
    import pandas as pd
    motor_data = {'onset': [0, 13.5, 31, 48.5, 66, 83.5, 101.0, 118.5, 136],
                   'duration': [13.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5, 6.5],
                   'weight': [1, 0, 1, 0, 1, 0, 1, 0, 0],
                   'trial_type':
                  ['baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline',
                   'stimulus',
                   'baseline']}

    motor_df = pd.DataFrame(motor_data, columns = ['onset', 'duration','trial_type'])
    motor1 = {
        'name': 'task-motor_events.tsv',
        'data': motor_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }

    return motor1


# IntendedFor = {
#     b0_phase: [
#     '{session}/func/sub-{subject}_{session}_task-object_run-01_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-object_run-02_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-rhyme_run-01_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-rhyme_run-02_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-scenemem_run-01_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-scenemem_run-02_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-sentence_run-01_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-sentence_run-02_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-wordgen_run-01_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-wordgen_run-02_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-binder_run-01_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-binder_run-02_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-verbgen_run-01_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-verbgen_run-02_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-rest_run-01_bold.nii.gz',
#     '{session}/func/sub-{subject}_{session}_task-rest_run-02_bold.nii.gz'],
# }
