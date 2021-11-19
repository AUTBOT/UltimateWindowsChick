import regex as re
import requests
from tqdm import tqdm


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

text = ""
with open("site.txt", "r") as file:
    text = file.read()

temps = re.findall(r'(?<=\"/).+?(?=\.mp4")', text)
links = ["https://erowall.com/" + x + ".mp4" for x in temps]

for link in tqdm(links):
    download_file(link)
