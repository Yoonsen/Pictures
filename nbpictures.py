from PIL import Image
import requests
import json

def get_manifest(urn):
    r = requests.get("https://api.nb.no/catalog/v1/iiif/{urn}/manifest".format(urn=urn))
    return r.json()

def super_search(term):
    r = requests.get("https://api.nb.no:443/catalog/v1/search", params = {'q':term, 'filter':'mediatype:bilder'})
    return r.json()

def load_picture(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content=True
    #print(r.status_code)
    return r.raw

def find_picture(term):
    x = super_search(term)
    urns = [f['metadata']['identifiers']['urn'] for f in  x['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items'] if 'urn' in f['metadata']['identifiers']]
    found = [get_manifest(urn) for urn in urns]
    return [p['sequences'][0]['canvases'][0]['images'][0]['resource']['@id'] for p in found]

picture_url = lambda result, i, size: result['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items'][i]['_links']['thumbnail_custom']['href'].format(width=0, height=size)