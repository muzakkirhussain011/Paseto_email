from .utils import get_device
from ..fairness.metrics import dp_gap, eo_gap, fpr_gap, ece, confusion_by_group
import torch
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score


def evaluate(model, data, sensitive_attr='s'):
    device = get_device()
    model.to(device)
    model.eval()
    ys, preds, probs, sens = [], [], [], []
    with torch.no_grad():
        for x, y, s in data:
            x, y = x.to(device), y.to(device)
            logit = model(x)
            prob = torch.sigmoid(logit).cpu().numpy()
            pred = (prob > 0.5).astype(int)
            ys.extend(y.cpu().numpy())
            preds.extend(pred)
            probs.extend(prob)
            sens.extend(s.numpy())
    acc = accuracy_score(ys, preds)
    try:
        auroc = roc_auc_score(ys, probs)
    except ValueError:
        auroc = 0.5
    f1 = f1_score(ys, preds, average='macro')
    conf = confusion_by_group(preds, ys, sens)
    dp = dp_gap(conf)
    eo = eo_gap(conf)
    fpr = fpr_gap(conf)
    cal = ece(probs, ys)
    return {'acc': acc, 'auroc': auroc, 'f1': f1, 'dp': dp, 'eo': eo, 'fpr': fpr, 'ece': cal, 'confusion': conf}
