from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
from selenium.common.exceptions import NoSuchElementException
import csv
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
# user_agent  = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

class EbayAt:
    timestamp = str(datetime.datetime.now()).replace(".","").replace("-","").replace(":","")
    filename = "results_{}".format(timestamp)+".csv"
    def __init__(self,url):
        self.driver = webdriver.Chrome('chromedriver.exe',options=options)
        self.csvCreater()
        self.start(url)
        # self.driver.quit()
    def writeTextFile(self,filename,data,operation):
        with open(filename,operation) as file:
            file.write(str(data)+"\n")
    def ScrollPage(self):
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                lastCount = lenOfPage
                sleep(3)
                lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True
    def csvCreater(self):
        with open(self.filename,'w' ,newline='') as file:
            fieldNames = ['Name','Remaining Time','Current Price','Article URL']
            thewriter = csv.DictWriter(file, fieldnames=fieldNames)
            thewriter.writeheader()

    def csvupdate(self,title,url,price,time_left):
        with open(self.filename,'a' ,newline='') as file:
            fieldNames = ['Name','Remaining Time','Current Price','Article URL']
            thewriter = csv.DictWriter(file, fieldnames=fieldNames)
            thewriter.writerow({'Name': str(title),'Remaining Time': str(time_left),'Current Price': str(price),'Article URL': str(url)})
  
    def start(self,url):
        self.driver.get(url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.lvtitle')))
        self.ScrollPage()
        self.driver.find_element_by_css_selector("a.btn.btn-s.small.btn-ter.dropdown-toggle").click()
        self.driver.find_element_by_css_selector('#cbBtmElem > div > ul.lyr.txtRt.dropdown-menu.dropdown-menu-sm.menu3 > li:nth-child(3) > a').click()
        Page = 1
        while True:
            print("Page Number: "+str(Page))
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.lvtitle')))
            self.ScrollPage()
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#gdpr-banner')))
                accept_button = self.driver.find_element_by_css_selector("button#gdpr-banner-accept")
                accept_button.click()
            except:
                pass
            listings = self.driver.find_elements_by_css_selector("li.sresult.lvresult.clearfix.li")

            # print(len(titles))
            for listing in listings:
                title = str(listing.find_element_by_css_selector("h3.lvtitle").text).replace("NEUES ANGEBOT","").strip()
                url = listing.find_element_by_css_selector("a.vip").get_attribute("href")
                price = str(listing.find_element_by_css_selector("li.lvprice.prc").text)
                time_left = str(listing.find_element_by_css_selector("li.timeleft").text)

                self.csvupdate(title,url,price,time_left)
                print(title,url,price,time_left)
            try:
                nextbutton = self.driver.find_element_by_css_selector("a.gspr.next")
                nextbutton.click()
            except NoSuchElementException:
                break
            Page = Page+1


ebay_instance = EbayAt("https://www.ebay.at/sch/last-minute-travel/m.html?_nkw=&_armrs=1&_ipg=&_from=&rt=nc&LH_Auction=1")