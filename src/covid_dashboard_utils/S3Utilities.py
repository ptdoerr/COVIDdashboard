import logging as log
import os
from pathlib import Path
import boto3

class S3Utilities:

    def __init__(self, config: dict) -> None:
        # config dict must contain following info:
        # aws_region
        # s3_bucket
        # aws_access_key_id
        # aws_secret_access_key
        self.config = config
        print('loading AWS config info: ', len(config))
        self.aws_region = config['aws_region'] #'us-east-1'
        # AWS credential now from environment variables
        self.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID') #config['aws_access_key_id']
        self.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY') #config['aws_secret_access_key']
        self.s3_bucket = config['s3_bucket']
        self.s3_public_bucket = 'cdash-public'
        print("Bucket: ", self.s3_bucket)
        self.s3_client = boto3.client('s3', 
            aws_access_key_id=self.aws_access_key_id, 
            aws_secret_access_key=self.aws_secret_access_key, 
            region_name=self.aws_region)
        self.s3_session = boto3.Session(aws_access_key_id=self.aws_access_key_id, 
            aws_secret_access_key=self.aws_secret_access_key)

        self.s3_resource = self.s3_session.resource('s3')


    def get_s3_files_list(self) -> list:
    
        files_dict = self.s3_client.list_objects(Bucket=self.s3_bucket) #['Contents']
        files_list = files_dict.keys()
        print(files_list)
        #for key in s3_client.list_objects(Bucket=s3_bucket)['Contents']:
        #   fname_full = key['Key']
        #  fname = Path(fname_full).stem
        # files_list.append(fname)
        
        return files_list

    def get_image_file_list(self, map_image_folder: str) -> list:

        image_list = []
    
        bucket = self.s3_resource.Bucket(self.s3_bucket)
        for object_summary in bucket.objects.filter(Prefix=map_image_folder):
            key = object_summary.key
            if key.endswith(".jpg"):
                image_list.append(key)
            
        return image_list

    # write io.BytesIO object to s3
    def write_to_s3(self, name, obj) -> None:
    
        log.info('writing object to s3: ', name)
        #bucket = s3_resource.Bucket(s3_bucket)
        #file_object.seek(0)
        #s3_client.upload_fileobj(s3_bucket, io.BytesIO(file_object), name)
    
        #object_bytes = file_object.read()
        #bucket.upload_fileobj(object_bytes, name)
    
        log.info('saving to s3- ', name, ' : ', len(obj))
    
        response = self.s3_client.put_object(Body=obj, Bucket=self.s3_bucket, Key=name)
        log.info(response)

    # write io.BytesIO object to s3
    def write_to_s3_public(self, name, obj) -> None:
    
        log.info('writing object to s3 public bucket: ', name)
        #bucket = s3_resource.Bucket(s3_bucket)
        #file_object.seek(0)
        #s3_client.upload_fileobj(s3_bucket, io.BytesIO(file_object), name)
    
        #object_bytes = file_object.read()
        #bucket.upload_fileobj(object_bytes, name)
    
        log.info('saving to s3- ', name, ' : ', len(obj))
    
        response = self.s3_client.put_object(Body=obj, Bucket=self.s3_public_bucket, Key=name)
        log.info(response)
    
    def read_object_from_s3(self, file_name):
    
        print('reading object from s3: ', file_name)
        s3_response_object = self.s3_client.get_object(Bucket=self.s3_bucket, Key=file_name)
        object_content = s3_response_object['Body'].read()
    
        return object_content

    def list_s3_contents(self) -> None:
        print('contents of s3 bucket: ', self.s3_bucket)
        for key in self.s3_client.list_objects(Bucket=self.s3_bucket)['Contents']:
            fname_full = key['Key']
            fname = Path(fname_full).stem
            print(fname_full, " : ", fname)

    def list_s3_public_contents(self) -> None:
        print('contents of s3 bucket: ', self.s3_public_bucket)
        for key in self.s3_client.list_objects(Bucket=self.s3_public_bucket)['Contents']:
            fname_full = key['Key']
            fname = Path(fname_full).stem
            print(fname_full, " : ", fname)
        