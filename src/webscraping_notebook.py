# %%
# https://www.google.com/search?q=what&tbm=isch

#! This code is suitable for downloading thumpnail images from google search

import requests
from bs4 import BeautifulSoup
import csv
import cv2
import numpy as np
import re
import pandas as pd
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import os
from PIL import Image
import time
import random

# %%
class google_webscraping:
    def __init__(self, path: str, query: str, total_img: int) -> None:
        self.GOOGLE_BASE: str = "https://www.google.com"
        self.query: str = query
        self.total_img: int = total_img
        self.IMG_PER_PAGE: int = 20
        self.BASE_PATH = os.getcwd()
        if not os.path.exists(path):
            # assert False, "Path does not exist"
            os.makedirs(path, exist_ok=True)
        self.path: str = path
        os.chdir(os.path.join(os.getcwd(), self.path))

    def close(self):
        os.chdir(self.BASE_PATH)

    def start(self):
        # 1 page has 20 images

        procs = []
        pool = ThreadPool(processes=cpu_count())
        for start_index in range(0, self.total_img, self.IMG_PER_PAGE):
            # print(name)
            proc = pool.apply_async(self.run, args=(start_index,))
            procs.append(proc)
            # time.sleep(0.2)

        # complete the processes
        for proc in procs:
            proc.get()

    def run(self, start_index):
        search_url: str = self.get_search_url(self.query, start_index)
        soup: BeautifulSoup = self.get_soup(search_url)
        image_urls: list = self.get_image_urls(soup)[:self.total_img]
        self.download_images(image_urls)

    def download_images(self, image_urls: list) -> None:
        for url in image_urls:
            response: requests.Response = requests.get(url)
            if response.status_code == 200:
                img = cv2.imdecode(np.frombuffer(
                    response.content, np.uint8), cv2.IMREAD_UNCHANGED)
                cv2.imwrite(filename=self.query+'_' +
                            url.split(':')[-1]+'.png', img=img)
                # print("DOWNLOADED", url, os.path.join(
                #     self.path, self.query+'_'+url.split(':')[-1]+'.png'))
            else:
                print("FAILED", url)
            # time.sleep(0.1)
            # print(url)
            # print(response.status_code)
            # print(len(response.text))
        # print(os.listdir('.'))

    def get_soup(self, url: str) -> BeautifulSoup:
        response: requests.Response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def get_image_urls(self, soup: BeautifulSoup) -> list:
        image_urls: list = []
        for img in soup.find_all("img"):
            if img.has_attr("src"):
                if not img["src"].startswith("http"):
                    continue
                image_urls.append(img["src"])
        return image_urls

    def get_search_url(self, query: str, start_index: int) -> str:
        return self.GOOGLE_BASE + "/search?q={query}&tbm=isch&start={start_index}".format(query=query, start_index=start_index)

def indexOf(arr, item):
    try:
        return arr.index(item)
    except:
        return -1
# %%
# web = google_webscraping(path="pirate_ship_images", query="pirate ship", total_img=2000)

# arr = []
# for start_index in range(0, web.total_img, web.IMG_PER_PAGE):
#     arr.append(web.get_image_urls(web.get_soup(web.get_search_url("pirate ship", start_index))))
    
# # np_arr = np.array(arr).flatten().tolist()
# np_arr = [item for sublist in arr for item in sublist]

# for i in np_arr:
#     # print(i)
#     loca_arr = list(filter(lambda k: i in k, arr))
#     if len(loca_arr) > 1:
#         print(i, len(loca_arr))
#     while indexOf(np_arr,i) != -1:
#         np_arr.remove(i)
#     np_arr.append(i)

# print(len(np_arr))

#! found out that google will sent same image url if we want too many imges

# # %%
total_img = 200
path = "images-small"
query = "pirate ship"

# print('single-threading')
# print("Starting...")
# start = time.time()
# web = google_webscraping(path=path,
#                          query=query, total_img=total_img)
# for start_index in range(0, web.total_img, 20):
#     web.run(start_index)
# old = time.time()-start
# print("Time taken [s]:", old)
# print(len(os.listdir('.')))
# web.close

print('multi-threading')
print("Starting...")
start = time.time()
web = google_webscraping(path=path,
                         query=query, total_img=total_img)
web.start()
new = time.time()-start
print("Time taken [s]:", new)
print(len(os.listdir('.')))
web.close()


# print("Speedup [เท่าตัว]:", old/new)
# print("Average Time per image old [s]:", old/total_img)
print("Average Time per image new [s]:", new/total_img)
# print("Faster time per image [s]:", (old-new)/total_img)

# %% [markdown]
#
