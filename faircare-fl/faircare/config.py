import yaml

DEF_CONFIG = {
    'lr': 1e-3,
    'batch_size': 32,
    'local_epochs': 1,
    'rounds': 1,
}

def load_config(path=None):
    cfg = DEF_CONFIG.copy()
    if path:
        with open(path) as f:
            cfg.update(yaml.safe_load(f))
    return cfg
