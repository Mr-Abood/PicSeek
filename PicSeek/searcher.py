import requests, base64, re
from typing import List, TypeVar
from .utils import Task

T = TypeVar('T', bound=Task)

class Flickr:
	def __init__(self):
		self.__client = requests.Session()
		self.__client.headers = {
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Safari/537.36'
		}
		self.__get_skeys()
	
	def __get_skeys(self):
		res = requests.get("https://www.flickr.com/search/?text=house").text
		self.__reqId = re.search(r'flickr\.request\.id\s*=\s*"([^"]+)"', res).group(1)
		self.__api_key = re.search(r'flickr\.api\.site_key\s*=\s*"([^"]+)"', res).group(1)
		
	def search(self, text: str, page: int, per_page: int=25) -> List[T]:
		if not isinstance(text, str) or not isinstance(page, int) or not isinstance(per_page, int): return []
		url = "https://api.flickr.com/services/rest"
		params = {
			"sort": "relevance",
			"parse_tags": "1",
			"content_types": "0,1,2,3",
			"video_content_types": "0,1,2,3",
			"extras": "can_comment,can_print,count_comments,count_faves,description,isfavorite,license,media,needs_interstitial,owner_name,path_alias,realname,rotation,url_sq,url_q,url_t,url_s,url_n,url_w,url_m,url_z,url_c,url_l",
			"per_page": str(per_page),
			"page": str(page),
			"lang": "en-US",
			"text": text,
			"viewerNSID": "",
			"method": "flickr.photos.search",
			"csrf": "",
			"api_key": self.__api_key,
			"format": "json",
			"hermes": "1",
			"hermesClient": "1",
			"reqId": self.__reqId,
			"nojsoncallback": "1"
		}
		response = self.__client.get(url, params=params).json()
		if response["stat"] == "fail" and int(response["code"]) == 100:
			self.__get_skeys()
			return self.search(text, page, per_page)
		elif response["stat"] == "fail": return []
		return [Task(img[[key for key in list(img) if key.startswith("url_") and key in ["url_c", "url_l", "url_m", "url_z", "url_w"]][-1]]) for img in response["photos"]["photo"]]


class IStock:
	def __init__(self):
		self.__client = requests.Session()
		self.__client.headers = {
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Safari/537.36',
			'accept': 'application/json'
		}
	
	def search(self, text: str, page: int) -> List[T]:
		if not isinstance(text, str) or not isinstance(page, int): return []
		url = "https://www.istockphoto.com/search/2/image"
		params = {
			"page": str(page),
			"phrase": text
		}
		response = self.__client.get(url, params=params).json()
		if not "gallery" in response: return []
		return [Task(img["thumbUrl"]) for img in response["gallery"]["assets"]]