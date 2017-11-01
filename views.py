from app import app


@app.route("/")
def index():
	return "hello world"


@app.route("/create_group")
def create_group():
	return "ok", 200


@app.route("/update_cover")
def update_cover():
	return "ok", 200


@app.route("/update_enviroment")
def update_enviroment():
	return "ok", 200


@app.route("/get_value")
def get_value():
	return "ok", 200


@app.route("/set_value")
def set_value():
	return "ok", 200