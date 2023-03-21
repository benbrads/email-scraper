import random
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
import time
import re
import os

def scrape_site_for_facebook(url): 
    facebook_link = ""
    #Check whether site is facebook already
    if "facebook" in url:
       return ""
    #Else, find facebook link from site
    business_site = requests.get(url)
    business_soup = BeautifulSoup(business_site.content, "html.parser")
    links = business_soup.find_all('a')
    
    #Use selenium if site is JS
    if(len(links) <= 0):
        chrome_options = Options()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('start-maximized')
        driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body")))
        plain_text = driver.page_source
        business_soup = BeautifulSoup(plain_text, 'html.parser')
        links = business_soup.find_all('a')
        driver.quit()
        print("Selenium Link Path")
    #from links, find one to facebook.
    for link in links:
        if "href" in link.attrs:
            if "facebook" in link['href']:
                facebook_link = link['href']
    print(facebook_link)
    return facebook_link

def scrape_site_for_email(url):
    print("Scrape Site Path")
    #Else, find facebook link from site
    business_site = requests.get(url)
    site_email = ""
    business_soup = BeautifulSoup(business_site.content, "html.parser")
    text = business_soup.findAll(string = True)
    for line in text:
        email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
        if(len(email) > 0):
            site_email = email[0]
    return site_email


        
def parse_facebook_for_email(url):
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('start-maximized')
    driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body")))
    except TimeoutException:
        print('TIME OUT')
        driver.quit()
    plain_text = driver.page_source
    print(plain_text)
    no_newline = plain_text.strip('\n')
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", no_newline)
    driver.quit()
    if(email):
        return email[0]
    else:
        return ""