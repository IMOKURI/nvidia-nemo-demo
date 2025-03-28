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
IMAGE_TAG = v0.0.1

build-nemo-run: ## Build nemo-run.
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile.nemo-run .

push-nemo-run: ## Push nemo-run.
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

run: ## Run nemo-run.
	docker run -it --rm -u 1000 -v $(HOME)/.kube:/home/ubuntu/.kube -v $(PWD):/app -w /app \
		-e SKYPILOT_DISABLE_USAGE_COLLECTION=1 $(IMAGE_NAME):$(IMAGE_TAG) bash



#######################################################################################################################
# nemo-executor
#######################################################################################################################
EXE_IMAGE_NAME = imokuri123/nemo-executor
EXE_IMAGE_TAG = v0.0.2

build-nemo-executor: ## Build nemo-executor.
	docker build -t $(EXE_IMAGE_NAME):$(EXE_IMAGE_TAG) -f Dockerfile.nemo-executor .

push-nemo-executor: ## Push nemo-executor.
	docker push $(EXE_IMAGE_NAME):$(EXE_IMAGE_TAG)

