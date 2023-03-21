from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
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
        ua = UserAgent()
        user_agent = ua.random
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        driver.set_window_size(1440,900)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body")))
        plain_text = driver.page_source
        business_soup = BeautifulSoup(plain_text, 'html.parser')
        links = business_soup.find_all('a')
    #from links, find one to facebook.
    for link in links:
        if "href" in link.attrs:
            if "facebook" in link['href']:
                facebook_link = link['href']
    return facebook_link

def scrape_site_for_email(url):
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
    ua = UserAgent()
    user_agent = ua.random
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f'user-agent={user_agent}')


    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    driver.set_window_size(1440,900)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body")))
    plain_text = driver.find_element(By.XPATH, "/html/body").text
    print(plain_text)
    no_newline = plain_text.strip('\n')
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", no_newline)
    if(email):
        return email[0]
    else:
        return ""