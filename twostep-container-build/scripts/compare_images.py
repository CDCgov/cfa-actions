import argparse
import subprocess
import sys

def main():
    """
    This script inspects a given Docker image, checks the TWO_STEP_BUILD_CACHE_KEY
    label, and compares it to a provided cache key. If they match, it reports a
    cache hit; otherwise, it reports a mismatch.

    Examples:
        python compare_images.py \
            --image ghcr.io/cdcgov/cfa-actions \
            --label TWO_STEP_BUILD_CACHE_KEY \
            --key first-step-cache-key \
            --output $GITHUB_OUTPUT
    """
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-i', '--image', required=True,
        help='Full image name (e.g. azurecr.io/cdcgov/cfa-actions).'
        )
    parser.add_argument(
        '-l', '--label', required=True,
        help='Label to check for in the image.'
    )
    parser.add_argument(
        '-k', '--key', required=True,
        help='Expected cache key (first-step-cache-key).'
        )
    parser.add_argument(
        '-o', '--output', default=None,
        help='Optional path for writing outputs.'
        )
    parser.add_argument(
        '-s', '--strategy', default='docker',
        help='Strategy to use for pulling the image. Default: docker.'
        )

    
    args = parser.parse_args()

    # Construct the full image reference, e.g., ghcr.io/cdcgov/cfa-actions:dependencies-latest
    image = args.image

    try:
        # Run docker inspect to get the TWO_STEP_BUILD_CACHE_KEY label
        # The --format directive returns only the label's value
        result = subprocess.check_output([
            args.strategy, "inspect",
            "--format={{ index .Config.Labels \"" + args.label + "\" }}",
            image
        ])
    except subprocess.CalledProcessError:
        print("Error: Unable to inspect the image or the image does not exist.")
        sys.exit(1)

    label_value = result.decode("utf-8").strip()

    # Compare label_value with the expected cache key
    print(f"Expected : {args.key}")
    print(f"Found    : {label_value}")
    if label_value != args.key:
        print("Cache hash does not match.")
        output_line = "cache-hit=false"
    else:
        print("Cache hash matches (all good!).")
        output_line = "cache-hit=true"

    # If a GitHub output file is provided, append the result line
    if args.output:
        try:
            with open(args.output, 'a', encoding='utf-8') as f:
                f.write(f"{output_line}\n")
        except OSError as e:
            print(f"Warning: Could not write to GitHub output file ({e}).")
    else:
        print(output_line)

if __name__ == "__main__":
    main()