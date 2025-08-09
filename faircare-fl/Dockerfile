FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "faircare.experiments.run_experiments", "--dataset", "heart", "--algo", "faircare", "--num_clients", "2", "--rounds", "1", "--local_epochs", "1", "--batch_size", "16", "--lr", "1e-3", "--dirichlet_alpha", "0.5", "--sensitive_attr", "sex", "--outdir", "runs/docker_demo/"]
