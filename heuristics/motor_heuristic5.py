import os
from collections import defaultdict

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# structurals
t1w1 = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_run-01_T1w')
t1w2 = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_{session}_run-02_T1w')

# task fMRI
motor1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-motor_run-01_bold')
motor2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-motor_run-02_bold')
motor3 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-motor_run-03_bold')
motor4 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-motor_run-04_bold')
motor5 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-motor_run-05_bold')
lang1 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-lang_run-01_bold')
lang2 = create_key(
    'sub-{subject}/ses-{session}/func/sub-{subject}_{session}_task-lang_run-02_bold')


# fieldmaps
fmap_pa = create_key(
    'sub-{subject}/ses-{session}/fmap/sub-{subject}_{session}_dir-PA_epi')
fmap_ap = create_key(
    'sub-{subject}/ses-{session}/fmap/sub-{subject}_{session}_dir-AP_epi')


def infotodict(seqinfo):

    last_run = len(seqinfo)

    info = {t1w1:[], t1w2:[], motor1: [], motor2: [], motor3: [], motor4: [], motor5: [], lang1: [], lang2: [], fmap_pa: [], fmap_ap: []}

    def get_series(key, s):
            info[key].append(s.series_id)

    def get_both_series(key1, key2, s):
        if len(info[key1]) == 0:
            info[key1].append(s.series_id)
        else:
            info[key2].append(s.series_id)

    motor_scans = defaultdict(list)
    lang_scans = defaultdict(list)

    for s in seqinfo:
        protocol = s.protocol_name.lower()
        if "t1_mprage" in protocol:
            get_both_series(t1w1, t1w2, s)
        elif "moto" in protocol and "ph" not in s.dcm_dir_name:
            motor_scans[s.dcm_dir_name].append(s.series_id)
        elif "lang" in protocol and "ph" not in s.dcm_dir_name:
            lang_scans[s.dcm_dir_name].append(s.series_id)
        elif "fieldmap" in protocol:
            if "pa" in protocol:
                get_series(fmap_pa,s)
            elif "ap" in protocol:
                get_series(fmap_ap, s)

        motor_uids = sorted(motor_scans.keys())
        motor_keys = [motor1,motor2,motor3,motor4, motor5]
        for motor_uid, motor_key in zip(motor_uids, motor_keys):
            for series_id in motor_scans[motor_uid]:
                info[motor_key].append(series_id)

        lang_uids = sorted(lang_scans.keys())
        lang_keys = [lang1,lang2]
        for lang_uid, lang_key in zip(lang_uids, lang_keys):
            for series_id in lang_scans[lang_uid]:
                info[lang_key].append(series_id)

    return info


MetadataExtras = {
    fmap_ap: {
        "PhaseEncodingDirection": "j-",
        "TotalReadoutTime": 0.0177332
    },
    fmap_pa: {
        "PhaseEncodingDirection": "j",
        "TotalReadoutTime": 0.0177332
    }
}

IntendedFor = {
    fmap_ap: {
        '{session}/func/sub-{subject}_{session}_task-motor_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-motor_run-02_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-lang_bold.nii.gz',
    },
    fmap_pa: {
        '{session}/func/sub-{subject}_{session}_task-motor_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-motor_run-02_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-lang_bold.nii.gz',
    }
}


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
    motor_events = {
        'name': 'task-motor_events.tsv',
        'data': motor_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }
    lang_events = {
        'name': 'task-lang_events.tsv',
        'data': motor_df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }


    return [motor_events, lang_events]
