from constants import VIEWS

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




