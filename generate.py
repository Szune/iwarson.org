from os import walk
from pathlib import Path
import shutil
import re

class BlogPost:
    def __init__(self, title, date, file_name):
        self.title = title
        self.date = date
        self.file_name = file_name

class TemplatePart:
    def __init__(self, name, content):
        self.name = name
        self.content = content

class MdSt:
    def __init__(self):
        self.in_block = False

def md_tag(s, tag, tagOp, tagCl):
    s = re.sub(tag, fr'{tagOp}\1{tagCl}', s)
    return s

def md_link_tag(s):
    s = re.sub('\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', s)
    return s

def md_ext_img_tag(s):
    s = re.sub('\?\[(.*?)\]', r'<img class="img-blog" src="\1">', s)
    return s

def md_int_img_tag(s):
    s = re.sub('!\[(.*?)\]', r'<img class="img-blog" src="assets/\1">', s)
    return s

def md_int_img_with_url_tag(s):
    s = re.sub('!!\[(.*?)\]', r'<a href="assets/\1"><img class="img-blog" src="assets/\1"></a>', s)
    return s

def md_block_tag(s, tag, tagVar, st):
    sub = re.subn(tag, tagVar, s)
    if sub[1] > 0:
        st.in_block = not st.in_block
    return sub[0]


def md_replace(s, st):
    last = st.in_block
    if not st.in_block:
        s = md_tag(s, '###\W?(.*?)\W?$', '<h3>','</h3>')
        s = md_tag(s, '##\W?(.*?)\W?$','<h2>','</h2>')
        s = md_tag(s, '#\W?(.*?)\W?$','<h1>','</h1>')
        s = md_tag(s, '\*\*\W?(.*?)\W?\*\*','<b>','</b>')
        s = md_tag(s, '__\W?(.*?)\W?__','<i>','</i>')
        s = md_link_tag(s)
        s = md_int_img_with_url_tag(s)
        s = md_int_img_tag(s)
        s = md_ext_img_tag(s)
        s = md_block_tag(s, '```', '<pre class="blog-pre"><code class="blog-code-block">',st)
        s = md_tag(s, '`\W?(.*?)\W?`', '<code class="blog-code">', '</code>')
    else:
        s = md_block_tag(s, '```', '</code></pre>', st)
    if s.strip() == "":
        return "<br>"
    if last:
        return s + "\n"
    return s

def apply_template(templ, title, content, root = "", date = ""):
    fin = templ.replace("{%TITLE%}", title)
    fin = fin.replace("{%CONTENT%}", content)
    fin = fin.replace("{%DATE%}", date)
    fin = fin.replace("{%ROOT%}", root)
    return fin

def get_page_and_apply_template(templ, s):
    lines = s.splitlines()
    title = md_tag(lines[0], "Title:\W?(.*?)\W?$", "", "")
    date = md_tag(lines[1], "Date:\W?(.*?)\W?$", "", "")
    content = ""
    if lines[2].strip() != "---":
        raise Exception("Misformed page file") 
    for line_num in range(3, len(lines)):
        content += lines[line_num] + "\n"

    fin = apply_template(templ, title, content, "", date)
    return fin


def blog_write(s, templ, blog_posts, file_name):
    st = MdSt()
    lines = s.splitlines()
    title = md_tag(lines[0], "Title:\W?(.*?)\W?$", "", "")
    date = md_tag(lines[1], "Date:\W?(.*?)\W?$", "", "")
    content = ""
    if lines[2].strip() != "---":
        raise Exception("Misformed blog file") 
    for line_num in range(3, len(lines)):
        content += md_replace(lines[line_num], st)

    fin = apply_template(templ, title, content, "../", date)
    blog_posts.append(BlogPost(title, date, file_name))
    return fin

def first_num_sort(s):
    return int(re.findall("(\d+)", s.file_name)[0])

def gen_blog_index(templ, blog_posts):
    # TODO: add pagination if necessary at some point far into the future
    c = len(blog_posts)
    content = '<p><ul class="blog-index">'
    for blog in sorted(blog_posts, key=first_num_sort, reverse=True):
        content += f'<li><a href="{blog.file_name}">{blog.date} - {blog.title}</a> ({c})' 
        c -= 1
    content += '</ul></p>'
    return apply_template(templ, "Blog", content)

def get_files(path, s):
    (_, _, filenames) = next(walk(path))
    return [y for y in filenames if y.endswith(s)]

def read_full(path):
    with open(path, 'r') as f:
        return f.read()

def write_full(path, content):
    with open(path, 'w+') as f:
        f.write(content)

def get_template(path, parts):
    content = read_full(path)
    for part in parts:
        content = content.replace('<{' + part.name + '}/>', part.content)
    return content

print("Initializing ...")
print("..Removing old generated version")
try:
    shutil.rmtree("docs-generated/")
except e:
    print(f"Exiting: Failed to remove docs/\n{e}")
    raise SystemExit
print("..Creating folders")
# make sure folders exist
Path("./docs-generated/blog").mkdir(parents=True, exist_ok=True)
Path("./docs-generated/assets").mkdir(parents=True, exist_ok=True)


templ_part_files = get_files('.', '.templpart')
templ_parts = []

for name in templ_part_files:
    content = read_full(name)
    templ_parts.append(TemplatePart(name.replace('.templpart','').upper(), content))

print("Reading site template...")
site_template = get_template(r'.\site.template', templ_parts)

filtered = get_files('.', '.page')
print("Generating site...")
for name in filtered:
    filt = re.sub('^(.*?).page$', r'\1.html', name)
    print(f"..Generating page '{filt}'")

    replaced_text = read_full(name)
    replaced_text = get_page_and_apply_template(site_template, replaced_text)
    print(f"..Generated page '{filt}'")
    write_full(f'docs-generated/{filt}', replaced_text)
    print(f"..Page '{filt}' saved to /docs-generated/{filt}")

print("Reading blog template...")
blog_template = get_template(r'.\blog.template', templ_parts)

filtered = get_files(r'.\blog', '.blog')

blog_posts = []
print("Generating blog...")
for filt in filtered:
    print(f"..Generating page '{filt}'")
    b_f_name = f'.\\blog\\{filt}'
    replaced_text = read_full(b_f_name)
    replaced_text = blog_write(replaced_text, blog_template, blog_posts, f'{b_f_name}.html')
    print(f"..Generated page '{filt}'")
    write_full(f'docs-generated/blog/{filt}.html', replaced_text)
    print(f"..Page '{filt}' saved to /docs-generated/blog/{filt}.html")


print("Reading blog index template...")
blog_index_template = get_template(r'.\blog-index.template', templ_parts)
print("Generating blog index...")
b_index = gen_blog_index(blog_index_template, blog_posts)
write_full('docs-generated/blog.html', b_index)
print("..Generated blog index")

print("..Overwriting assets folder in /docs-generated")
shutil.copytree('assets', 'docs-generated/assets', ignore=shutil.ignore_patterns('*.*~', '*.swp'), dirs_exist_ok=True)
print("..Overwriting assets folder in /docs-generated/blog")
shutil.copytree('blog/assets', 'docs-generated/blog/assets', ignore=shutil.ignore_patterns('*.*~', '*.swp'), dirs_exist_ok=True)
print("Success!")
