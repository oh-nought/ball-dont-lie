from dotenv import load_dotenv
import os

load_dotenv()

SEASONS = [str(year) for year in range(2003, 2025)]

S3_BUCKET = os.getenv("S3_BUCKET")
PROFILE = os.getenv("AWS_PROFILE")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_HOST= os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv('DB_PORT')