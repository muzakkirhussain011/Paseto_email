import os

def get_mimic_path():
    return os.environ.get('MIMIC_LOCAL_DIR', '')

def get_eicu_path():
    return os.environ.get('EICU_LOCAL_DIR', '')
