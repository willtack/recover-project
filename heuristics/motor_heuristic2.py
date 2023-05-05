import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# structurals
t1w = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_T1w')


# task fMRI
motor3mm = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-motor3mm_bold')
motor2mm = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-motor2mm_bold')
imotor3mm_run1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-imotor3mm_run-01_bold')
imotor3mm_run2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-imotor3mm_run-02_bold')
imotor2mm = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-imotor2mm_bold')


def infotodict(seqinfo):

    last_run = len(seqinfo)

    info = {t1w:[], motor3mm:[], motor2mm: [], imotor3mm_run1:[], imotor3mm_run2: [], imotor2mm: []}

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
        elif "motor" in s.series_description:
            if "2mmiso" in protocol and "imotor" not in protocol:
                get_series(motor2mm,s)
            elif "3mmiso" in protocol and "imotor" not in protocol:
                get_series(motor3mm,s)
            if "2mmiso" in protocol and "imotor" in protocol:
                get_series(imotor2mm,s)
            elif "3mmiso" in protocol and "imotor" in protocol:
                get_both_series(imotor3mm_run1, imotor3mm_run2,s)


    return info


def AttachToProject():
    import pandas as pd
    motor_data = {'onset': [0, 2.5, 20, 37.5, 55, 72.5, 90.0, 107.5, 125],
                   'duration': [2.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5, 17.5],
                   'weight': [0, 1, 0, 1, 0, 1, 0, 1, 0],
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
    motor3mm_events = {
        'name': 'task-motor3mm_events.tsv',
        'data': motor_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }
    motor2mm_events = {
        'name': 'task-motor2mm_events.tsv',
        'data': motor_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }
    imotor3mm_events = {
        'name': 'task-imotor3mm_events.tsv',
        'data': motor_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }
    imotor2mm_events = {
        'name': 'task-imotor2mm_events.tsv',
        'data': motor_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }

    return [motor3mm_events, motor2mm_events, imotor3mm_events, imotor2mm_events]
