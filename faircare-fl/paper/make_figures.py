import argparse
import json
import os
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    hist_path = os.path.join(args.indir, 'history.json')
    if not os.path.exists(hist_path):
        return
    history = json.load(open(hist_path))
    rounds = [h['round'] for h in history]
    acc = [h['acc'] for h in history]
    dp = [h['dp'] for h in history]
    eo = [h['eo'] for h in history]
    plt.figure(); plt.plot(rounds, acc); plt.xlabel('round'); plt.ylabel('accuracy'); plt.savefig(os.path.join(args.outdir,'acc.png'))
    plt.figure(); plt.plot(rounds, dp, label='DP'); plt.plot(rounds, eo, label='EO'); plt.legend(); plt.savefig(os.path.join(args.outdir,'fairness.png'))

if __name__ == '__main__':
    main()
