import threading
import json
import os

from app import app
import base
from validation import get_missing_fields
import vk_utils
import render

import services

from flask import request


SECRET_SERVICE_KEY = os.environ["SECRET_SERVICE_KEY"]


# UTILS
def api_result(result, is_error):
	if is_error:
		result = {"code":"error", "message":result, "result":{}}
		result = json.dumps(result)

		return result, 200
	else:
		result = {"code":"ok", "message":"ok", "result":result}
		result = json.dumps(result)

		return result, 200

def update_cover_image(group_id):
	result, code = base.get_access_token(group_id)
	if not code:
		return result, code

	access_token = result
	cover = base.get_cover_image(group_id)
	
	vk_utils.update_cover(group_id, access_token, cover)
	from random import randint

	return "ok", True


## ROUTES
@app.route("/")
def index():
	return "hello world", 200


# VK-APP
@app.route("/create_group", methods=["POST"])
def create_group():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id", "access_token"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	result, code = base.create_group(data["group_id"], data["access_token"])
	if not code: return api_result(result, True)

	return api_result("", False)

@app.route("/edit_token", methods=["POST"])
def edit_token():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id", "access_token"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	result, code = base.edit_token(data["group_id"], data["access_token"])
	if not code: return api_result(result, True)

	return api_result("", False)


@app.route("/get_enviroment", methods=["POST"])
def get_enviroment():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id"]

	result, code = base.get_enviroment(data["group_id"])
	if not code: return api_result(result, True)

	return api_result(result, False)


@app.route("/get_group", methods=["POST"])
def get_group():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id"]

	result, code = base.get_group(data["group_id"])
	if not code: return api_result(result, True)

	return api_result(result, False)

@app.route("/update_cover", methods=["POST"])
def update_cover():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id", "resources", "views"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	result, code = base.set_cover(data["group_id"], data["views"], data["resources"])
	if not code: return api_result(result, True)	

	thread = threading.Thread(target=update_cover_image, args=(data["group_id"],))
	thread.daemon = True
	thread.start()

	return api_result("", False)

@app.route("/group_exist", methods=["POST"])
def group_exist():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id"]

	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	group_existing = base.is_group_exist(data["group_id"])

	return api_result(group_existing, False)

@app.route("/update_service", methods=["POST"])
def update_service():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id", "service_id", "fields"]

	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	result, code = services.update_service(data["group_id"], data["service_id"], data["fields"])	

	if not code:
		return api_result(result, True)

	return api_result("ok", False)

@app.route("/activate_service", methods=["POST"])
def activate_service():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id", "service_id", "activation"]

	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	result, code = services.activate_service(data["group_id"], data["service_id"], data["activation"])	
	if not code:
		return api_result(result, True)

	return api_result("ok", False)
	

# SERVICES
@app.route("/create_varible", methods=["POST"])
def create_varible():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id", "varible_name", "varible_type"]

	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect secret key", True)

	result, code = base.create_varible(data["group_id"], data["varible_name"], data["varible_type"])	
	if not code:
		return api_result(result, True)

	return api_result("ok", False)

@app.route("/get_varible", methods=["POST"])
def get_varible():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id", "varible_name"]

	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect secret key", True)

	result, code = base.get_varible(data["group_id"], data["varible_name"])
	if not code:
		return api_result(result, True)

	return api_result(result, False)

@app.route("/set_varible", methods=["POST"])
def set_varible():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id", "varible_name", "value"]

	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect secret key", True)

	result, code = base.set_varible(data["group_id"], data["varible_name"], data["value"])	
	if not code:
		return api_result(result, True)
		
	return api_result("ok", False)

@app.route("/delete_varible", methods=["POST"])
def delete_varible():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id", "varible_name"]

	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect secret key", True)

	result, code = base.delete_varible(data["group_id"], data["varible_name"])	
	if not code:
		return api_result(result, True)

	return api_result("ok", False)

@app.route("/update_image", methods=["POST"])
def update_image():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id"]

	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect secret key", True)

	thread = threading.Thread(target=update_cover_image, args=(data["group_id"],))
	thread.daemon = True
	thread.start()

	return api_result("ok", False)