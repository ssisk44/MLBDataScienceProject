from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import numpy as np
import time, os


def main():
    getPlayer()
    BBREF_cleaned_toCSV('bryceharper_standard_batting.csv')

def get_csv_bbref(link_list):
    chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver

    soup_list = []
    for i in link_list:
        driver = webdriver.Chrome(chromedriver)
        driver.maximize_window()
        driver.get(i)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 500);")
        e1 = driver.find_element_by_xpath('//*[@id="all_batting_standard"]/div[1]/div/ul/li[3]')
        e2 = driver.find_element_by_xpath('//*[@id="batting_standard_sh"]/div/ul/li[3]/div/ul/li[4]/button')
        time.sleep(2)

        action = ActionChains(driver)
        action.move_to_element(e1).perform()
        action.move_to_element(e2).click().perform()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        crude = soup.find('pre', id='csv_batting_standard')
        soup_list.append(crude)
        driver.close()
    return soup_list


def getPlayer():
    bharperstats_list = ["https://www.baseball-reference.com/players/h/harpebr03.shtml"]
    raw_csv_data_list = get_csv_bbref(bharperstats_list)

    ############# PARSE THIS CANCER #############
    df = pd.DataFrame(raw_csv_data_list)
    df.to_csv(r'bryceharper_standard_batting.csv', index=False)



def BBREF_cleaned_toCSV(file):
    df = pd.read_csv(file).to_numpy()
    arr = df[0][2].split('\n')
    arr.remove('')

    newarr = []
    for i in range(0, len(arr)):
        newarr.append(arr[i].split(','))
    header = newarr[0]
    pd.DataFrame(newarr[1:]).to_csv(file, index=False, header=header)



main()


