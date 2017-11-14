from jinja2 import Template
from render.draw import *

BACKGROUND_SIZE = (1280, 364)

def render_cover(views, resources, enviroment):
	background = resources["background"].resize(BACKGROUND_SIZE)

	for view in views:
		if view["type"] == "text":
			value = Template(view["value"]).render(**enviroment)
			text = draw_text(value, view["font"],view["size"], color_code=view["color"])
			text = rotate_image(text, view["angle"])
			background = paste_image(text, background, (view["x"], view["y"]))

		if view["type"] == "linear":
			value = enviroment.get(view["value"], 0)/view["max_value"]*100//1
			
			bar = resources["%s:bar" % view["id"]] 
			stand = resources.get("%s:stand" % view["id"])
			
			linear = draw_progress_bar(bar, stand, view["border"], value)
			linear = linear.resize((view["w"], view["h"]))
			linear = rotate_image(linear, view["angle"])
			background = paste_image(linear, background, (view["x"], view["y"]))
		
		if view["type"] == "radial":
			value = enviroment.get(view["value"], 0)/view["max_value"]*100//1
			
			bar = resources["%s:bar" % view["id"]] 
			stand = resources.get("%s:stand" % view["id"])
			 
			radial = draw_radial(bar, stand, view["border"], view["start_angle"], value)
			radial = radial.resize((view["w"], view["h"]))
			radial = rotate_image(radial, view["angle"])
			background = paste_image(radial, background, (view["x"], view["y"]))

		if view["type"] == "image":
			img = resources["%s:image" % view["id"]]
			img = img.resize((view["w"], view["h"]))
			img = rotate_image(img, view["angle"])
			background = paste_image(img, background, (view["x"], view["y"]))

	return background