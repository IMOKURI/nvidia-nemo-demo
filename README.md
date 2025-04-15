<div align="center">

# NVIDIA NeMo with Skypilot for HPE AI Essentials - Demo

</div>

## Requirements

- `~/.kube/config`
    - [Minimum permissions required for SkyPilot](https://docs.skypilot.co/en/latest/cloud-setup/cloud-permissions/kubernetes.html)
- `~/.gitconfig`
    - Add `/app` as safe directory
      ```bash
      git config --global --add safe.directory /app
      ```

## Preparation

- Download dataset
  ```bash
  huggingface-cli download --repo-type dataset --local-dir data/ Atom007/mc4-japanese-data mc4-ja-tfrecord_5k.jsonl
  ```
- Download base model
  ```bash
  huggingface-cli download rinna/gemma-2-baku-2b-it
  ```

## How to Run

- Run client container
  ```bash
  make up
  ```
- Prepare dataset (inside the client container)
  ```bash
  make dataset
  ```
- Run NeMo program (inside the client container)
  ```bash
  make run
  ```
- Run inference (inside the pod)
  ```bash
  conda deactivate
  python /nemo_run/code/nemo_skypilot_inference.py
  ```
- Tear down cluster (inside the client container)
  ```bash
  make down
  ```

## Check status

- Check status of the cluster
  ```bash
  sky status
  ```
- Check status of the experiments
  ```bash
  nemo experiment status nemo_demo
  ```
