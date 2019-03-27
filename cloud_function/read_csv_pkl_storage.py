# google library
from google.cloud import storage
import gcsfs


import pandas as pd
import pickle


storage_client = storage.Client()
fs = gcsfs.GCSFileSystem(project='your project id as a string')
bucket_name = 'your bucket name as a string'


# open .csv file
csv_file = fs.open(bucket_name + "/path to your csv file in your bucket")
# read it with pandas
df = pd.read_csv(csv_file)


# open .pkl file
pkl_file = fs.open(bucket_name + 'path to your .pkl file')
# load pkl file
model = pickle.load(pkl_file)

