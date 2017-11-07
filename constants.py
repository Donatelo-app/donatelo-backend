VIEWS = {
	"text": {"id": str,
		      "value": str,
		      "x": int,
		      "y": int,
		      "w": int,
		      "h": int,,
		      "font": str, 
		      "italic": bool,
		      "bold": bool,
		      "angle": float
		      },

	"image": {"id": str,
		      "value": str,
		      "x": int,
		      "y": int,
		      "w": int,
		      "h": int,
		      "angle": float
		      },

	"linear": {"id": str,
	      "value": str,
	      "max_value": float,
	      "x": int,
	      "y": int,
	      "w": int,
	      "h": int,
	      "angle": float,
	      "border": int,
	      },

	"radial": {"id": str,
	      "value": str,
	      "max_value": float,
	      "x": int,
	      "y": int,
	      "w": int,
	      "h": int,
	      "angle": float,
	      "start_angle": float,
	      "direction": int,
	      "border": int
	      }
}

RESOURCES = {
	"text": [],
	"image": ["image"],
	"linear": ["bar", "stand"],
	"radial": ["bar", "stand"]
}