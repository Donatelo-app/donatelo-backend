import os
from base64 import encodebytes, decodebytes
from io import BytesIO
from api_utils import APIResponse
import requests

from validation import validate_views, validate_resources, get_resources_names_from_view
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
		return APIResponse(message="Group already exist", error_code=1)

	mongo.groups.insert({"group_id":group_id, "access_token": access_token})
	mongo.env.insert({"group_id":group_id, "enviroment":{}})
	
	return APIResponse(message="ok")

def edit_token(group_id, access_token):
	group = mongo.groups.find_one({"group_id":group_id})
	if not group: 
		return APIResponse(message="Group is not exist", error_code=1)

	group["access_token"] = access_token
	mongo.groups.update_one({"group_id":group_id}, {"$set":group})
	
	return APIResponse(message="ok")

def get_group(group_id):
	cover = mongo.covers.find_one({"group_id":group_id})
	if cover is None:
		cover = {"views":[]}
		resources = {}
	else:
		resources = dict([(res_name, "%s/%s:%s.png" % (S3_URL, group_id, res_name)) for res_name in get_resources_names_from_view(cover["views"])])
	
	enviroment = get_enviroment(group_id)
	if enviroment.error_code:
		return enviroment

	group = {"views": cover["views"], "resources": resources, "enviroment": enviroment.value, "services":SERVICES}

	return APIResponse(value=group)

def is_group_exist(group_id):
	group = mongo.groups.find_one({"group_id":group_id})
	if group is None:
		return APIResponse(value=False, error_code=0)
	else:
		return APIResponse(value=True, error_code=0)

def get_access_token(group_id):
	group = mongo.groups.find_one({"group_id":group_id})	
	if not group: 
		return APIResponse(message="Unknown group id", error_code=1)
	else:
		return APIResponse(value=group["access_token"], error_code=0)

# COVER
def set_cover(group_id, views, resources):
	message, code = validate_views(views)
	if not code:
		return APIResponse(message=message, error_code=1)

	old_cover = mongo.covers.find_one({"group_id":group_id})
	if not old_cover: 
		old_views = None
	else:
		old_views = old_cover["views"]

	message, code = validate_resources(group_id, views, old_views, resources)
	if not code:
		return APIResponse(message=message, error_code=1)

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

	return APIResponse(message="ok")

def get_resources(group_id):
	group = get_group(group_id)
	if group.error_code:
		return group

	views = group.value["views"]
	enviroment = group.value["enviroment"]

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
				return APIResponse(message="Error to load image from %s" % view["value"], error_code=1)
				#res = Image.new("RGBA", (10, 10))
			resources["%s:image" % view["id"]] = res

	return APIResponse(value=resources)

def get_cover_image(group_id):
	group = get_group(group_id)
	if group.error_code:
		return group
	
	views = group.value["views"]
	env = group.value["enviroment"]

	resources = get_resources(group_id)
	if resources.error_code:
		return resources

	cover = render.render_cover(views, resources.value, env)

	return APIResponse(value=cover)


# ENVIROMENT
def get_enviroment(group_id):
	enviroment = mongo.env.find_one({"group_id":group_id})
	if enviroment is None:
		return APIResponse(message="Unknown group id", error_code=1)

	enviroment = enviroment["enviroment"]
	return APIResponse(value=enviroment)

def set_enviroment(group_id, enviroment):
	enviroment = get_enviroment(group_id)
	if enviroment.error_code:
		return enviroment

	mongo.env.update_one({"group_id":group_id}, {"$set":{"group_id":group_id, "enviroment":enviroment.value}})
	return APIResponse(message="ok")

# VARIBLE
def get_varible(group_id, varible_name):
	enviroment = get_enviroment(group_id)
	if enviroment.error_code:
		return enviroment

	varible = enviroment.value.get(varible_name)

	if varible is None:
		return APIResponse(message="Unknown varible name: %s" % varible_name, error_code=1)

	return APIResponse(value=varible)

def create_varible(group_id, varible_name, varible_type):
	if not varible_type in VARIBLES_TYPES:
		return APIResponse(message="Unknown varible type", error_code=1)

	enviroment = get_enviroment(group_id)
	if enviroment.error_code:
		return enviroment

	if not enviroment.value.get(varible_name) is None:
		return APIResponse(message="Varible already exist", error_code=1)

	enviroment.value[varible_name] = VARIBLES_TYPES[varible_type]
	
	set_env_status = set_enviroment(group_id, enviroment.value)
	if set_env_status.error_code:
		return set_env_status

	return APIResponse(message="ok")

def set_varible(group_id, varible_name, value):
	varible = get_varible(group_id, varible_name)
	if varible.error_code:
		return varible
	
	enviroment = get_enviroment(group_id)
	if enviroment.error_code:
		return enviroment

	if not varible_name in enviroment.value:
		return  APIResponse(message="Unknown varible name: %s" % varible_name, error_code=1)

	if not type(varible.value) is type(value): 
		return APIResponse("Varible type must be %s but you use %s" % (type(varible.value), type(value)), error_code=1)

	enviroment.value[varible_name] = value
	
	env_set_status = set_enviroment(group_id, enviroment.value)
	if env_set_status.error_code:
		return env_set_status

	return APIResponse(message="ok")

def delete_varible(group_id, varible_name):
	enviroment = get_enviroment(group_id)
	if enviroment.error_code:
		return enviroment

	if not varible_name in enviroment.value:
		return APIResponse(message="Unknown varible name: %s" % varible_name, error_code=1)

	enviroment.value.pop(varible_name)
	set_env_status = set_enviroment(group_id, enviroment.value)
	if set_env_status.error_code:
		return set_env_status

	return APIResponse(message="ok")
