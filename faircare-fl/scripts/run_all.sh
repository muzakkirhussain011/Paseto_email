#!/bin/bash
set -e
python -m faircare.experiments.run_experiments "$@"
python -m faircare.paper.make_figures --indir $(dirname "$@") --outdir paper/figs/
python -m faircare.paper.tables --indir $(dirname "$@") --outdir paper/tables/
