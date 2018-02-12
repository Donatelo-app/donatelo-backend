import json

class APIResponse:
	def __init__(self, message="ok", value=None, error_code=0):
		self.message = message
		self.value = value
		self.error_code = error_code

	def get_flask_response(self):
		
		if self.error_code:
			return json.dumps(message), 400
		else:
			return json.dumps(value), 200