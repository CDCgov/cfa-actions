# Post artifact as a comment [![Test PR post artifact](https://github.com/CDCgov/cfa-actions/actions/workflows/test-post-artifact.yml/badge.svg)](https://github.com/CDCgov/cfa-actions/actions/workflows/test-post-artifact.yml)

## Inputs

| Field         | Description                                                                                                                             | Required | Default        |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------|----------|----------------|
| `gh-token`      | The GitHub token to use for the API calls. | true | - |
| `artifact-name` | Artifact name as in the `actions/upload-artifact` step. | false    | `artifact`     |
| `message`       | Message template to be posted in the PR, as Github-flavored Markdown (GFM). Use the placeholder `{ artifact-url }` to reference the URL of the uploaded artifact, either raw or as GFM formatted link. Use the `{ artifact-name }` placeholder to include the artifact name in the message | false    | `'Thank you for your contribution ${{ github.actor }} :rocket:! Your { artifact-name } is ready for download :point_right: [here]({ artifact-url }) :point_left:!'` |
| `python`        | The path to the Python executable. | false    | `'python'`       |

This action only runs in PRs and requires the `pull-requests: write` and `actions: read` permissions. 

## Example: Post artifact created within a job

Here are the contents of a job that (i) uploads an artifact using `actions/upload-artifact` and (ii) posts the artifact as a comment using this action. The action requires the runner to have: `python` and `gh cli` installed.


```yaml
    # Required permissions
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        name: Checkout code

      # Uploading an artifact with name 'readme'
      - uses: actions/upload-artifact@v4
        name: Upload artifact
        with:
          path: './README.md'
          name: readme

      # Post the artifact pulling the id from the `readme` step.
      - name: Post the artifact
        uses: CDCgov/cfa-actions/post-artifact@1.2.0
        if: ${{ github.event_name == 'pull_request' }}
        with:
          artifact-name: readme
          gh-token: ${{ secrets.GITHUB_TOKEN }}
          message: 'Thank you for your contribution ${{ github.actor }} :rocket:! Your { artifact-name } is ready for download :point_right: [here]({ artifact-url }) :point_left:!'
```

For a live example, see [../.github/workflows/test-post-artifact.yml](../.github/workflows/test-post-artifact.yml).

## Example: Post an artifact created in a previous job

When passing between jobs, the artifact id can be passed as an output. Here is an example of how to do it:

```yaml
jobs:

  build:

    runs-on: ubuntu-latest

    # Expose the artifact id as an output
    outputs:
      artifact-id: ${{ steps.upload.outputs.artifact-id }}

    steps:
      - uses: actions/checkout@v4
        name: Checkout code

      # Uploading an artifact with id 'readme'
      - uses: actions/upload-artifact@v4
        name: Upload artifact
        with:
          path: './README.md'
          name: readme

  post:
    runs-on: ubuntu-latest
    
    # This job depends on the `build` job
    needs: build

    # Required permissions
    permissions:
      actions: read
      pull-requests: write

    steps:
      # Post the artifact pulling the id from the `readme` step.
      # The msg will refer to the arfitact as 'README file'.
      - name: Post the artifact
        if: ${{ github.event_name == 'pull_request' }}
        uses: CDCgov/cfa-actions/post-artifact@main
        with:
          artifact-name: readme
          gh-token: ${{ secrets.GITHUB_TOKEN }}

```
