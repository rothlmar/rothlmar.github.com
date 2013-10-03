import os, yaml, bs4, re, markdown2

def load_files(post_dir=os.curdir):
    posts = {}
    files = [post_dir + '/' + filename for filename in list(os.walk(post_dir))[0][2]]
    for post in files:
        with open(post) as f:
            posts[post] = f.read()
    return posts

def split_posts(posts):
    modified_posts = []
    for title,post in posts.items():
        pd = {}
        pd['title'] = title
        pd['yaml_part'] = post[:post.index('---',10)]
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
                                  


if __name__ == "__main__":
    posts = load_files()
    # mod_posts = split_posts(posts)
    do_slideshow(posts)
