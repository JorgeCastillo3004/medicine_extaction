from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random

# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import pandas as pd
import re
import os
import json
from selenium import webdriver 
import chromedriver_autoinstaller 
from selenium.webdriver.common.proxy import Proxy, ProxyType

def save_check_point(filename, dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def load_check_point(filename):
    # Opening JSON file
    if os.path.isfile(filename):
        with open(filename, 'r') as openfile:        
            json_object = json.load(openfile)
    else:
        json_object = {}
    return json_object

# chromedriver_autoinstaller.install() 

# Create Chromeoptions instance 
def launch_naviagator():
    options = webdriver.ChromeOptions() 
     
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
     
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
     
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 

    # LOAD DEFAULT PROFILE
    # LOAD DEFAULT PROFILE
    options.add_argument(r"user-data-dir=/home/jorge/.config/google-chrome/") #leave out the profile
    options.add_argument(r"profile-directory=Profile\ 1") #enter profile here

    # driverArticle = webdriver.Chrome()
    # driverArticle.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    # from mainArticle import *
    ################# IP SETTINGS ###############################
    # proxy_ip_port = '2.56.119.93:5074'						#
    # proxy = Proxy()											#
    # proxy.proxy_type = ProxyType.MANUAL						#
    # proxy.http_proxy = proxy_ip_port							#
    # proxy.ssl_proxy = proxy_ip_port							#
    # capabilities = webdriver.DesiredCapabilities.CHROME 		#
    # proxy.add_to_capabilities(capabilities) 					#
    #############################################################

    # LOAD DEFAULT PROFILE
    # options.add_argument = {'user-data-dir':'/home/jorge/.config/google-chrome/Default'}
     
    # Setting the driver path and requesting a page 
    driver = webdriver.Chrome(options=options)
     
    # Changing the property of the navigator value for webdriver to undefined 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

def find_block(driver, header):
    wait = WebDriverWait(driver, 10)

    xpath_expression = """//div[@class="columnContainer--ZzkOF" and
                     ..//div[@class="header--AEA7m" and contains(.,"{}")]]""".format(header)
    block = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
    block = driver.find_element(By.XPATH, xpath_expression)
    return block

def element_classification(element):
    # CLASSIFICATION, CLASIFICATE LIKE FOLDER OR ARTICLE LINK
    HTML = element.get_attribute('outerHTML')
    if 'library-list' in HTML:        
        return True
        
    elif 'articleLink' in HTML:        
        return False

def check_json(file_path = 'check_points/articles_links.json'):
    dict_links = load_check_point(file_path)
    keys = list(dict_links.keys())
    if len(keys)!= 0:
        new_key = int(keys[-1]) + 1
    else:
        new_key = 0
    return dict_links, new_key

def stop_validate():
    user_input = input("Type s to stop other to continue: ")
    if user_input=='s':
        print(stop)

def explore_block(driver, current_path, header):
    # DEFINE MAXT TIME TO WAIT ELEMENTS
    wait = WebDriverWait(driver, 10)

    # FIND BLOCK USING HEADER
    print("CURRENT HEADER: ", header)
    block = find_block(driver, header)
    
    # GET LIST OF ELEMENTS INSIDE CURRENT BLOCK
    list_of_elements = block.find_elements(By.XPATH, './/div[@class="listContainer--SnK6M"]/div/a')

    # CALCULATE THE DEEP INSIDE FOLDERS (IT IS USED ONLY FOR CONTROL)
    deep = len(current_path.split('/'))    
    
    # INIT INDEX CONTROL
    curren_index = 0
    
    # NAVIGATE THROUGH BLOCK WITH CURRENT HEADER
    while curren_index < len(list_of_elements):

        # CREATE CURRENT ELEMENT USING CURRENT INDEX AND LIST OF ELEMENTS
        element = list_of_elements[curren_index]
        current_name = element.text
        print("#"*(deep-5), current_name)

        # CHECK IF CURRENT ELEMENT IS A FOLDER OR ARTICLE (IN CASE OF FOLDER RETURN TRUE)
        folder_flag = element_classification(element)

        if folder_flag:
            print("#"*(deep-5), "Start  : ", element.text)
            # CHECK IF CURRENT_PATH EXIST
            current_path = os.path.join(current_path, element.text.replace(' ', '_'))
            if not os.path.exists(current_path):
                os.makedirs(current_path)                

            # CLICK ON CURRENT FOLDER
            element.click()

            # SEARCH AND WAIT FOR THE BLOCK WHERE THE HEADER MATCHES THE ELEMENT'S TEXT.
            block = find_block(driver, element.text)

            # REPEAT EXPLORE BLOCK WHERE HEADER IS THE CURRENT FOLDER NAME
            explore_block(driver, current_path, element.text)

            # CLICK AGAIN IN FOLDER TO COMPRESS AGAIN FOLDER.
            # xpath_folder = '//div[@class="childrenContainer--h7CNS" and contains(.,"{}")]'.format(current_name)
            # xpath_folder = '//div[@class="childrenContainer--h7CNS"]//*[contains(text(), "{}")]'.format(current_name)
            xpath_folder = '//a[@data-e2e-test-id="library-list-item-link-active"]//*[contains(text(), "{}")]'.format(current_name)
            folder = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_folder)))
            print("#"*(deep-5), "Colapse: ", folder.text, (deep-5), end=' ')
            # stop_validate()
            folder.click()
            print("Click ready")
            # time.sleep(4)
        else:
            # GET ARTICLE LINK
            article_link = element.get_attribute('href')            

            # LOAD JSON LINK DICTIONARY
            dict_links, new_key = check_json(file_path = 'check_points/articles_links.json')

            dict_links[new_key] = {'folder':current_path, 'link':article_link}

            save_check_point('check_points/articles_links.json', dict_links)

        # DUE TO THAT SOME ELEMENTS DESAPEAR FROM SCREEEM, IT IS NECESSARY TO FIND AGAIN
        # FIND BLOCK USING HEADER
        block = find_block(driver, header)
        
        # GET LIST OF ELEMENTS INSIDE CURRENT BLOCK
        list_of_elements = block.find_elements(By.XPATH, './/div[@class="listContainer--SnK6M"]/div/a')

        # UPDATE INDEX CONTROL        
        curren_index += 1

def main(driver):
    # CHECK IF FOLDER check_points EXIST AND CREATE IF IS NECESSARY    
    if not os.path.exists('check_points'):
        os.makedirs('check_points')
    # FIND THE START BLOCK (LIBRARY)
    # start_block = driver.find_element(By.XPATH, '//div[@data-e2e-test-id="library-column-Library"]')
    
    # GET CURRENT PATH
    # current_path = os.getcwd()
    current_path = ''
    explore_block(driver, current_path, 'Biblioteca')

# if __name__ == "__main__":  
#     main()