
import os
import time
import random
import spintax
import requests
#import config
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, randrange
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM

#from selenium_stealth import stealth


PROXY = "3.88.169.225:80"


def stop(n):
    time.sleep(randint(2, n))

# login bot===================================================================================================


def youtube_login(email, password):

    
    
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
 
# Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
 
# Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 
 
# Setting the driver path and requesting a page 
    
    driver = webdriver.Chrome(options=options)
    
    useragentarray = [ 
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
] 

    for i in range(len(useragentarray)): 
	# Setting user agent iteratively as Chrome 108 and 107 
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragentarray[i]}) 
        print(driver.execute_script("return navigator.userAgent;")) 
        driver.get("https://www.httpbin.org/headers") 
	
    
    
    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    
    driver.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=20&ct=1706748464&rver=7.0.6738.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26nlp%3d1%26deeplink%3dowa%252f%26RpsCsrfState%3de44656e1-6c09-fa35-df08-06fa09a944d2&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c')
    
    time.sleep(3)


    signin = driver.find_element_by_id("i0116")

    signin.send_keys("brynnbates@outlook.com")

    signin.send_keys(Keys.ENTER)

    time.sleep(2)

    passw = driver.find_element_by_id("i0118")

    passw.send_keys("Greanday312312312312")

    passw.send_keys(Keys.ENTER)

    time.sleep(2)

    driver.find_element_by_id("acceptButton").click()

    print("Enter")




# running bot------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("imported")

def default(a, b):
    email = "312whoami312@gmail.com" 
    password = "Greanday312"

    driver = youtube_login(email, password)

