from PIL import Image
import requests
import json

def iiif_manifest(urn):
    r = requests.get("https://api.nb.no/catalog/v1/iiif/{urn}/manifest".format(urn=urn))
    return r.json()


def search_urns(term):
    """Find all urns as customized thumbnails"""
    
    return picture_urns(super_search(term))

def super_search(term, number=50, page=0):
    """Søk etter term og få ut json"""
    number = max(number, 50)
    r = requests.get(
        "https://api.nb.no:443/catalog/v1/search", 
         params = {
             'q':term, 
             'filter':'mediatype:bilder', 
             'page':page, 
             'size':number
         }
    )
    return r.json()
 
def picture_urns(json):
    """From result of super_search, to be fed into iiif_manifest"""

    urns = [
        f['metadata']['identifiers']['urn'] 
        for f in  json['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items'] 
        if 'urn' in f['metadata']['identifiers']
    ]
    return urns

def picture_urls(json_from_super_search, size=200):
    """generates urls from super_search"""
    
    urls = [
        f['_links']['thumbnail_custom']['href'].format(width=0, height=size) 
        for f in json_from_super_search['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items'] 
        if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
        and 'thumbnail_custom' in f['_links']
    ]
    
    return urls

def load_picture(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content=True
    #print(r.status_code)
    return r.raw

def find_picture(term):
    x = super_search(term)
    urns = [
        f['metadata']['identifiers']['urn'] 
        for f in  x['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items'] 
        if 'urn' in f['metadata']['identifiers']
    ]
    found = [get_manifest(urn) for urn in urns]
    
    return [p['sequences'][0]['canvases'][0]['images'][0]['resource']['@id'] for p in found]

picture_url = lambda pics, item = 0, width=400: picture_urls(pics,200)[item]

picture_search = lambda term, size=200: picture_urls(super_search(term, size))

def show_picture(pictures, number=0, size=500):
    return Image.open(load_picture(picture_url(pictures, number, size)))