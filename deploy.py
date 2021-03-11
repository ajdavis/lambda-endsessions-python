import base64
import json
import os
import pprint
import shutil
import subprocess
import tempfile

print('PUBLISH LAYER')
os.chdir('extension')
if os.path.exists('extension.zip'):
    os.remove('extension.zip')

python_example_extension_files = os.listdir('python-example-extension')
subprocess.check_call(
    'pip3 install -q -r python-example-extension/requirements.txt'
    ' -t python-example-extension'.split())

subprocess.check_call(
    'zip -q -r extension.zip python-example-extension'.split())
for filename in os.listdir('python-example-extension'):
    if filename not in python_example_extension_files:
        shutil.rmtree(os.path.join('python-example-extension', filename))

subprocess.check_call(
    'zip -q -r extension.zip extensions python-example-extension'.split())
reply = subprocess.check_output(
    'aws lambda publish-layer-version'
    ' --layer-name python-example-extension'
    ' --region us-east-1'
    ' --zip-file fileb://extension.zip'.split())

reply_obj = json.loads(reply)
pprint.pprint(reply_obj)
layer_arn = reply_obj['LayerArn']
layer_version = reply_obj['Version']
print(f'Layer ARN {layer_arn}, version {layer_version}')
os.remove('extension.zip')
os.chdir('..')

print('PUBLISH FUNCTION')
os.chdir('function')
if os.path.exists('function.zip'):
    os.remove('function.zip')

function_files = os.listdir('.')
subprocess.check_call('pip3 install -q -r requirements.txt -t .'.split())
subprocess.check_call('zip -q -r function.zip .'.split())
reply = subprocess.check_output(
    'aws lambda update-function-code'
    ' --function-name python-mongodb-session-close-test'
    ' --region us-east-1'
    ' --publish'
    ' --zip-file fileb://function.zip'.split())

reply_obj = json.loads(reply)
pprint.pprint(reply_obj)
function_version = reply_obj['Version']
print(f'Function version {function_version}')
os.remove('function.zip')
for filename in os.listdir('.'):
    if filename not in function_files:
        shutil.rmtree(filename)

os.chdir('..')

print('UPDATE FUNCTION')
reply = subprocess.check_output(
    f'aws lambda update-function-configuration'
    f' --function-name python-mongodb-session-close-test'
    f' --region us-east-1'
    f' --layers {layer_arn}:{layer_version}'.split())

reply_obj = json.loads(reply)
pprint.pprint(reply_obj)

print('INVOKE FUNCTION')
with tempfile.NamedTemporaryFile() as tmp:
    reply = subprocess.check_output(
        f'aws lambda invoke'
        f' --function-name python-mongodb-session-close-test'
        f' --log-type Tail'
        f' {tmp.name}'.split())

    reply_obj = json.loads(reply)
    pprint.pprint(reply_obj)

    print(tmp.read().decode())
    print(base64.b64decode(reply_obj['LogResult']).decode())
