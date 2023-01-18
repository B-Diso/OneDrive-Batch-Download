from pathlib import Path
import requests
from requests_ntlm import HttpNtlmAuth
from multiprocessing.dummy import Pool
from tqdm import tqdm
from time import time


def download_files(url):
    onedrive_url = 'https://<hostname>/sites/<site collection title>/_layouts/15/download.aspx?SourceUrl='

    username = 'username'
    password = 'password'

    session = requests.Session()
    # disable security certificate check in Python requests
    session.verify = False

    # Make sure blank at the end of urls not processed
    if len(url) == 0:
        return "Line Kosong!"

    # Create directory for downloaded file
    # I'm using Windows, don't judge me...
    directory = url.split("/")
    download_path = '\\'.join(directory[:-1])
    Path(download_path).mkdir(parents=True, exist_ok=True)

    # Actually download the file
    session.auth = HttpNtlmAuth(username, password)
    response = session.get(onedrive_url + '/' + url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'})  # Less suspicious for IT guys...

    global total_download
    # Log Total Downloaded files
    if response.status_code == 200:
        total_download += 1

    # Save file to disk
    with open('.\\' + url.replace('/', '\\'), 'wb') as f:
        f.write(response.content)
        f.close()
    # print(f"selesai download {directory[-1]}")


if __name__ == '__main__':
    total_download = 0
    t0 = time()
    urls = open("url.txt", "r", encoding="utf-8").read().split('\n')

    for _ in tqdm(Pool().imap_unordered(download_files, urls), total=len(urls)):
        pass

    print(f"{total_download} files berhasil diunduh!")
    print('Total time:', time() - t0)
