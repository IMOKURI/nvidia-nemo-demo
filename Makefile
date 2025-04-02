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

build-nemo-run: ## Build nemo-run.
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile .

push-nemo-run: ## Push nemo-run.
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

run: ## Run nemo-run.
	docker run -it --rm -v $(HOME)/.kube:/root/.kube -v $(HOME)/.gitconfig:/root/.gitconfig -v $(PWD):/app -w /app \
		-e SKYPILOT_DISABLE_USAGE_COLLECTION=1 $(IMAGE_NAME):$(IMAGE_TAG) bash
