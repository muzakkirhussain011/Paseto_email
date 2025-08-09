from .metrics import dp_gap, eo_gap


def summarize(history):
    lines = ["round,acc,dp,eo"]
    for h in history:
        lines.append(f"{h['round']},{h['acc']},{h['dp']},{h['eo']}")
    return "\n".join(lines)
