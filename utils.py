import re

from constants import VIEWS, RESOURCES, SERVICES

def generate_resource_id(view_id, resource_name):
	return "%s:%s" % (view_id, resource_name)

def get_resources_names_from_view(views):
	resources = ["background"]
	for view in views:
		for resource_name in RESOURCES[view["type"]]:
			res_id = generate_resource_id(view["id"], resource_name)
			resources.append(res_id)
	return resources

def validate_views(views):
	if not type(views) is list:
		return "Views must be list type, but you use %s" % type(views), False

	for i, view in enumerate(views):
		message, code = validate_view(view)
		if not code:
			return "view[%s]: %s" % (i, message), False

	return "ok", True

def validate_view(view):
	if not view.get("type") in VIEWS:
		return "Unknown view type", False

	view_format = VIEWS[view["type"]]


	extra_fields = set(view.keys()) - set(view_format.keys())
	if extra_fields:
		return "Unknown fields :%s" % (str(extra_fields)), False

	missing_fields = set(view_format.keys()) - set(view.keys())
	if missing_fields:
		return "Missing fields :%s" % (str(missing_fields)), False

	for field_name, field_type in view_format.items():
		this_type = type(view[field_name])
		if not field_type is this_type:
			return "Field '%s' must be %s type, but you use %s" % (field_name, field_type, this_type), False

	return "ok", True


def validate_resources(group_id, new_views, old_views, resources):
	this_resources = set(resources.keys())

	is_background_exist = not old_views is None
	if old_views is None:
		old_views = []

	old_resources = set(get_resources_names_from_view(old_views))
	new_resources = set(get_resources_names_from_view(new_views))

	if not is_background_exist:
		old_resources.remove("background")

	extra_resources = this_resources-new_resources
	if extra_resources:
		return "Unknown resources: %s" % (str(extra_resources)), False

	missing_resources = (new_resources - old_resources) - this_resources
	if missing_resources:
		return "Missing resources :%s" % (str(missing_resources)), False

	#### Check for types ####

	return "Ok", True

def get_missing_fields(required_fields, data):
	missing_fields = []
	for field in required_fields:
		if field not in data:
			missing_fields.append(field)


	return missing_fields


def validate_service_form(service_id, form):
	if not service_id in SERVICES:
		return "Unknown service ID", False

	SERVICE = SERVICES[service_id]

	if not type(form) is dict:
		return "Field service_id must be %s, but you use %s" % (dict, type(form)), False

	missing_fields = set(SERVICE["inputs"]) - set(form)
	extra_fields = set(form) - set(SERVICE["inputs"])

	if missing_fields:
		return "Missing fields :%s" % (str(missing_fields)), False

	if extra_fields:
		return "Extra fields :%s" % (str(extra_fields)), False


	for input_id, input_value in form.items():
		if not type(input_value) is str:
			return "Field %s must be %s, but you use %s" % (input_id, str, type(input_value)), False

		regexp = SERVICE["inputs"][input_id]["regexp"]
		result = re.match(regexp, input_value)

		if result is None or result.group(0) != input_value:
			return "Invalid input[%s] format." % (input_id,) , False

	return "ok", True