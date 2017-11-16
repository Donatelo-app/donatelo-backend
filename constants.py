VIEWS = {
	"text": {"id": str,
			  "type": str,
		      "value": str,
		      "x": int,
		      "y": int,
		      "size":int,
		      "font": str, 
		      "angle": int,
		      "color": str,
		      },

	"image": {"id": str,
			  "type": str,
		      "value": str,
		      "x": int,
		      "y": int,
		      "w": int,
		      "h": int,
		      "angle": int
		      },

	"linear": {"id": str,
		  "type": str,	
	      "value": str,
	      "max_value": float,
	      "x": int,
	      "y": int,
	      "w": int,
	      "h": int,
	      "angle": int,
	      "border": int,
	      "stand_color": str,
	      "bar_color": str
	      },

	"radial": {"id": str,
		  "type": str,
	      "value": str,
	      "max_value": float,
	      "x": int,
	      "y": int,
	      "w": int,
	      "h": int,
	      "angle": int,
	      "start_angle": int,
	      "direction": int,
	      "border": int,
	      "stand_color": str,
	      "bar_color": str
	      }
}

RESOURCES = {
	"text": [],
	"image": [],
	"linear": ["bar", "stand"],
	"radial": ["bar", "stand"]
}

VARIBLES_TYPES = {
	"int": 0,
	"str": "",
	"float": 0.0
}