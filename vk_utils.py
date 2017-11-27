from io import BytesIO
import vk_api
from vk_api import VkUpload

def update_cover(group_id, access_token, cover):
	img = BytesIO()
	cover.save(img, format="png")
	img.seek(0)

	vk_session = vk_api.VkApi(token=access_token)
	upload = vk_api.VkUpload(vk_session)

	photo = upload.photo_cover(img, group_id=group_id, crop_x2 = cover.size[0], crop_y2 = cover.size[1])

def get_viewer_mode(viewer_id):
	pass