import argparse
import os
import csv
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--algo', nargs='+', default=['faircare'])
    parser.add_argument('--seeds', nargs='+', type=int, default=[0,1])
    parser.add_argument('--outdir', default='runs/sweep/')
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    index_path = os.path.join(args.outdir, 'index.csv')
    with open(index_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['algo','seed','path'])
        for algo in args.algo:
            for seed in args.seeds:
                run_dir = os.path.join(args.outdir, f'{algo}_{seed}')
                cmd = [
                    'python','-m','faircare.experiments.run_experiments',
                    '--dataset','heart','--algo',algo,
                    '--num_clients','5','--rounds','2','--batch_size','32',
                    '--seed',str(seed),'--outdir',run_dir
                ]
                subprocess.run(cmd, check=True)
                writer.writerow([algo, seed, run_dir])

if __name__ == '__main__':
    main()
