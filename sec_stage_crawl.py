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
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

dataframe = {"Num of experience": [], "Position": [], "Job requirements": []}

df_old = pd.read_excel("job.xlsx")
urls = df_old["URL"].to_list()

for url in tqdm(urls):
  req = driver.get(url)
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  job_info = soup.find_all(
          "div", {"class": "detail-box has-background"})
  try:
    job_info_break = job_info[1].ul.find_all("li")
  except Exception:
    pass

  try:
    dataframe["Num of experience"].append(re.sub(' +', ' ', job_info_break[1:-1][0].p.text.replace("\n", "").strip()))
  except Exception:
    dataframe["Num of experience"].append("")
  
  try:
    dataframe["Position"].append(re.sub(' +', ' ', job_info_break[1:-1][1].p.text.replace("\n", "").strip()))
  except Exception:
    dataframe["Position"].append("")
  
  try:
    job_req = soup.find_all(
            "div", {"class": "detail-row"})
    dataframe["Job requirements"].append(job_req[2])
  except Exception:
    dataframe["Job requirements"].append("")
    
  df = pd.DataFrame(dataframe)
  df.to_excel("job_info.xlsx")   
  
