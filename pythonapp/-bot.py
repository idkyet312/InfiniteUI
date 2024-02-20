
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
    
    driver.get('http://instagram.com')
    
    time.sleep(3)
    
    fields = driver.find_elements_by_tag_name("input")
    fields[0].send_keys("312whoami312@gmail.com")
    
    time.sleep(3)
    
    fields[1].send_keys("Greanday312")
    fields[1].send_keys(Keys.ENTER)
    
    time.sleep(3)
    
    i = 1
    
    for i in range(3):
        driver.get('http://google.com')
        
        search_field = driver.find_element_by_id("APjFqb")
        search_field.send_keys("site:instagram.com + “youtuber”")
        search_field.send_keys(Keys.ENTER)
        
        time.sleep(3)
        
        results = driver.find_elements(By.CLASS_NAME,"MjjYud")
        print(len(results))
        results[i+4].click() # clicks the first one
        
        time.sleep(10)
        
        msg = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[2]/div/div[2]/div").click()
        
        time.sleep(3)
        
        #driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]").click()
        
        time.sleep(2)
        
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/p").send_keys("Elevate your videos with NEXTGEN! Our expert editing transforms footage into captivating stories. Fast, affordable, and tailored to you. Let's create something amazing together! Join now and write the code '2FAC' in the chat to receive a free professional edit at nextgenc.org")
        #msg[0].click()
        print("=============================================================================================================")
        print("Google Login")
          
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]").click()
        
        
        
    # finding email field and putting our email on it
    email_field = driver.find_element(By.XPATH,'//*[@id="identifierId"]')
    email_field.send_keys(email)
    driver.find_element(By.ID,"identifierNext").click()
    stop(5)
    print("email - done")

    # finding pass field and putting our pass on it
    find_pass_field = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located(find_pass_field))
    pass_field = driver.find_element(*find_pass_field)
    WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable(find_pass_field))
    pass_field.send_keys(password)
    driver.find_element_by_id("passwordNext").click()
    stop(5)
    print("password - done")
    WebDriverWait(driver, 200).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ytd-masthead button#avatar-btn")))
    print("Successfully login")
    print("============================================================================================================")

    return driver

    print("=============================================================================================================")
    print("Google Login")

    # finding email field and putting our email on it
    
    print("Successfully login")
    print("============================================================================================================")

    return driver
# ==============================================================================================================


# comment bot===================================================================================================
def comment_page(driver, urls, comment):

    if len(urls) == 0:
        print("============================================================================================================")
        print('Finished keyword jumping to next one...')
        return []

    # gettin a video link from the list
    url = urls.pop()

    driver.get(url)
    print("Video url:" + url)
    driver.implicitly_wait(1)

    # checking if video is unavailable
    if not check_exists_by_xpath(driver, '//*[@id="movie_player"]'):
        print("skiped")
        return comment_page(driver, urls, random_comment())

    time.sleep(2)
    # You can add like function by uncommenting 4 lines below
    # like_button = EC.presence_of_element_located(By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-icon-button/button/yt-icon')
    # WebDriverWait(driver, 50).until(EC.element_to_be_clickable(like_button)).click()
    # print('Liked')
    # time.sleep(1)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(1)

    # checking if comments are disabled
    if not check_exists_by_xpath(driver, '//*[@id="simple-box"]/ytd-comment-simplebox-renderer'):
        print("skiped")
        return comment_page(driver, urls, random_comment())

    # checking if video is a livestream
    if check_exists_by_xpath(driver, '//*[@id="contents"]/ytd-message-renderer'):
        print("skiped")
        return comment_page(driver, urls, random_comment())

    # finding comment box and submiting our comment on it
    comment_box = EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#placeholder-area'))
    WebDriverWait(driver, 4).until(comment_box)
    comment_box1 = driver.find_element_by_css_selector('#placeholder-area')
    ActionChains(driver).move_to_element(
        comment_box1).click(comment_box1).perform()
    add_comment_onit = driver.find_element_by_css_selector(
        '#contenteditable-root')
    add_comment_onit.send_keys(comment)
    driver.find_element_by_css_selector('#submit-button').click()
    print("done")

    stop(8)

    return comment_page(driver, urls, random_comment())
# ==============================================================================================================


# comment section
def random_comment():
    # You can edit these lines if you want to add more comments===================================
    comments = [
        'I like how all the elements combine in this video',
        'Great video',
        'nice video, ƒree editing. enter 2F6B in chat in the handle'

    ]
# =============================================================================================
    r = np.random.randint(0, len(comments))

    return comments[r]


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True


# running bot------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("imported")

def default(a, b):
    email = "312whoami312@gmail.com" 
    password = "Greanday312"

    driver = youtube_login(email, password)

    while True:
        key = driver.find_element_by_name('search_query')

        # get keyword list and extract each key
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f]
            random_keyword = random.choice(keywords)
            keys = spintax.spin(random_keyword)

            # send keyword in the search box
            for char in keys:
                key.send_keys(char)

        time.sleep(1)

        # click search icon
        driver.find_element_by_css_selector(
            '#search-icon-legacy > yt-icon').click()
        time.sleep(3)
        # click filter button to filter the videos for the recently uploaded, you can remove or edit this option
        driver.find_element_by_id("filter-button").click()
        time.sleep(3)
        driver.find_element_by_link_text("This week").click()
        time.sleep(3)

        # filtering for last hour
        #driver.find_element_by_xpath(
        #    "(//yt-formatted-string[@class='style-scope ytd-search-filter-renderer'])[1]").click()
        time.sleep(3)

        # grabbing videos titles
        for i in range(2):
            ActionChains(driver).send_keys(Keys.END).perform()
            time.sleep(1)
        titles = driver.find_elements_by_xpath('//*[@id="video-title"]')

        urls = []

        # getting url from href attribute in title
        for i in titles:
            if i.get_attribute('href') != None:
                urls.append(i.get_attribute('href'))
            else:
                continue

        # checking if we have links or not
        if urls == []:
            print("There is not videos for this keyword at the moment")
        else:
            comment_page(driver, urls, random_comment())