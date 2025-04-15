.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / \
		{printf "\033[38;2;98;209;150m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

export
NOW = $(shell date '+%Y%m%d-%H%M%S')

#######################################################################################################################
# nemo-run
#######################################################################################################################
IMAGE_NAME = imokuri123/nemo-run
IMAGE_TAG = v0.0.3

.PHONY: build
build: ## Build nemo-run container
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile.skypilot .

.PHONY: push
push: ## Push nemo-run container
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

#######################################################################################################################
# nemo-vllm
#######################################################################################################################
VLLM_IMAGE_NAME = imokuri123/nemo-vllm
VLLM_IMAGE_TAG = v0.0.1

.PHONY: build-vllm
build-vllm: ## Build nemo-vllm container
	docker build -t $(VLLM_IMAGE_NAME):$(VLLM_IMAGE_TAG) -f Dockerfile.vllm .

.PHONY: push-vllm
push-vllm: ## Push nemo-vllm container
	docker push $(VLLM_IMAGE_NAME):$(VLLM_IMAGE_TAG)


#######################################################################################################################
# operations
#######################################################################################################################
.PHONY: up
up: ## Start nemo-run container
	docker run -it --rm \
		-v $(HOME)/.kube:/root/.kube \
		-v $(HOME)/.gitconfig:/root/.gitconfig \
		-v $(PWD):/app \
		-w /app \
		-e SKYPILOT_DISABLE_USAGE_COLLECTION=1 \
		$(IMAGE_NAME):$(IMAGE_TAG) \
		bash

.PHONY: dataset
dataset: ## Preprocess dataset
	python /opt/NeMo/scripts/nlp_language_modeling/preprocess_data_for_megatron.py \
		--input=/app/data/mc4-ja-tfrecord_5k.jsonl \
		--json-keys=text \
		--tokenizer-library=megatron \
		--tokenizer-type=GPT2BPETokenizer \
		--dataset-impl=mmap \
		--output-prefix=/app/data/mc4-ja-tfrecord \
		--append-eod \
		--workers=48

.PHONY: run
run: ## Run application
	python ./nemo_skypilot_training.py

.PHONY: download
download: ## Download checkpoints
	rsync -Pavz nemo_demo:/checkpoints/gemma2_baku_lora checkpoints/

.PHONY: down
down: ## Down skypilot cluster
	sky down --yes nemo_demo

.PHONY: up-vllm
up-vllm: ## Start nemo-vllm container
	docker run -it --rm \
		-v $(PWD):/app \
		-w /app \
		$(VLLM_IMAGE_NAME):$(VLLM_IMAGE_TAG) \
		bash
