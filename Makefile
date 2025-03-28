.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / \
		{printf "\033[38;2;98;209;150m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

export
NOW = $(shell date '+%Y%m%d-%H%M%S')

.PHONY: run
run: ## run
	docker run -it --rm -u 1000 -v $(HOME)/.kube:/home/ubuntu/.kube -v $(PWD):/app -w /app imokuri123/nemo-jupyter:v0.0.3 bash

