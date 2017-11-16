import sys
import base
import vk_utils
from random import randint

def update_cover(group_id):
	result, code = base.get_access_token(group_id)
	if not code:
		print(result)
		exit()

	access_token = result
	cover = base.get_cover_image(group_id)
	
	cover.save("lol%s.png" % randint(1,100))
	vk_utils.update_cover(group_id, access_token, cover)


if len(sys.argv)<2:
	print("group_id is missing")
	exit()

update_cover(sys.argv[1])