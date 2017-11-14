from PIL import Image, ImageDraw, ImageFont, ImageColor
from base64 import encodebytes, decodebytes
from io import BytesIO


FONTS = {
    "BEBAS": "Bebas-Regular.ttf",
    "ROBOTO": "Roboto-Regular.ttf"
}

RADIAL_MASK = Image.open("render/radial-mask.png")



def rotate_image(image, angel):
    max_s = int((image.size[0]**2+image.size[1]**2)**0.5)
    canvas = Image.new("RGBA", (max_s, max_s))
    canvas.paste(image, (max_s//2-image.size[0]//2, max_s//2-image.size[1]//2))
    
    return canvas.rotate(angel)


def paste_image(image, background, point, align="center"):
    if align == "center":
        point = point[0]-image.size[0]//2, point[1]-image.size[1]//2
    if align == "right":
        pass

    background.paste(image, point, image)
    
    return background


def draw_progress_bar(bar, stand, border, precent):
    if stand is None: stand = Image.new("RGBA", bar.size)
    
    bar = bar.crop((0,0,bar.size[0]/100*precent, bar.size[1]))

    stand = stand.resize((stand.size[0]+border*2, stand.size[1]+border*2))
    try:
        stand.paste(bar, (border, border), bar)
    except:
        stand.paste(bar, (border, border))
    return stand


def draw_text(text, font_name, size, color_code="#FFFFFFFF"):
    color = ImageColor.getrgb(color_code)
    if len(color)==3: color = tuple(list(color) + [255])
    
    font = ImageFont.truetype('./render/fonts/%s' % FONTS[font_name], size)
    
    image = Image.new('RGBA', font.getsize(text)) 
    ImageDraw.Draw(image).text((0, 0), text, font=font, fill=color)
    
    return image


def draw_radial(image, stand, border, start_angle, percent, direction=1):
    if stand is None: stand = Image.new("RGBA", image.size)
    stand = stand.resize((stand.size[0]+border*2, stand.size[1]+border*2))
    
    mask = Image.new("RGBA", RADIAL_MASK.size)
    
    angle = int(360/100*percent)
    
    if angle>360: angle = 360
    if angle<180:
        mask.paste(RADIAL_MASK.rotate(-angle), (0,0), RADIAL_MASK.rotate(180))
    else:
        mask.paste(RADIAL_MASK.rotate(180), (0,0), RADIAL_MASK.rotate(180))
        mask.paste(RADIAL_MASK.rotate(-angle), (0,0), RADIAL_MASK.rotate(-angle))


    mask = mask.resize(image.size)
    mask = mask.rotate(-start_angle)
    
    if direction<0:
        mask = mask.transpose(Image.FLIP_TOP_BOTTOM)
        
    stand.paste(image, (border,border), mask)
    
    return stand
