import os
from base64 import encodebytes, decodebytes
from io import BytesIO
import requests

from utils import validate_views, validate_resources, get_resources_names_from_view
from constants import VARIBLES_TYPES, SERVICES
import render

from pymongo import MongoClient
import boto3
from PIL import Image

mongo_client = MongoClient(os.environ["MONGO_URL"])
mongo = mongo_client[os.environ["MONGO_URL"].split("/")[-1]]
s3 = boto3.client("s3", aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"], aws_secret_access_key=os.environ["AWS_ACCESS_KEY"])

S3_BUCKET = os.environ["S3_BUCKET"]
S3_URL = os.environ["S3_URL"]

STANDART_IMAGE = "https://pp.userapi.com/c824503/v824503449/c4e1/D1Vi3y86Vww.jpg"


# GROUP
def create_group(group_id, access_token):
	group = mongo.groups.find_one({"group_id":group_id})
	if group: 
		return "Group already exist", False

	mongo.groups.insert({"group_id":group_id, "access_token": access_token})
	mongo.env.insert({"group_id":group_id, "enviroment":{}})
	return "ok", True
def get_group(group_id):
	cover = mongo.covers.find_one({"group_id":group_id})
	if cover is None:
		cover = {"views":[]}
	resources = dict([(res_name, "%s/%s:%s.png" % (S3_URL, group_id, res_name)) for res_name in get_resources_names_from_view(cover["views"])])
	
	result, code = get_enviroment(group_id)
	if not code:
		return result, code

	enviroment = result

	return {"views": cover["views"], "resources": resources, "enviroment": enviroment, "services":SERVICES}, True
def is_group_exist(group_id):
	group = mongo.groups.find_one({"group_id":group_id})
	if group is None:
		return False
	return True
def get_access_token(group_id):
	group = mongo.groups.find_one({"group_id":group_id})	
	if not group: 
		return "Unknown group id", False

	return group["access_token"], True

# COVER
def set_cover(group_id, views, resources):
	message, code = validate_views(views)
	if not code:
		return message, code

	old_cover = mongo.covers.find_one({"group_id":group_id})
	if not old_cover: 
		old_views = None
	else:
		old_views = old_cover["views"]

	message, code = validate_resources(group_id, views, old_views, resources)
	if not code:
		return message, code

	for key, image in resources.items():
		if ";base64," in image:
			image = image.split(";base64,")[1]

		image = image.encode()
		image_obj = BytesIO(decodebytes(image))
		image = Image.open(image_obj)
		image.save(image_obj, 'png')
		image_obj.seek(0)


		key = "%s:%s.png" % (group_id, key)

		s3.upload_fileobj(image_obj, S3_BUCKET, key)
		s3.put_object_acl(ACL='public-read', Bucket=S3_BUCKET, Key=key)

	old_cover = mongo.covers.find_one({"group_id":group_id})
	cover = {"group_id":group_id, "views":views}
	
	if not old_cover: 
		mongo.covers.insert(cover)
	else:
		mongo.covers.update_one({"group_id":group_id}, {"$set":cover})

	return "ok", True
def get_resources(group_id):
	result, code = get_group(group_id)
	if not code:
		return result, code

	views = result["views"]
	enviroment = result["enviroment"]

	resources_names = get_resources_names_from_view(views)
	resources = {}

	for res_name in resources_names:
		res = BytesIO()
		s3.download_fileobj("donatelo", "%s:%s.png" % (group_id, res_name), res)
		res.seek(0)
		res = Image.open(res)

		resources[res_name] = res

	for view in views:
		if view["type"] == "image":
			res = requests.get(enviroment.get(view["value"], STANDART_IMAGE)).content
			try:
				res = Image.open(BytesIO(res))
			except Exception as ex:
				return "Error to load image from %s" % view["value"], False
				#res = Image.new("RGBA", (10, 10))
			resources["%s:image" % view["id"]] = res

	return resources, True
def get_cover_image(group_id):
	result, code = get_group(group_id)
	if not code:
		return result, code
	
	views = result["views"]
	env = result["enviroment"]

	result, code = get_resources(group_id)
	if not code:
		return result, code

	resources = result
	cover = render.render_cover(views, resources, env)

	return cover


# ENVIROMENT
def get_enviroment(group_id):
	enviroment = mongo.env.find_one({"group_id":group_id})
	if enviroment is None:
		return "Unknown group id", False

	enviroment = enviroment["enviroment"]
	return enviroment, True
def set_enviroment(group_id, enviroment):
	result, code = get_enviroment(group_id)
	if not code:
		return result, code
	mongo.env.update_one({"group_id":group_id}, {"$set":{"group_id":group_id, "enviroment":enviroment}})
	return "ok", True

# VARIBLE
def get_varible(group_id, varible_name):
	result, code = get_enviroment(group_id)
	if not code:
		return result, code

	varible = result.get(varible_name)

	if varible is None:
		return "Unknown varible name: %s" % varible_name, False

	return varible, True
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
	
	result, code = set_enviroment(group_id, enviroment)
	if not code:
		return result, code

	return "ok", True
def set_varible(group_id, varible_name, value):
	result, code = get_varible(group_id, varible_name)
	if not code:
		return result, code
	cur_value = result
	
	result, code = get_enviroment(group_id)
	if not code:
		return result, code
	enviroment = result

	if not varible_name in enviroment:
		return "Unknown varible name: %s" % varible_name, False

	if not type(cur_value) is type(value): 
		return "Varible type must be %s but you use %s" % (type(cur_value), type(value)), False

	enviroment[varible_name] = value
	result, code = set_enviroment(group_id, enviroment)
	if not code:
		return result, code

	return "ok", True
def delete_varible(group_id, varible_name):
	result, code = get_enviroment(group_id)
	if not code:
		return result, code
	enviroment = result

	if not varible_name in enviroment:
		return "Unknown varible name: %s" % varible_name, False

	enviroment.pop(varible_name)
	result, code = set_enviroment(group_id, enviroment)
	if not code:
		return result, code

	return "ok", True
