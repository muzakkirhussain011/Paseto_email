import argparse
import json
import os
import csv
from tabulate import tabulate


def summarize_run(path):
    hist = json.load(open(os.path.join(path,'history.json')))
    last = hist[-1]
    return last['acc'], last['dp'], last['eo']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    index = os.path.join(args.indir, 'index.csv')
    rows = []
    if os.path.exists(index):
        with open(index) as f:
            reader = csv.DictReader(f)
            for row in reader:
                acc, dp, eo = summarize_run(row['path'])
                rows.append([row['algo'], int(row['seed']), acc, dp, eo])
    else:
        acc, dp, eo = summarize_run(args.indir)
        rows.append(['single',0,acc,dp,eo])
    table = tabulate(rows, headers=['algo','seed','acc','dp','eo'])
    with open(os.path.join(args.outdir,'results_table.tex'),'w') as f:
        f.write(table)
    with open(os.path.join('paper','RESULTS.md'),'w') as f:
        f.write('```\n'+table+'\n```')

if __name__ == '__main__':
    main()
