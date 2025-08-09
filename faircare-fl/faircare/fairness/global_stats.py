from collections import Counter


def aggregate_confusion(conf_list):
    agg = {0: Counter({'tp':0,'fp':0,'fn':0,'tn':0}), 1: Counter({'tp':0,'fp':0,'fn':0,'tn':0})}
    for conf in conf_list:
        for g in [0,1]:
            agg[g].update(conf[g])
    return {g: dict(agg[g]) for g in agg}
