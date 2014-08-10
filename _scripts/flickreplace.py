#! /usr/bin/env python

import sys
import requests, yaml
from numbers import Number

with open(sys.argv[1]) as f:
    _, header, content = f.read().split('---')

header = yaml.load(header)

def id_replace(hdr, prop):
    fmt_str = 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg'
    if hdr.get(prop):
        for idx, val in enumerate(hdr.get(prop)):
            proper_val = None
            if val.endswith('/'):
                proper_val =  val.split('/')[-2]
            elif isinstance(val, Number):
                proper_val = val
            if proper_val is not None:
                params = {'method': 'flickr.photos.getInfo',
                          'api_key': '50ab800ac3ed275e5d441705e5608ce6',
                          'photo_id': proper_val,
                          'format': 'json',
                          'nojsoncallback': 1}
                res = requests.get('https://api.flickr.com/services/rest/',
                                   params=params)
                flickr_resp = res.json()['photo']
                hdr[prop][idx] = fmt_str.format(**flickr_resp)
                
id_replace(header, 'slideshow_images')
id_replace(header, 'images')
                
with open(sys.argv[1],'w') as f:
    f.write('---\n')
    f.write(yaml.dump(header, default_flow_style=False))
    f.write('\n---')
    f.write(content)
