import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import pickle
import schedule_manager as sch
import os

access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

conn = S3Connection(access_key_id, secret_access_key)
bucket = conn.get_bucket('coursetracker')
k = Key(bucket)
k.key = 'data'

def save():
	pickle.dump(sch.master_list, open('/tmp/save.p', 'wb'))
	k.set_contents_from_file(open('/tmp/save.p', 'rb'))
	print('saved data to s3')

def load():
	k.get_contents_to_filename('/tmp/save.p')
	sch.master_list = pickle.load(open('/tmp/save.p', 'rb'))
	print('loaded data from s3')