import json
from boto3.session import Session

class Storage:
    def __init__(self, s3_bucket, profile_name):
        self.s3_bucket = s3_bucket
        self.session = Session(profile_name=profile_name)
        self.s3 = self.session.resource('s3')
        self.s3_client = self.session.client('s3')

    def putObject(self, data, s3_key):
        try:
            self.s3_client.put_object(
                Body=data,
                Bucket=self.s3_bucket,
                Key=s3_key
            )
        except Exception as e:
            print(f"Error putting object: {str(e)}")

    def getObject(self, s3_key):
        try:
            obj = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=s3_key
            )
            data = obj['Body'].read()
            return data
        except Exception as e:
            print(f"Error getting object: {str(e)}")
