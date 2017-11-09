import os
from base64 import encodebytes, decodebytes
from io import BytesIO

from utils import validate_views, validate_resources, get_resources_names_from_view
from constants import VARIBLES_TYPES

from pymongo import MongoClient
import boto3


mongo_client = MongoClient(os.environ["MONGO_URL"])
mongo = mongo_client[os.environ["MONGO_URL"].split("/")[-1]]
s3 = boto3.client("s3", aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"], aws_secret_access_key=os.environ["AWS_ACCESS_KEY"])

S3_BUCKET = os.environ["S3_BUCKET"]
S3_URL = os.environ["S3_URL"]



def get_cover(group_id):
	cover = mongo.covers.find_one({"group_id":group_id})
	if cover is None:
		return "Unknown group id", False
	resources = dict([(res_name, "%s/%s:%s.png" % (S3_URL, group_id, res_name)) for res_name in get_resources_names_from_view(cover["views"])])
	
	return {"views": cover["views"], "resources": resources}, True


def get_enviroment(group_id):
	enviroment = mongo.enviroment.find_one({"group_id":group_id})
	if enviroment is None:
		return "Unknown group id", False

	return enviroment, True


def get_varible(group_id, varible_name):
	result, code = get_enviroment(group_id)
	if not code:
		return result, code
	varible = result.get(varible_name)

	if varible is None:
		return "Unknown varible name", False

	return varible, True


def get_access_token(group_id):
	group = mongo.groups.find_one({"group_id":group_id})	
	if not group: 
		return "Unknown group id", False

	return group["access_token"], True


def create_group(group_id, access_token):
	group = mongo.groups.find_one({"group_id":group_id})
	if group: 
		return "Group already exist", False

	mongo.group.insert({"group_id":group_id, "access_token": access_token})
	mongo.enviroment.insert({"group_id":group_id})
	return "ok", True


def set_cover(group_id, views, resources):
	message, code = validate_views(views)
	if not code:
		return message, code

	old_cover = mongo.covers.find_one({"group_id":group_id})
	if not old_cover: 
		old_views = []
	else:
		old_views = old_cover["views"]

	message, code = validate_resources(group_id, views, old_views, resources)
	if not code:
		return message, code

	for key, image in resources.items():
		image = BytesIO(decodebytes(image))
		key = "%s:%s.png" % (group_id, key)

		s3.upload_fileobj(image, S3_BUCKET, key)
		s3.put_object_acl(ACL='public-read', Bucket=S3_BUCKET, Key=key)

	old_cover = mongo.covers.find_one({"group_id":group_id})
	cover = {"group_id":group_id, "views":views}
	
	if not old_cover: 
		mongo.covers.insert(cover)
	else:
		mongo.covers.update_one({"group_id":group_id}, {"$set":cover})

	return "ok", True



def set_varible(group_id, varible_name, value):
	result, code = get_varible(group_id, varible_name)
	if not code:
		return result, code

	cur_value = result
	enviroment = get_enviroment(group_id)

	if not type(cur_value) is type(value): 
		return "Varible type must be %s but you use %s" % (type(cur_value), type(value)), False

	enviroment[varible_name] = value
	mongo.enviroment.update_one({"group_id":group_id}, {"$set":enviroment})

	return "ok", True



def create_varible(group_id, varible_name, varible_type):
	if not varible_type in VARIBLES_TYPES:
		return "Unknown varible type", False

	result, code = get_enviroment(group_id)
	if not code:
		return result, code
	enviroment = result

	if not enviroment.get(varible_name) is None:
		return "Varible already exist", False

	enviroment[varible_name] = VARIBLES_TYPES[varible_type]
	mongo.enviroment.update_one({"group_id":group_id}, {"$set":enviroment})

	return "ok", True

