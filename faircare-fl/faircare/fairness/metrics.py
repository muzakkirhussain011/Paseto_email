import numpy as np


def confusion_by_group(preds, labels, sens):
    conf = {0: {'tp':0,'fp':0,'fn':0,'tn':0}, 1:{'tp':0,'fp':0,'fn':0,'tn':0}}
    for p,l,s in zip(preds, labels, sens):
        group = int(s)
        if p==1 and l==1: conf[group]['tp']+=1
        if p==1 and l==0: conf[group]['fp']+=1
        if p==0 and l==1: conf[group]['fn']+=1
        if p==0 and l==0: conf[group]['tn']+=1
    return conf


def rate(tp, fp, fn, tn):
    return tp+fp+fn+tn


def dp_gap(conf):
    p1 = (conf[1]['tp']+conf[1]['fp'])/max(1, rate(**conf[1]))
    p0 = (conf[0]['tp']+conf[0]['fp'])/max(1, rate(**conf[0]))
    return abs(p1-p0)


def eo_gap(conf):
    tpr1 = conf[1]['tp']/max(1, conf[1]['tp']+conf[1]['fn'])
    tpr0 = conf[0]['tp']/max(1, conf[0]['tp']+conf[0]['fn'])
    return abs(tpr1-tpr0)


def fpr_gap(conf):
    fpr1 = conf[1]['fp']/max(1, conf[1]['fp']+conf[1]['tn'])
    fpr0 = conf[0]['fp']/max(1, conf[0]['fp']+conf[0]['tn'])
    return abs(fpr1-fpr0)


def ece(probs, labels, bins=10):
    probs = np.array(probs)
    labels = np.array(labels)
    bins = np.linspace(0,1,bins+1)
    ece = 0.0
    for i in range(len(bins)-1):
        idx = (probs>=bins[i]) & (probs<bins[i+1])
        if idx.sum()==0: continue
        acc = labels[idx].mean()
        conf = probs[idx].mean()
        ece += abs(acc-conf)*idx.mean()
    return ece
