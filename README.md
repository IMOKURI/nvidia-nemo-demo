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
- Prepare dataset [`Atom007/mc4-japanese-data`](https://huggingface.co/datasets/Atom007/mc4-japanese-data)
  ```bash
  python /opt/NeMo/scripts/nlp_language_modeling/preprocess_data_for_megatron.py \
      --input=/app/data/mc4-ja-tfrecord_5k.jsonl \
      --json-keys=text \
      --tokenizer-library=megatron \
      --tokenizer-type=GPT2BPETokenizer \
      --dataset-impl=mmap \
      --output-prefix=mc4-ja-tfrecord \
      --append-eod \
      --workers=48
  ```
- Run NeMo program
  ```bash
  python nemo_skypilot_demo.py
  ```
