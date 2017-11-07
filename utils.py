from constants import VIEWS, RESOURCES

def generate_resource_id(group_id, view_id, resource_name):
	reutrn "%s:%s:%s" % (group_id, view_id, resource_name)

def validate_cover(cover):
	views = cover.get("views")

	if not type(views) is list:
		return "Field views must be list type, but you use %s" % type(cover.get("views")), False

	for i, view in enumerate(views):
		message, code = validate_view(view)
		if not code:
			return "view[%s]: %s" % (i, message), False

def validate_view(view):
	if not view.get("type") in VIEWS:
		return "Unknown view type", False

	view_format = VIEWS[cover["type"]]


	extra_fields = set(view.keys()) - set(view_format.keys())
	if extra_fields:
		return "Unknown fields :%s" % (str(extra_fields)), False

	missing_fields = set(view_format.keys()) - set(view.keys())
	if missing_fields:
		return "Missing fields :%s" % (str(missing_fields)), False

	for field_type, field_name in view_format.items():
		this_type = type(view[field_name])
		if not field_type is this_type:
			return "Field '%s' must be %s type, but you use %s" % (field_name, field_type, this_type), False

	return "ok", True


def validate_resources(group_id, new_views, old_views, resources):
	this_resources = set(resources.keys())

	old_resources = set()
	for view in old_views:
		for resource_name in RESOURCES[view["type"]]:
			res_id = generate_resource_id(group_id, view["id"], resource_name)
			old_resources.add(res_id)

	new_resources = set()
	for view in new_views:
		for resource_name in RESOURCES[view["type"]]:
			res_id = generate_resource_id(group_id, view["id"], resource_name)
			new_resources.add(res_id)

	extra_resources = this_resources-new_resources
	if extra_resources:
		return "Unknown resources: %s" %s (str(extra_resources)), False

	missing_resources = (new_resources - old_resources) - this_resources
	if missing_resources:
		return "Missing resources :%s" % (str(missing_resources)), False

	#### Check for types ####

	return True
