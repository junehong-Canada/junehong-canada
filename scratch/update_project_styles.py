import os
import re

projects_dir = r"c:\Project\AIoT\junehong-dominicus.github.io\projects"
style_link = '  <link rel="stylesheet" href="../style.css">'

for filename in os.listdir(projects_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(projects_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remove <style>...</style>
        new_content = re.sub(r"  <style>.*?</style>", style_link, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"Skipped {filename} (no style block found or already updated)")
