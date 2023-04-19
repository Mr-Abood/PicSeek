import base64, requests

class Task:
	def __init__(self, link):
		self.__link = link
		self.__content = None
	
	@property
	def content(self):
		if self.__content is None: self.__content = requests.get(self.__link).content
		return self.__content
	
	@property
	def base64(self):
		if self.__content is None: self.__content = requests.get(self.__link).content
		return base64.b64encode(self.__content)
	
	@property
	def link(self):
		return self.__link
	
	def save(self, filename):
		if self.__content is None: self.__content = requests.get(self.__link).content
		with open(filename, "wb") as f: f.write(self.__content)