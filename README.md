# AWS/Azure Lambda File Copy

Python lambda functions that are triggered whenever a file is uploaded to blob storage. Function will make a duplicate of that file and upload it to a "copy" bucket.

<br>

## Prerequisites 

* Install python project dependencies.
    ```
    pipenv install
    ```

* Create AWS Lambda function using the code in [pythonLambdaFunction.py](./pythonLambdaFunction.py).

* Modify [fileCopyTriggerAWS.py](./fileCopyTriggerAWS.py), adding your newly created AWS lambda function information.

* Setup Azure Functions python project and create storage containers.
    ```
    god help you
    ```

<br>

## Run

* Hook up lambda funtion triggers to existing s3 buckets.
    ```
    pipenv run python3 fileCopyTriggerAWS.py
    ```

<br>
