from faircare.fairness.metrics import confusion_by_group, dp_gap, eo_gap

def test_dp_eo():
    preds = [1,0,1,0]
    labels = [1,0,0,1]
    sens = [1,1,0,0]
    conf = confusion_by_group(preds, labels, sens)
    dp = dp_gap(conf)
    eo = eo_gap(conf)
    assert dp >= 0 and eo >= 0
