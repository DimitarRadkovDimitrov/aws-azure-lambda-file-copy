import json, boto3


def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    s3 = event['Records'][0]['s3']
    bucket_name = s3['bucket']['name']
    object_key = s3['object']['key']
    
    copy_bucket_name = create_bucket_copy_if_not_exists(s3_client, bucket_name)
    copy_bucket = boto3.resource('s3').Bucket(copy_bucket_name)
    copy_bucket.wait_until_exists()
    create_file_copy_if_not_exists(s3_client, bucket_name, copy_bucket_name, object_key)
    

def create_bucket_copy_if_not_exists(client, bucket_name):
    copy_bucket = bucket_name + "-copy"
    if copy_bucket not in client.list_buckets():
        client.create_bucket(Bucket=copy_bucket)
    return copy_bucket
    
    
def create_file_copy_if_not_exists(client, src_bucket_name, dest_bucket_name, object_key):
    copy_file = object_key + "-copy"
    client.copy_object(
        Bucket=dest_bucket_name, 
        CopySource={
            'Bucket': src_bucket_name,
            'Key': object_key
        },
        Key=copy_file
    )
