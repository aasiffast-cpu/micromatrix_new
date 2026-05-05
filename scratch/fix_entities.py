import html
import os

file_path = r'c:\Users\CC\Desktop\new updationsss\micromatrix_new\login.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

fixed_content = html.unescape(content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"Successfully fixed entities in {file_path}")
