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

## How to Run

- Run client container
  ```bash
  make run
  ```
- Run NeMo program
  ```bash
  python nemo_skypilot_demo.py
  ```
