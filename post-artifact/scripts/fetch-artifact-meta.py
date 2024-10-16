import re
import json
import sys
import os

# Retrieving environment variables
ARTIFACT_NAME = os.environ.get('ARTIFACT_NAME')
SHA = os.environ.get('SHA')

def find_artifact() -> dict:
    fn = '_artifacts-' + SHA + '.json'
    with open(fn, 'r') as file:
        data = json.load(file)

    artifacts = data.get('artifacts')

    for i in range(len(artifacts)):

        print(f"Artifact: {artifacts[i]}")

        name = artifacts[i].get('name')
        id = artifacts[i].get('id')
        expires_at = artifacts[i].get('expires_at')

        if not name:
            continue

        if not id:
            continue

        if ARTIFACT_NAME == name:
            return dict(id=str(id), expires_at=expires_at)
    return ''

meta = find_artifact()

if meta.get('id') == '':
    print(f"Artifact { ARTIFACT_NAME } not found.")
    sys.exit(1)

with open(SHA + '_artifact_id', 'w') as file:
    file.write(meta.get('id'))

with open(SHA + '_artifact_expires_at', 'w') as file:
    file.write(meta.get('expires_at'))