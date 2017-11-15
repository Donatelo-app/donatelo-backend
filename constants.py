VIEWS = {
	"text": {"id": str,
			  "type": str,
		      "value": str,
		      "x": int,
		      "y": int,
		      "size":int,
		      "font": str, 
		      "angle": float,
		      "color": str,
		      },

	"image": {"id": str,
			  "type": str,
		      "value": str,
		      "x": int,
		      "y": int,
		      "w": int,
		      "h": int,
		      "angle": float
		      },

	"linear": {"id": str,
		  "type": str,	
	      "value": str,
	      "max_value": float,
	      "x": int,
	      "y": int,
	      "w": int,
	      "h": int,
	      "angle": float,
	      "border": int,
	      "color": str
	      },

	"radial": {"id": str,
		  "type": str,
	      "value": str,
	      "max_value": float,
	      "x": int,
	      "y": int,
	      "w": int,
	      "h": int,
	      "angle": float,
	      "start_angle": float,
	      "direction": int,
	      "border": int,
	      "color": str
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