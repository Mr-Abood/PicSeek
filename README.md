# PicSeek

PicSeek is a Python library for searching for images on IStock and Flickr. It provides a simple and easy-to-use interface for accessing these services and retrieving images based on various search parameters.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PicSeek.

```bash
pip install PicSeek==1.0.0
```

## Examples
### Search in Flickr
``` python
from PicSeek import Flickr

flickr = Flickr()

for img in flickr.search(text="cat", page=1, per_page=20):
	print(img.link)
	#print(img.content)
	#print(img.base64)
	#img.save(filename="img.png")
```

### Search in IStock
``` python
from PicSeek import IStock

istock = IStock()

for img in istock.search(text="cat", page=1):
	print(img.link)
	#print(img.content)
	#print(img.base64)
	#img.save(filename="img.png")
```

## Developer
Telegram: [https://t.me/O0O0I](https://t.me/O0O0I)
