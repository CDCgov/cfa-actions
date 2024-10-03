import re
import json
import sys
import os

# Retrieving environment variables
ARTIFACT_NAME = os.environ.get('ARTIFACT_NAME')
SHA = os.environ.get('SHA')

def find_artifact() -> str:
    fn = '_artifacts-' + SHA + '.json'
    with open(fn, 'r') as file:
        data = json.load(file)

    artifacts = data.get('artifacts')

    for i in range(len(artifacts)):

        print(f"Artifact: {artifacts[i]}")

        name = artifacts[i].get('name')
        id = artifacts[i].get('id')

        if not name:
            continue

        if not id:
            continue

        if ARTIFACT_NAME == name:
            return str(id)
    return ''

id = find_artifact()

if id == '':
    print(f"Artifact { ARTIFACT_NAME } not found.")
    sys.exit(1)

with open(SHA + '_artifact_id', 'w') as file:
    file.write(id)