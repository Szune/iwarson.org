import shutil
print("Updating site ...")
print("..Removing old version")
try:
    shutil.rmtree("docs/")
except e:
    print(f"Exiting: Failed to remove docs/\n{e}")
    raise SystemExit


print("..Overwriting docs/")
shutil.copytree('docs-generated/', 'docs', ignore=shutil.ignore_patterns('*.*~', '*.swp'), dirs_exist_ok=True)
print("..Writing CNAME")
with open('docs/CNAME', 'w+') as f:
    f.write("www.iwarson.org")
print("..Copying favicon.ico")
shutil.copyfile('favicon.ico', 'docs/favicon.ico')
print("Success!")
