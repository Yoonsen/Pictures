# Pictures

# Code for searching and downloading thumbnail pictures from the National Library of Norway

Imported resources

```
from PIL import Image
import requests
import json
```

### get_manifest(urn):
Access the IIIF manifest of a picture from its URN. Returns link to full size image.

### super_search(term):
Search a term and get the ten first pictures.

### load_picture(url):
Load a picture from any URL pointing to a downloadable picture.

### find_picture(term):
This function takes a term, and returns the URNs for the pictures.

### picture_url
returns the url for a picture

### show_picture(pictures, number=0, size=500):
return Image.open(load_picture(picture_url(pictures, number, size)))`
