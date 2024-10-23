import json
import re
import os

# Retrieving environment variables
ARTIFACT_NAME = os.environ.get('ARTIFACT_NAME')
SHA = os.environ.get('SHA')

def main(json_comments) -> str:

    # Open the JSON file and load its contents into a Python object
    with open(json_comments, 'r') as file:
        data = json.load(file)

    if (data == []):
        return ''

    matching_msg = re.escape(
        "<!-- action-comment-id:" + re.sub(r'\s+', '_', ARTIFACT_NAME)+" -->"
        )

    # Now you can work with the 'data' object
    for i in range(len(data)):

        body = data[i].get('body')
        auth = data[i].get('user').get('login')
        url =  data[i].get('url')

        if not url:
            continue

        if not auth:
            continue

        if not body:
            continue
            
        match = re.search(r'\d+$', url)

        if not match:
            continue

        id = match.group()

        # Regex match to the body of the comment looking
        # for the expression "Thank you for your contribution"
        # if found, print the author and the body of the comment
        if (re.search(matching_msg, body)) and (re.match(r'^github-actions\[bot\]', auth)):
            return id

    return ''

id = main('_events-' + SHA + '.json')
fn = '_ID-' + SHA
with (open(fn, 'w')) as file:
    file.write(id)

with (open(fn+'_found', 'w')) as file:
    if id == '':
        file.write('false')
    else:
        file.write('true')