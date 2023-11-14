"""
                        _oo0oo_
                       o8888888o
                       88" . "88
                       (| -_- |)
                       0\  =  /0
                     ___/`---'\___
                   .' \|     |// '.
                  / \|||  :  |||// \
                 / _||||| -:- |||||- \
                |   | \\  -  /// |   |
                | \_|  ''\---/''  |_/ |
                \  .-\__  '-'  ___/-. /
              ___'. .'  /--.--\  `. .'___
           ."" '<  `.___\_<|>_/___.' >' "".
          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
          \  \ `_.   \_ __\ /__ _/   .-` /  /
      =====`-.____`.___ \_____/___.-`___.-'=====
                        `=---='
"""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

dataframe = {"Job Title": [], "Location": [], "Salary": [], "URL": []}

for i in tqdm(range(58)):
    url = f"https://careerbuilder.vn/viec-lam/Marketing-tai-ha-noi-kl4,8,511s3-trang-{i+1}-vi.html"
    req = driver.get(url)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_tags = soup.find_all(
        "div", {"class": "job-item"})
    for tag in job_tags:
        job_info = tag.find(
            "a", {"class": "job_link"})
        salary = tag.find(
        "div", {"class": "salary"})
        location = tag.find(
        "div", {"class": "location"})
        dataframe["Job Title"].append(job_info["title"])
        dataframe["URL"].append(job_info["href"])
        dataframe["Location"].append(location.ul.li.text)
        dataframe["Salary"].append(salary.p.text)

    print(len(dataframe["URL"]))
df = pd.DataFrame(dataframe)
df.to_excel("job.xlsx")   