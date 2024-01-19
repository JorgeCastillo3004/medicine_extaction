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
chromedriver_autoinstaller.install() 

# Create Chromeoptions instance 
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
options.add_argument(r"profile-directory=Profile 5") #enter profile here

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

def saveCheckPoint(filename):
    dictionary = {
        "path":'/'.join(listpath)     
    }
    
    json_object = json.dumps(dictionary, indent=4)    
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def loadCheckPoint(filename):
    # Opening JSON file
    with open(filename, 'r') as openfile:        
        json_object = json.load(openfile)
    return json_object

def saveArticleLinks(filename, dictinfo):    
    
    json_object = json.dumps(dictinfo)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def getListBooks(blocks):
    for block in blocks:
        header = block.find_element(By.CLASS_NAME, 'header--AEA7m')
        
        if 'Biblioteca' in header.text or 'Library' in header.text:
            blocklibrary = block
            books = blocklibrary.find_elements(By.CLASS_NAME, 'container-4155112263')        
    return books

def clickGetNextHeader(component):
    dictStepCheck['Next_Header'] = component.text
    if component.text=='':
        print("#"*20," NEXT HEADER EMPTY ", "#"*20)

    TS = random.uniform(1, 2.5)
    counttry = 0 
    ClickWait = True
    while ClickWait:
        try:
            time.sleep(TS)	    	
            component.click()
            ClickWait = False
        except:
            print("W", end='')
            time.sleep(TS)
            counttry +=1
            
            if counttry==50:	            
                checkflag = input('"y" to continue or "n"to stop script ')
                print(dictStepCheck)
                
                if checkflag == 'y':
                	counttry=0
                else:
                	print(stop)
    return component.text

def updateBlocks(driver):	
	blocks = driver.find_elements(By.CLASS_NAME,'column-2408730506')
	return blocks

def getTypeOfLink(item):
    HTML = item.get_attribute('outerHTML')
    if 'id="list-item-article-' in HTML:            
        article = True
    else:            
        article = False
    return article

def createFolderPath(folderpath):
	isExist = os.path.exists(folderpath)
	if not isExist:
		os.makedirs(folderpath)

def getComponents(blocks, nextHeader):
    # print("Inside getComponents")
    # print("Numero de bloques actuales", len(blocks) )
    TS = random.uniform(1.5, 2.5)
    repeatflag1  = True
    repeatflag2 = True
    while repeatflag1 or repeatflag2:
        try:
            for block in blocks:    
                header = block.find_element(By.CLASS_NAME, 'header--AEA7m')
                # check every block until find nexHeader in header block
                if nextHeader in header.text:
                    # load the object that match with nextheader
                    container = block.find_elements(By.CLASS_NAME, 'container-4155112263')
                    # in case of article link, it get the article link
                    repeatflag2 = checkListFolders(container) # return repeatflag = True, if some element is empty, include avoid next header empty
                    print("repeatflag2 inside get components ")
                    try:
                        # in case of to be an article save article link
                        articleLinkContainer = block.find_element(By.CLASS_NAME, 'articleLink--HCJ2O.link--RO9eO')
                        link = (articleLinkContainer.get_attribute('href'))
                    except:
                        link= ''
                    return {'container':container,'link': link}
                repeatflag1 = False
        except:
            print("Waiting until find container, block with the actual next header", end ='')
            blocks = updateBlocks(driver)
            time.sleep(TS)
            
def depurar():
    confirmacion = input("continuer 'y'")
    if confirmacion:
        print("continuar")
    else:
        print(stop)

def checkListFolders(container):
    verificationflag = False   
    firstcheck = True
    maxtries = 0
    while not verificationflag:

        for foldername in container:
            print("Containter: text ", foldername.text)
            if foldername.text == '':
                secondchecks = False
            else:
                secondchecks = True

            if firstcheck and secondchecks:
                firstcheck = True
            else:                
                firstcheck = False
        
        if firstcheck and secondchecks:
            verificationflag = True
            repeatflag = False

        # Count and limit the number of tries
        if not verificationflag:
            time.sleep(0.3)
            maxtries += 1
            if maxtries ==10:
                verificationflag = True
                repeatflag = True
    return repeatflag

def funcInfiniteCheck(driver, element):

    global listpath, dictColumns, dictPathsLinks, dictArticleLinks, idarticle    
    dictPathsLinks = {}
    dictStepCheck = {}
    folderpath = '/'.join(listpath)	
    createFolderPath(folderpath)
    # print("#"*20, "  FOLDER PATH  ", "#"*20)
    # print(folderpath)
    saveCheckPoint('checkpointAmboss/CheckPoint.json')
    print("########################## NEXT HEADER ##########################", element.text)
    # time.sleep(1.5)-wait-
    nextHeader = clickGetNextHeader(element) # Get actual header and click in the element    
    dictStepCheck['Next_Header'] = nextHeader
    blocks = updateBlocks(driver)
    # time.sleep(1.5) -wait-
    dictStepCheck['Update_Block'] = 'ready'
    key = nextHeader.replace(' ','')	
    dictColumns[key] = getComponents(blocks, nextHeader)    
    dictStepCheck['Get_Components_Colum'] = 'ready'

    level = len(blocks)
    # print("Deep ", level)
    
    #########################################################
    listcontenido = []                                      #
    for item in dictColumns[key]['container']:              # FOR DELETE ONLY FOR TEST
        listcontenido.append(item.text)                     #
    #########################################################

    checkListFolders(dictColumns[key]['container'])
    
    print("List initial contenido: ")
    print(listcontenido)
    for item in dictColumns[key]['container']: # Elementos resultantes de hacer click

        # time.sleep(3) # -w- #
        verificacion = getTypeOfLink(item) # verificacion if is an article-link
        dictStepCheck['Article_check'] = verificacion

        if verificacion: # case download article
            #Descargar articulo/archivo            
            filename = item.text.replace(' ','')
            filepath = '/'.join([folderpath, '/',filename])            
            articleLink = dictColumns[key]['link']
            dictStepCheck['Link_Article'] = 'ready'
            dictArticleLinks[idarticle] = {'folder':folderpath, 'link':articleLink}            
            idarticle += 1            
            # print(dictStepCheck,'\n')
            # print("Actual article: ", item.text)
            # print("#"*30, 'ARTICLE LINK' ,"#"*30)
            # print(articleLink)
            saveArticleLinks('checkpointAmboss/articleLinks.json', dictArticleLinks)
            # getArticleData(articleLink, filepath)

        else:

            while len(listpath)<level+1:
                listpath.append('')

            if len(listpath)>level:
                listpath = listpath[0:level+1]

            listpath[level] = item.text.replace(' ','_').replace(',','')
            print("#"*50)
            print(dictStepCheck,'\n')
            # Ejecucion recursiva
            # se llama a la misma funcion
            # Elementos y palabra sobre la que se hizo click            
            dictStepCheck['Click_new_folder'] = 'launched'
            funcInfiniteCheck(driver, item)
    print("End folder conten", item.text)
###################################### FUNCIONES FOR EXTRACT ARTICLE INFORMATION #######################################
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def confirmLogin(): 
    global registerflag
    while not registerflag:
        userin = input("Please confirm if the login in the account is ready, please type 'y'")
        if userin =='y':
            registerflag = True

def saveLastArticle(idnumber, link):
    filename = 'checkpointAmboss/lastarticle.json'
    dictionary = {'last':idnumber, 'link':link}
    json_object = json.dumps(dictionary)    
    with open(filename, "w") as outfile:
        outfile.write(json_object)
        
def getSectionInfo(section):
    global count, dicttest
    count = 0
    dicttest = {}    
    print("Get section information: ")
    while '\nNOTES\nFEEDBACK' in section.text:
        print('w',end='-')
        dicttest[count] = section.text
        count +=1
        time.sleep(0.2)
#         driver.key_down(Keys.SHIFT)
#         webdriver.ActionChains(driver).key_down(Keys.SHIFT).perform()
    dicttest[count] = section.text    
    # return section.text.replace('\nAPPUNTI\nFEEDBACK','')

def getLinksbySection(section):
    dictSection = {}
    links = section.find_elements(By.CLASS_NAME, 'api')
    linktext = []
    for link in links:
        # if link.text!='':
        if link.text!=''and not(link.get_attribute('href') is None) and not('--same-article' in link.get_attribute('outerHTML')):
            key = link.text.replace(' ','_')
            dictSection[key] = link.get_attribute('href')
            linktext.append(link.text)
    # Loop to give format at section text
    sectiontext = section.text

    # for wordlink in linktext:    
    #     boldword = color.BOLD + wordlink + color.END
    #     sectiontext = sectiontext.replace(wordlink, boldword)

    return dictSection, sectiontext

def getYouTubeLink(section, dictSection):
    # Search block that contains all the elements from this section.
    try:
        class_sub = 'content--kLKAu.baseStyles-2133108132--disableImagePointerEventOnTutorial-3958995088--anchorLinkStyles-27620709'
        subSectionContainer = section.find_element(By.CLASS_NAME, class_sub)
        tags = subSectionContainer.find_elements(By.CSS_SELECTOR,"div, h3, h4")
        
        for tag in tags:

            HTML = tag.get_attribute('outerHTML')
            if '<h3' in HTML or '<h4'in HTML:
                if tag.text !='':
                    namelink = tag.text.replace(' ','_') + '_youtubelink'
                
            if '<div' in HTML and 'miamed-video=' in HTML:
                youtubelink = re.findall('miamed-video="(.+?)"', HTML)
                dictSection[namelink] = youtubelink
        return dictSection
    except Exception as e:
        print("Error: ", e)
        print("Section without YOUTUBE links")
        return dictSection
                
def getArticleData(articleLink, filepath):
    global registerflag    
    driver.get(articleLink)   

    # define wait until load each elemets -WAIT-
    dictArticle = {}
    # First step detect sections and header
    headerContainers = driver.find_elements(By.CLASS_NAME, 'container-915194668')
    while len(headerContainers)==0:
        time.sleep(0.5)
        print('-w cont', end='')
        headerContainers = driver.find_elements(By.CLASS_NAME, 'container-915194668')
    # Iterate over each section with header
    for section in headerContainers:
        print(section.text)
        # Find element to expand section 
        expansor = section.find_element(By.CLASS_NAME, 'headerContainer--rfIL2')
        # Save section name in other variable
        namesection = section.text
        # Expand section
        print("Click to expand section") 
        expansor.click()
        # time.sleep(2.5) # -WAIT-
        getSectionInfo(section)
        

        ######################## LINKS EXTRACTIONS: LINKS INFO, YOUTUBE LINKS ###########################
        # Check all the availables links and save it in dictSection[key] = _links                       #
        print("Getting links by section")                                                               #
        dictSection, contentSection = getLinksbySection(section)                                        #
        # Load info in dictArticle                                                                      #
        dictArticle[namesection] = contentSection                                                       #
        print("Getting youtubelinks")                                                                   #
        dictSection = getYouTubeLink(section, dictSection)                                              #       
        print("len dict section", len(dictSection))                                                     #
        if len(dictSection)!= 0:                                                                        #
            dictArticle[namesection+'_links'] = [dictSection]                                           #
                                                                                                        #
        #################################################################################################

        print("############## Searching Table ##############")
        getTableData(filepath +'_tables.xlsx', section, namesection)    
        # -WAIT- #
        time.sleep(2)
        expansor.click() # Click to contract section

    df = pd.DataFrame.from_dict(dictArticle)
    df.to_excel(filepath + '.xlsx')
    return dictArticle

def getTableData(filename, section, sectionname):
    try:
        tables = section.find_elements(By.CSS_SELECTOR, 'table')

        for numbtable, table in enumerate(tables):

            HTMLstring = table.get_attribute('outerHTML')

            if not os.path.exists(filename):
                df = pd.DataFrame()
                df.to_excel(filename,sheet_name= sectionname+"_{}".format(numbtable))


            HTMLstring = table.get_attribute('outerHTML')
            df = pd.read_html(HTMLstring)[0]    

            with pd.ExcelWriter(filename, mode="a", engine="openpyxl", if_sheet_exists = "replace") as writer:
                df.to_excel(writer, sheet_name=sectionname+"_{}".format(numbtable))
            print("Table Saved Succesfully")
    except:
        print("Without Table")

def loopOverLinks(articleLinksdict):
    
    confirmLogin()
    userconfirmation = input("Do you want to continue in previous check point? 'y' yes or 'n' to restart at inicial point ")
    
    if userconfirmation == 'y':
        checkpoint = loadCheckPoint('checkpointAmboss/lastarticle.json')
        idnumber = int(checkpoint['last'])
        print("Loading check point, last dict number: ", idnumber)
    else:
        idnumber = 0
        
    for idnumber in list(articleLinksdict.keys())[idnumber:]:
        articleLink = articleLinksdict[idnumber]['link']
        filepath = articleLinksdict[idnumber]['folder']
        getArticleData(articleLink, filepath)
        print("#"*60)
        print(idnumber, articleLink, filepath)
        saveLastArticle(idnumber, articleLink)


#########################################################################################################################
def main():
    """
    Main Function:
    - Configure Chrome browser settings.
    - Load the main URL.
    - Provide options to either retrieve a list of article links again or proceed directly to download article information.

    This main function calls two primary functions:
    - funcInfiniteCheck: Performs the task of clicking on each folder to gather all available article links.
    - loopOverLinks: Performs the task of accessing each URL and retrieving article information.

    """
    time.sleep(3)
    driver.get("https://next.amboss.com/us/library/")
    time.sleep(3)
    loadlist = input("Do you want to load a list of links? Type 'y' or type 'n' to update the list of links ")
    
    while not(loadlist =='n' or loadlist =='y'):
        loadlist = input("Please type 'y' or 'n', unique valid options" )

    if loadlist == 'n':

        print("Proceed to get list of links")

        blocks = updateBlocks(driver)
        books = getListBooks(blocks)

        level = len(blocks)

        for book in (books):
            
            print("\n Book {}".format(level), book.text)
            listpath[1] = book.text.replace(' ','_')
            
            time.sleep(TS)

            funcInfiniteCheck(driver, book)

    if loadlist =='y':
        print("Proceed to download article info")
        # Get links info

        articleLinksdict = loadCheckPoint('checkpointAmboss/articleLinks.json')
        loopOverLinks(articleLinksdict)


dictColumns = {}
TS = 3
i = 1
listpath = ['files','']
numbBlocksInitial = 1
dictStepCheck = {}
registerflag = False
idarticle = 0
dictArticleLinks = {}

if __name__ == "__main__":  
    main()