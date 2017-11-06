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
		      "angel": float
		      },

	"image": {"id": str,
		      "value": str,
		      "x": int,
		      "y": int,
		      "w": int,
		      "h": int,
		      "angel": float
		      },

	"linear": {"id": str,
	      "value": str,
	      "max_value": float,
	      "x": int,
	      "y": int,
	      "w": int,
	      "h": int,
	      "angel": float,
	      "border": int,
	      },

	"radial": {"id": str,
	      "value": str,
	      "max_value": float,
	      "x": int,
	      "y": int,
	      "w": int,
	      "h": int,
	      "angel": float,
	      "start_angel": float,
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