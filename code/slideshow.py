import os, yaml, bs4, re, markdown2, codecs

def load_files(post_dir=os.curdir):
    posts = {}
    files = [post_dir + '/' + filename for filename in list(os.walk(post_dir))[0][2]]
    for post in files:
        with codecs.open(post,'r','utf-8') as f:
            posts[post] = f.read()
    return posts

def split_posts(posts):
    modified_posts = []
    for title,post in posts.items():
        pd = {}
        pd['title'] = title
        pd['yaml_part'] = post[:post.index('---',10)]
        pd['yaml'] = yaml.load(pd['yaml_part'])
        pd['content'] = post[post.index('---',10) + 3:]
        pd['soup'] = bs4.BeautifulSoup(pd['content'])
        modified_posts.append(pd)
    return modified_posts

def do_slideshow(posts):
    ss_posts = dict([i for i in posts.items() if '[slideshow]' in i[1]])
    attachments = list(os.walk('../_attachments'))[0][2]
    for key in ss_posts.keys():
        ss_posts[key] = ss_posts[key].replace('[slideshow]','{% include slideshow.html %}')

    for key in ss_posts.keys():
        split_title = key.split('-')
        year = split_title[0][2:]
        month = split_title[1]
        tot_date = key[2:12]
        print(tot_date, year, month)
        images = [a.split('-')[-1].split('.')[0] for a in attachments if tot_date in a]
        print(images)
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

def fix_floats(main_part):
    def fixit(trigger,replacement):
        to_fix = main_part.findAll('div',attrs={"style":re.compile(trigger)})
        for item in to_fix:
            item.attrs["class"] = replacement
            del item.attrs['style']

    fixit("float:left","alignleft")
    fixit("float:right","alignright")

def aligncenter_wrap(main_part):
    centered_images = main_part.findAll('img',{"class":"aligncenter"})
    for img in centered_images:
        parent = img.parent
        parent.wrap(main_part.new_tag("div",**{"class":"aligncenter"}))

# markdown for paragraphs

def wrap_thumbnails(post):
    aligned_images = post['soup'].findAll('img',{"class":re.compile("align(left|right)")})
    for img in aligned_images:
        parent = img.findParent()
        gp = parent.findParent('div')
        if gp:
            print(post['title'],parent,gp)
                                  
def do_videos(post,service='flickr'):
    post['yaml'] = yaml.load(post['yaml_part'])
    video = {}
    flickre = re.compile('\[' + service + '\s+(?:http://vimeo.com/)?(\d+)"?.*?\]')
    # flickre = re.compile('\[' + service + ' video=(\d+)"?.*?\]')
    re_match = flickre.search(post['content'])
    group = re_match.group()
    video['id'] = re_match.groups()[0]
    width = re.search('w=(\d+)',group)
    height = re.search('h=(\d+)',group)
    if width:
        video['width'] = width.groups()[0]
    if height:
        video['height'] = height.groups()[0]
    print(group, video)
    post['yaml']['video'] = video
    post['content'] = flickre.sub('{% include ' + service + 'video.html %}',post['content'])
    write_post(post)

def do_captions(post):
    def re_sub(mo):
        return '<div class="' + mo.groups()[0]+'">' + mo.groups()[2] + '\n<p style="max-width:160px"><em>' + mo.groups()[1] + '</em></p></div>'
    capre = re.compile('\[caption.*?align="(.*?)".*?caption="(.*?)".*?\](.*?)\[/caption\]')    
    re_match = capre.search(post['content'])
    if re_match:
        # print(re_match.groups())
        content = capre.sub(re_sub, post['content'])
        # print(content)
        post['content'] = content
        write_post(post)
    else:
        print(post['title'])


def write_post(post):
    with codecs.open(post['title'],'w','utf-8') as f:
        f.write('---\n')
        f.write(yaml.dump(post['yaml']))
        f.write('\n---\n')
        f.write(post['soup'].prettify())



if __name__ == "__main__":
    posts = load_files()
    # mod_posts = split_posts(posts)
    do_slideshow(posts)
