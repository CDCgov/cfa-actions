#!/usr/bin/env bash

# Default values
OUTPUT=""
STRATEGY="docker"

# Parse flags
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -r|--registry) REGISTRY="$2"; shift ;;
        -i|--image) IMAGE="$2"; shift ;;
        -t|--tag) TAG="$2"; shift ;;
        -o|--output) OUTPUT="$2"; shift ;;
        -s|--strategy) STRATEGY="$2"; shift ;;
        -h|--help)
            echo "Check if an image exists in a registry."
            echo ""
            echo "The script will attempt to pull the image from the registry."
            echo "If the image is found, it will write 'image-found=true' to the output file."
            echo "If the image is not found, it will write 'image-found=false' to the output file."
            echo ""
            echo "Usage: $0 -r <registry> -i <image> -t <tag> [-o <output>]"
            echo ""
            echo "Options:"
            echo "  -r, --registry  The registry where the image is stored."
            echo "  -i, --image     The image name."
            echo "  -t, --tag       The image tag."
            echo "  -o, --output    The output file to write the result to."
            echo "  -s, --strategy  The strategy to use for pulling the image. Default: docker"
            exit 0
            ;;
        *) 
            echo "Unknown parameter passed: $1"
            echo "Usage: $0 -r <registry> -i <image> -t <tag> [-o <output>]"
            exit 1
            ;;
    esac
    shift
done

# Check required parameters
if [ -z "${REGISTRY}" ] || [ -z "${IMAGE}" ] || [ -z "${TAG}" ]; then
    echo "Error: Missing required parameters."
    echo "Usage: $0 -r <registry> -i <image> -t <tag> [-o <output> -s <strategy>]"
    exit 1
fi

# Ensuring the registry has a trailing slash
if [ "${REGISTRY: -1}" != "/" ]; then
    REGISTRY="${REGISTRY}/"
fi

# Ensuring we can pull the image, if cache exists
if [ "${STRATEGY}" == "docker" ] || [ "${STRATEGY}" == "podman" ]; then
    
    ${STRATEGY} pull ${REGISTRY}${IMAGE}:${TAG} || \
        export IMAGE_NOT_FOUND=true
else
    echo "Error: Unknown strategy '${STRATEGY}'"
    exit 1
fi

if [ -n "$IMAGE_NOT_FOUND" ]; then
    echo "Image was not found."

    if [ -z "${OUTPUT}" ]; then
        exit 0
    fi

    echo "image-found=false" >> ${OUTPUT}
else
    echo "Image found."

    if [ -z "${OUTPUT}" ]; then
        exit 0
    fi

    echo "image-found=true" >> ${OUTPUT}
fi