import pandas as pd
import json
import io
from src.settings import S3_BUCKET
from src.execution.storage import Storage

'''
this is only to be used for the first run
from here on out, training data will be pulled through the s3 bucket
'''

# storage = Storage(s3_bucket=S3_BUCKET)

# with open("training/data/intents.json", "r") as f:
#     data = json.load(f)

# df = pd.DataFrame(data[""], columns=["query", "intent"])
# buffer = io.BytesIO()
# test = df.to_csv(buffer, index=False)
# buffer.seek(0)

# storage.putObject(data=buffer, s3_key='datasets/intent_classifier/v000/train.json')