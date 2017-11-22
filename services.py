import requests
import os

import base
from utils import validate_service_form
from constants import SERVICES

SECRET_SERVICE_KEY = os.environ["SECRET_SERVICE_KEY"]

def activate_service(group_id, service_id, activation):
	is_group_exist = base.is_group_exist(group_id)
	if not is_group_exist:
		return "Unknown group_id: %s" % group_id, False 

	if not type(activation) is bool:
		return "Field activation must be %s, but you use %s" % (bool, type(activation)), False

	if not service_id in SERVICES:
		return "Unknown service id", False

	service = SERVICES[service_id]

	response = requests.post(service["api_link"]+"/set_activate", json={"group_id": group_id, "activation": activation, "secret_key": SECRET_SERVICE_KEY})
	if response.status_code != 200:
		try:
			return response.json()["message"], False
		except Exception as ex:
			print(ex)
			return "Error in service", False
	
	return response.json(), True

def update_service(group_id, service_id, form):
	is_group_exist = base.is_group_exist(group_id)
	if not is_group_exist:
		return "Unknown group id", False

	result, code = validate_service_form(service_id, form)
	if not code:
		return result, False

	service = SERVICES[service_id]

	response = requests.post(service["api_link"]+"/set_fields", json={"group_id": group_id, "fields": form, "secret_key": SECRET_SERVICE_KEY})
	if response.status_code != 200:
		try:
			return response.json()["message"], False
		except Exception as ex:
			print(ex)
			return "Error in service", False
	
	return response.json(), True
