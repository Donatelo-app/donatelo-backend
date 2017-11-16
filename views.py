import subprocess
import json
import os

from app import app
import base
from utils import get_missing_fields
import vk_utils
import render

from flask import request

def api_result(result, is_error):
	if is_error:
		result = {"code":"error", "message":result, "result":{}}
		result = json.dumps(result)

		return result, 200
	else:
		result = {"code":"ok", "message":"ok", "result":result}
		result = json.dumps(result)

		return result, 200

@app.route("/")
def index():
	return "hello world", 200


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


@app.route("/update_cover", methods=["POST"])
def update_cover():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id", "resources", "views"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	result, code = base.set_cover(data["group_id"], data["views"], data["resources"])
	if not code: return api_result(result, True)	

	process = subprocess.Popen("python %s%supdate_script.py %s" % (os.getcwd(), os.sep, data["group_id"]))

	return api_result("", False)

@app.route("/get_cover", methods=["POST"])
def get_cover():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id"]

	result, code = base.get_cover(data["group_id"])
	if not code: return api_result(result, True)	

	return api_result(result, False)



@app.route("/get_varible", methods=["POST"])
def create_varible():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id", "access_token"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)



@app.route("/get_varible", methods=["POST"])
def get_varible():
	return "ok", 200


@app.route("/set_varible", methods=["POST"])
def set_varible():
	return "ok", 200


@app.route("/group_exist", methods=["POST"])
def group_exist():
	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["group_id"]

	group_existing = base.is_group_exist(data["group_id"])

	return api_result(group_existing, False)


def update_cover(group_id):
	result, code = base.get_access_token(group_id)
	if not code:
		return result, code

	access_token = result
	cover = base.get_cover_image(group_id)
	
	vk_utils.update_cover(group_id, access_token, cover)

	return "ok", True