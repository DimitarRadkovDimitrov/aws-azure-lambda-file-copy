import boto3
from botocore.exceptions import ClientError


def grant_s3_lambda_permissions(client, function_name):
    try:
        response = client.add_permission(
            Action='lambda:InvokeFunction',
            FunctionName=function_name,
            Principal='s3.amazonaws.com',
            StatementId='ID-1'
        )
    except ClientError as e:
        pass


def get_all_buckets_without_lambda_event(client, lambda_config_id, s3_event_name):
    buckets_to_configure = []
    buckets = get_all_buckets_by_name(client)

    if len(buckets) == 0:
        print("Currently no s3 buckets exist.")
        return buckets
    else:
        for bucket in buckets:
            if not has_lambda_invoke_event(client, bucket, lambda_config_id, s3_event_name):
                buckets_to_configure.append(bucket)
        
        return buckets_to_configure


def get_all_buckets_by_name(client):
    return [bucket['Name'] for bucket in client.list_buckets()['Buckets']]


def has_lambda_invoke_event(client, bucket, lambda_arn, s3_event_name):
    bucket_config = client.get_bucket_notification_configuration(Bucket=bucket)

    if 'LambdaFunctionConfigurations' not in bucket_config:
        return False

    if (bucket_config['LambdaFunctionConfigurations'][0]['LambdaFunctionArn'] == lambda_arn and
            s3_event_name in bucket_config['LambdaFunctionConfigurations'][0]['Events']):
        return True

    return False


def add_lambda_invoke_event(client, bucket, lambda_arn, s3_event_name):
    client.put_bucket_notification_configuration(
        Bucket=bucket,
        NotificationConfiguration={
            'LambdaFunctionConfigurations':[{
                'LambdaFunctionArn': lambda_arn,
                'Events':[
                    s3_event_name
                ]
            }]
        }
    )


if __name__ == "__main__":
    lambda_arn = '[YOUR_LAMBDA_ARN]'
    s3_event_name = 's3:ObjectCreated:Put'

    s3_client = boto3.client('s3')
    lambda_client = boto3.client('lambda', 'us-east-1')

    grant_s3_lambda_permissions(lambda_client, lambda_arn)
    print("Granted invoke function permissions to s3 service.")

    buckets = get_all_buckets_without_lambda_event(s3_client, lambda_arn, s3_event_name)
    for bucket in buckets:
        add_lambda_invoke_event(s3_client, bucket, lambda_arn, s3_event_name)
        print(f"Added Lamda Function event to bucket {bucket}.")
