import re
import os
from sample.filedown import filedown

dir_path = os.path.join(os.getcwd(), '../loot/Queen')
os.makedirs(dir_path, exist_ok=True)

with open('../assets/queens-blade.txt', 'r') as f_in:
    url_list = f_in.readlines()

os.chdir(dir_path)

for url in url_list:
    filename = 'Queens-Blade-' + re.search(r"(?<=201_)(\d+\.jp2)(?=&id)", url).group()
    filedown(url, filename)
