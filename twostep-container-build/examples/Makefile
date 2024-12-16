ifndef TAG
TAG := latest
endif

ifndef IMAGE
IMAGE := ghcr.io/cdcgov/cfa-actions
endif

ifndef ENGINE
ENGINE := podman
endif

deps:
	$(ENGINE) build \
		--no-cache \
		-t $(IMAGE):dependencies-$(TAG) -f Containerfile.dependencies

build:
	cd ../../ && \
		$(ENGINE) build \
		--build-arg TAG=dependencies-$(TAG) \
		--build-arg GH_SHA=example \
		--build-arg IMAGE=$(IMAGE) \
		--no-cache \
		-t $(IMAGE):$(TAG) \
		-f twostep-container-build/examples/Containerfile

print-sha:
	$(ENGINE) inspect $(IMAGE):$(TAG) --format='{{json .Config.Labels}}' | jq .