# Determine this makefile's path.
# Be sure to place this BEFORE `include` directives, if any.
# THIS_FILE := $(lastword $(MAKEFILE_LIST))
THIS_FILE := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# include vars.mk

.PHONY: install
install: install ## install jena tools
	@mkdir $(CURRENT_DIR)/.tmp
	cd $(CURRENT_DIR)/.tmp && \
		wget https://downloads.apache.org/jena/binaries/apache-jena-3.17.0.tar.gz && \
		tar xzf apache-jena-3.17.0.tar.gz && \
		ln -s apache-jena-3.17.0 jena

.PHONY: validate-shape
validate-shape: ## validate shape
	$(CURRENT_DIR)/.tmp/jena/bin/riot --validate $(CURRENT_DIR)/dsp-repository/v1/dsp-repository.shacl.ttl

.PHONY: validate-example
validate-example: ## validate example
	$(CURRENT_DIR)/.tmp/jena/bin/riot --validate $(CURRENT_DIR)/example/example-metadata.ttl
	$(CURRENT_DIR)/.tmp/jena/bin/shacl validate --shapes $(CURRENT_DIR)/dsp-repository/v1/dsp-repository.shacl.ttl --data $(CURRENT_DIR)/example/example-metadata.ttl
	$(CURRENT_DIR)/.tmp/jena/bin/riot --validate $(CURRENT_DIR)/example/example-metadata-minimal.ttl
	$(CURRENT_DIR)/.tmp/jena/bin/shacl validate --shapes $(CURRENT_DIR)/dsp-repository/v1/dsp-repository.shacl.ttl --data $(CURRENT_DIR)/example/example-metadata-minimal.ttl
	$(CURRENT_DIR)/.tmp/jena/bin/riot --validate $(CURRENT_DIR)/example/example-metadata-maximal.ttl
	$(CURRENT_DIR)/.tmp/jena/bin/shacl validate --shapes $(CURRENT_DIR)/dsp-repository/v1/dsp-repository.shacl.ttl --data $(CURRENT_DIR)/example/example-metadata-maximal.ttl

.PHONY: validate-example-with-check
validate-example-with-check: ## validate example and check validation report 
	$(CURRENT_DIR)/.tmp/jena/bin/shacl validate --shapes $(CURRENT_DIR)/dsp-repository/v1/dsp-repository.shacl.ttl --data $(CURRENT_DIR)/example/example-metadata.ttl | grep -q "sh:conforms  true"
	$(CURRENT_DIR)/.tmp/jena/bin/shacl validate --shapes $(CURRENT_DIR)/dsp-repository/v1/dsp-repository.shacl.ttl --data $(CURRENT_DIR)/example/example-metadata-minimal.ttl | grep -q "sh:conforms  true"
	$(CURRENT_DIR)/.tmp/jena/bin/shacl validate --shapes $(CURRENT_DIR)/dsp-repository/v1/dsp-repository.shacl.ttl --data $(CURRENT_DIR)/example/example-metadata-maximal.ttl | grep -q "sh:conforms  true"

.PHONY: validate
validate: validate-shape validate-example ## validate all

.PHONY: clean
clean: ## remove temporary artifacts
	@rm -rf $(CURRENT_DIR)/.tmp || true

.PHONY: help
help: ## this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.PHONY: install-requirements
install-requirements: ## install python requirements
		pip3 install -r requirements.txt
		
.PHONY: test
test: ## runs all tests
	bazel test --test_output=all //test/...

.DEFAULT_GOAL := help
