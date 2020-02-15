from os import walk
import shutil
import re

(_, _, filenames) = next(walk('.'))
filtered = [y for y in filenames if y.endswith('.html')]

print("Generating site...")
for filt in filtered:
    print(f"..Generating page '{filt}'")
    with open(filt, 'r') as f:
        replaced_text = f.read()
        matches = re.findall('<{(.*?)}/>', replaced_text)
        for m in matches:
            with open(f'{m}.g', 'r') as rep:
                replace_with = rep.read()
                print(f"....Replacing part '{m}' with content in '{m}.g'")
                replaced_text = replaced_text.replace('<{' + m + '}/>', replace_with)
        
        print(f"..Generated page '{filt}'")
        with open(f'docs-generated/{filt}', 'w+') as new_f:
            new_f.write(replaced_text)
        print(f"..Page '{filt}' saved to /docs-generated/{filt}")

print("..Overwriting assets folder in /docs-generated")
shutil.copytree('assets', 'docs-generated/assets', ignore=shutil.ignore_patterns('*.*~', '*.swp'), dirs_exist_ok=True)
print("Success!")
