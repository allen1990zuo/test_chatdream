## Create virtual env
```
pip3 install virtualenv
virtualenv chatbot
```

## Activate virtual env
```
source chatbot/Scripts/activate
```

## Install packages
```
pip3 install -r requirements.txt
```

## Run gradio app
```
python langchain_server.py

```

## Lambda server notes:
please exclude \archive_code \context and \dream_meaning when upload to lambda server


# Test Lambda locally
## Create a test virtual: `virtualenv local`
## Activate the env: `source local/Scripts/activate`
## Install python-lambda-loca/setuptool: `pip install python-lambda-local` and `pip install setuptools`
## Install project dependency: `pip install -r requirements.txt`
## test: `python-lambda-local -f lambda_handler lambda_function.py event.json`
lambda_handler is the name of your handler function
lambda_function.py is the name of your file with Python code
event.json is the test event data
eg `python-lambda-local -f lambda_handler lambda_server.py event.json -t 100`
## Deactivate: `deactivate`

# As we have dependencies need to install and deploy to AWS lambda, we need to build zip file (only used for the initial, continue deploy will handle by AWS Codepipeline): https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
## Create a deploy virtual: `virtualenv deploy`
## Activate the env: `source deploy/Scripts/activate`
## Install dependencies: `pip install -r requirements.txt`
## Deactivate: `deactivate`
## Create a deployment package with the installed libraries at the root: `cd deploy/Lib/site-packages` and `zip -r ${OLDPWD}/function.zip .`
## Add function code files to the root of your deployment package: `cd $OLDPWD` and `zip -g function.zip lambda_function.py supporting_file1.py supporting_file2.py`
## Then use CDK package to deploy
