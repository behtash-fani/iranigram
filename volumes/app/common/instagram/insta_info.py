from instagpy import InstaGPy, config
from django.conf import settings
from decouple import config
from ensta import Guest
import requests
import json
import os


class InstagramAccInfo:
    def __init__(self) -> None:
        pass

    def get_username_from_link(self, link):
        insta = InstaGPy()
        config.SESSION_DIRECTORY = "Insta Saved Sessions"
        username = config("INSTAGRAM_USER1")
        password = config("INSTAGRAM_PASS1")
        insta.login(username, password)
        insta.logged_in()
        post_url = str(link)
        post_details = insta.get_post_details(post_url)
        if post_details:
            post_details = json.dumps(post_details)
            post_details = json.loads(post_details)
        username = post_details["data"]["shortcode_media"]["owner"]["username"]
        if username:
            return username
        else:
            return None

    def check_acc_is_available(self, username):
        try:
            response = requests.get(f"https://www.instagram.com/{username}")
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
        
    def acc_privacy(self, username):
        guest = Guest()
        try:
            is_private = guest.profile(username).is_private
            print(is_private)
            if is_private is not True:
                return 'acc_public' # this show account in public
            else:
                return 'acc_private' # this show account in private
        except:
            return('There is a problem with Instagram')

    def profile_pic_from_username(self, username):
        guest = Guest()
        instagram_url = guest.profile(username).profile_picture_url
        profile_pic_url = self.save_profile_pic(instagram_url)
        return profile_pic_url

    def profile_pic_from_link(self, link):
        username = self.get_username_from_link(link)
        profile_pic_url = self.profile_pic_from_username(username)
        return profile_pic_url
    
    def save_profile_pic(self, profile_pic_link=None):
        response = requests.get(profile_pic_link)
        file_name = os.path.basename(profile_pic_link.split("?")[0])
        profile_pic_path = os.path.join(settings.MEDIA_ROOT, "profile_pic")
        os.makedirs(profile_pic_path, exist_ok=True)
        file_path = os.path.join(settings.MEDIA_ROOT, "profile_pic", file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)
        profile_pic_url = os.path.join(settings.MEDIA_URL, "profile_pic", file_name)
        return profile_pic_url
