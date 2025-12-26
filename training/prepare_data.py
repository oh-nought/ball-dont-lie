import pandas as pd
import json
import io
from src.settings import S3_BUCKET
from src.execution.storage import Storage

'''
this is only to be used for the first run
'''

# storage = Storage(s3_bucket=S3_BUCKET)

# with open("training/data/intents.json", "r") as f:
#     data = json.load(f)

# data_str = json.dumps(data)
# data_bytes = data_str.encode('utf-8')

# storage.putObject(data=data_bytes, s3_key='datasets/intent_classifier/v000/train.json')