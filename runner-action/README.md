# Runner Action

This action allows you to securely run scripts on the Azure Container App runners in the Azure subscription from public runners. A Github App is required to call a workflow in a cdcent repository that has access to the Container App runners.

The Container App runners have some limitations compared to `ubuntu-latest`, namely the absence of docker and lack of access to `apt-get` for installation. See the Predict handbook for more info on the Container App runners.

## Inputs and Outputs

| Field | Description | Required | Default |
|-------|-------------|----------|---------|
| `github_app_id` | A GitHub App ID installed on CDCEnt | true | |
| `github_app_pem` | The PEM-encoded private key for the GitHub APP| true | |
| `script` | A bash script to be run on the Azure self-hosted runner | true | |
| `wait_for_completion` | true/false option to wait for the dispatched workflow to complete | false | false |
| `print_logs` | true/false option to print the action logs once the workflow has completed | false | false |

## Examples and Usage
The script passed to this action is a normal bash script which means no marketplace actions can be used here.

The following example uses the `az acr import` command to pull an image from GHCR to ACR:

```yaml
  acr-import:
    name: Import image from GHCR
    runs-on: ubuntu-latest
    steps:
    - name: ACR Import
      uses: CDCgov/cfa-actions/runner-action@1.0.0 # check cfa-actions repo for latest tag
      with:
        github_app_id: ${{ secrets.CDCENT_ACTOR_APP_ID }}
        github_app_pem: ${{ secrets.CDCENT_ACTOR_APP_PEM }}
        wait_for_completion: true
        print_logs: true
        script: |
          IMAGE_TAG=${{ env.IMAGE_NAME }}:${{ steps.image-tag.outputs.tag }}

          az login --service-principal \
          --username ${{ fromJSON(secrets.AZURE_SERVICE_PRINCIPAL).clientId }} \
          --password ${{ fromJSON(secrets.AZURE_SERVICE_PRINCIPAL).clientSecret }} \
          --tenant ${{ fromJSON(secrets.AZURE_SERVICE_PRINCIPAL).tenantId }}

          az acr import --name ${{ env.REGISTRY }} \
            --source "ghcr.io/cdcgov/$IMAGE_TAG" \
            --username '${{ github.repository_owner }}'\
            --password ${{ secrets.GITHUB_TOKEN }} \
            --image "$IMAGE_TAG" \
            --force && echo 'Copied image!'

          if [ $? -ne 0 ]; then
            echo "Failed to copy image"
          fi
```
With the `wait_for_completion` and `print_logs` parameters set to true, the workflow will enter a polling loop and then print the logs. The logs from the self-hosted runner will be prefixed with a timestamp. Here is what the output for this workflow run would look like:
```
100 14462  100 14462    0     0  61107      0 --:--:-- --:--:-- --:--:-- 61279
Workflow run status: queued
Waiting for 15 seconds before retrying...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 14467  100 14467    0     0  58110      0 --:--:-- --:--:-- --:--:-- 58334
Workflow run status: in_progress
Waiting for 15 seconds before retrying...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 14470  100 14470    0     0  59790      0 --:--:-- --:--:-- --:--:-- 59793
Workflow run status: completed
Workflow run completed with conclusion: success
Run GITHUB_TOKEN='***'
Fetching logs from: https://api.github.com/repos/cdcent/cfa-cdcgov-actions/actions/runs/13729339208/logs
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

100  5847    0  5847    0     0   8428      0 --:--:-- --:--:-- --:--:--  8428
Archive:  run_logs.zip
  inflating: run_logs/Run Script/2_Run Script.txt  
  inflating: run_logs/0_Run Script.txt  
  inflating: run_logs/-2147483648_Run Script.txt  
  inflating: run_logs/Run Script/1_Set up job.txt  
  inflating: run_logs/Run Script/3_Complete job.txt  
Logs have been downloaded and unzipped to the run_logs directory.
Run # decrypt AES key using RSA private key
2025-03-07T21:09:54.2034431Z [
2025-03-07T21:09:54.2040343Z   ***
2025-03-07T21:09:54.2041331Z     "cloudName": "AzureCloud",
2025-03-07T21:09:54.2042427Z     "homeTenantId": "48aa478c-32b6-4e41-babc-cc13a9c9b986",
2025-03-07T21:09:54.2047074Z     "id": "ef340bd6-2809-4635-b18b-7e6583a8803b",
2025-03-07T21:09:54.2053012Z     "isDefault": true,
2025-03-07T21:09:54.2053992Z     "managedByTenants": [
2025-03-07T21:09:54.2054822Z       ***
2025-03-07T21:09:54.2055691Z         "tenantId": "2f4a9838-26b7-47ee-be60-ccc1fdec5953"
2025-03-07T21:09:54.2056638Z       ***
2025-03-07T21:09:54.2057360Z     ],
2025-03-07T21:09:54.2058150Z     "name": "EXT-EDAV-CFA-PRD",
2025-03-07T21:09:54.2059013Z     "state": "Enabled",
2025-03-07T21:09:54.2059963Z     "tenantId": "48aa478c-32b6-4e41-babc-cc13a9c9b986",
2025-03-07T21:09:54.2061020Z     "user": ***
2025-03-07T21:09:54.2061893Z       "name": "84181eed-46c4-49ba-b539-f688ce7c3562",
2025-03-07T21:09:54.2062871Z       "type": "servicePrincipal"
2025-03-07T21:09:54.2063699Z     ***
2025-03-07T21:09:54.2064406Z   ***
2025-03-07T21:09:54.2065705Z ]
2025-03-07T21:09:54.8360735Z WARNING: The login server endpoint suffix '.azurecr.io' is automatically omitted.
2025-03-07T21:10:06.2097970Z Copied image!
```

