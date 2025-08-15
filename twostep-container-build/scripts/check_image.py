import argparse
import subprocess
import sys

def parse_args():
    """
    Check if an image exists in a registry.

    The script will attempt to pull the image from the registry.
    If the image is found, it will write 'image-found=true' to the output file.
    If the image is not found, it will write 'image-found=false' to the output file.

    Examples:
        python check_image.py -r docker.io/library -i alpine -t 3.12 -o output.txt
    """
    parser = argparse.ArgumentParser(
        description=parse_args.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-r', '--registry', required=True, help='The registry where the image is stored.')
    parser.add_argument('-i', '--image', required=True, help='The image name.')
    parser.add_argument('-t', '--tag', required=True, help='The image tag.')
    parser.add_argument('-o', '--output', help='The output file to write the result to.')
    parser.add_argument('-s', '--strategy', default='docker', help='The strategy to use for pulling the image. Default: docker')

    return parser.parse_args()

def main():
    args = parse_args()

    registry = args.registry
    image    = args.image
    tag      = args.tag
    output   = args.output
    strategy = args.strategy

    if not registry.endswith('/'):
        registry += '/'

    try:
        subprocess.run(
            [strategy, 'pull', f'{registry}{image}:{tag}'],
            check=True
        )
        image_found = True
    except subprocess.CalledProcessError:
        image_found = False

    if output:
        with open(output, 'a') as f:
            f.write(f'image-found={"true" if image_found else "false"}\n')

    print("Image found." if image_found else "Image was not found.")

if __name__ == "__main__":
    main()
