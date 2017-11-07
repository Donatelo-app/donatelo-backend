import os
from base64 import encodebytes, decodebytes
from io import BytesIO

from utils import validate_views, validate_resources

from pymongo import MongoClient
import boto3


mongo_client = MongoClient(os.enviroment["MONGO_URL"])
mongo = mongo_client[os.enviroment["MONGO_URL"].split("/")[-1]]
s3 = boto3.client("s3", aws_access_key_id=os.enviroment["AWS_ACCESS_KEY_ID"], aws_secret_access_key=os.enviroment["AWS_ACCESS_KEY"])

S3_BUCKET = os.enviroment["S3_BUCKET"]
S3_URL = os.enviroment["S3_URL"]

def get_cover(group_id):
	pass

def get_enviroment(group_id):
	enviroment = mongo.enviroment.find_one({"group_id":group_id})
	return enviroment

def get_varible(group_id, varible_name):
	enviroment = mongo.enviroment.find_one({"group_id":group_id})
	return enviroment.get(varible_name)

def get_access_token(group_id):
	group = mongo.groups.find_one({"group_id":group_id})	
	if not group: return None

	return group["access_token"]


def create_group(group_id, access_token):
	group = mongo.groups.find_one({"group_id":group_id})
	if group: return False

	mongo.group.insert({"group_id":group_id, "access_token": access_token})
	return True

def set_cover(group_id, views, resources):
	message, code = validate_views(views)
	if not code:
		return message, code

	old_views = mongo.covers.find_one({"group_id":group_id})
	if not old_cover: 
		old_views = []
	else:
		old_views = old_views["views"]

	message, code = validate_resources(group_id, views, old_views, resources)
	if not code:
		return message, code

	for key, image in resources.items():
		image = BytesIO(encodebytes(image))
		key += ".png"

		s3.upload_fileobj(im, S3_BUCKET, key)
		s3.put_object_acl(ACL='public-read', Bucket=S3_BUCKET, Key=key)

	old_cover = mongo.covers.find_one({"group_id":group_id})
	cover = {"group_id":group_id, "views":views}
	
	if not old_cover: 
		mongo.covers.insert(cover)
	else:
		mongo.covers.update_one({"group_id":group_id}, {"$set":cover})

	return "ok", True

def set_varible(group_id, varible_name, value):
	enviroment = mongo.enviroment.find_one({"group_id":group_id})
	cur_value = enviroment.get(varible_name) 

	if cur_value is None: 
		return "Varible is not exist",False
	if not type(cur_value) is type(value): 
		reutrn "Varible type must be %s but you use %s" % (type(cur_value), type(value)), False

	enviroment[varible_name] = value
	mongo.enviroment.update_one({"group_id":group_id}, {"$set":enviroment})

	return "Ok", True