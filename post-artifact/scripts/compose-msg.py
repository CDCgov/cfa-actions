import re

# Retrieving environment variables
import os
import sys

ARTIFACT_NAME = os.environ.get('ARTIFACT_NAME')
MESSAGE = os.environ.get('MESSAGE')
SERVER_URL = os.environ.get('SERVER_URL')
REPOSITORY = os.environ.get('REPOSITORY')
RUN_ID = os.environ.get('RUN_ID')
ARTIFACT_ID = os.environ.get('ARTIFACT_ID')
SHA = os.environ.get('SHA')

msg = "[]("+ re.sub(r'\s+', '_', ARTIFACT_NAME)+")"
msg = msg + MESSAGE

updated = re.sub(
  r'{ artifact-name }',
  ARTIFACT_NAME,
  msg
  )

if not re.search(r'{ artifact-url }', updated):
    print(
        "The message template must include the placeholder " \
        "{ artifact-url }."
        )
    sys.exit(1)

updated = re.sub(
    r'{ artifact-url }',
    SERVER_URL + '/' + REPOSITORY + '/actions/runs/' + RUN_ID + \
        '/artifacts/' + ARTIFACT_ID,
    updated
    )

with open('msg-' + SHA + '.txt', 'w') as file:
    file.write(updated)