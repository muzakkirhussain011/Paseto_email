#!/bin/bash
set -e
python -m faircare.experiments.run_sweep "$@"
python -m faircare.paper.tables --indir runs/sweep/ --outdir paper/tables/
