import os, yaml


files = list(os.walk('.'))
for post in files[0][2]:
    with open(post) as f:
        posts[post] = f.read()

ss_posts = dict([i for i in posts.items() if '[slideshow]' in i[1]])
for key in ss_posts.keys():
    ss_posts[key] = ss_posts[key].replace('[slideshow]','{% include slideshow.html %}')
yaml.parse(ss_posts.items()[0][0])

attachments = list(os.walk('../_attachments'))
attachments = attachments[0][2]

for k,v in ss_posts.items():
    if '{% include ' not in v:
        print(k)

for key in ss_posts.keys():
    split_title = key.split('-')
    year = split_title[0]
    month = split_title[1]
    tot_date = key[:10]
    images = [a.split('-')[-1].split('.')[0] for a in attachments if tot_date in a]
    yaml_part = ss_posts[key][:ss_posts[key].index('---',10)]
    other_part = ss_posts[key][ss_posts[key].index('---',10):]
    image_names = ['"' + a + '.jpg?w=900"' for a in images]
    image_base = 'image_base: http://rothlbaby.files.wordpress.com/{0}/{1}/\n'.format(year,month)
    slideshow_images = 'slideshow_images: [' + ', '.join(image_names) + ']\n'
    with open(key,'w') as f:
        f.write(yaml_part)
        f.write(image_base)
        f.write(slideshow_images)
        f.write(other_part)
