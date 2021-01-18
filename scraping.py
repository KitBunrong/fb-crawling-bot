import re
import time
import json
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options 

login_form_url = "https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=100"

def sent_message():
    try: 
        text = driver.find_element_by_xpath('//*[@id="composerInput"]')
        text.send_keys('Hii :)')
        print("Message inputted...")
        sent = driver.find_element_by_xpath('//*[@id="composer_form"]/table/tbody/tr/td[2]/input')
        sent.click()
        print("Message sent clicked...")
    except Exception:
        text = driver.find_element_by_xpath('//*[@id="composer_form"]/div[2]/table/tbody/tr/td[1]/textarea')
        text.send_keys('Hii :)')
        print("Message inputted...")
        sent = driver.find_element_by_xpath('//*[@id="composer_form"]/div[2]/table/tbody/tr/td[2]/input')
        sent.click()
        print("Message button clicked...")

def add_fri_sent_mess(profile_url):
    """ Automatic add frind to and get sent message.
    """
    driver.get(profile_url)

    try: 
        # add = driver.find_element_by_xpath("//table/tbody/tr/td/a[.='Add Friend']")
        add = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div[1]/div[3]/table/tbody/tr/td[1]/a')
        print(add.get_attribute('innerHTML'))
        if(add.get_attribute('innerHTML') == 'Add Friend'):
            add.click()
            
            bname = driver.find_element_by_xpath("//*[@id='root']/div[1]/div[1]/div[1]/div[1]/span/strong")
            print("'Sent Friend Reqest to :", bname.get_attribute('innerHTML'), " , Waiting for Comfirmation...")

            msg = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div[1]/div[1]/div[1]/div/table/tbody/tr/td[2]/a')
            msg.click()
            print("Message button clicked...")
            sent_message()

        elif(add.get_attribute('innerHTML') == 'Message'):
            name = driver.find_element_by_xpath('//*[@id="m-timeline-cover-section"]/div[2]/div[1]/span/div/span/strong')
            print('You already friend with :', name.get_attribute('innerHTML'))

    except Exception:
        try: 
            name = driver.find_element_by_xpath("//*[@id='root']/div[1]/div[1]/div[2]/div/span/div/span/strong")
            print("Waiting Confirmation from :", name.get_attribute("innerHTML"))            
        except Exception:
            print("There's Something Went Wrong...")   

    # ? When should message sent to:
    # ? 1. At the same time we sent friend request
    # ? 2. When we got friend comfirmation
    # text = driver.find_element_by_xpath("//table/tbody/tr/td/textarea")
    # sent.click()
    # sent = driver.find_element_by_xpath("//table/tbody/tr/td[2]/a[.='Message']")
    # print("Message button clicked")
    # text.send_keys("Hello Hi bybybye!!")
    # print("text")


def json_to_obj(filename):
    """ Extract data from JSON file and save it on Python object 
    """
    print("*** : json_to_obj ***")
    obj = None 
    with open(filename) as json_file:
        obj = json.loads(json_file.read())
    return obj

def dataframe_to_obj():
    """ Extract data from csv file and save it to Python object 
    """
    print("*** : dataframe_to_obj ***")
    list_url = []
    filename = input("Enter filename [e.g., sample.csv] : ")
    try: 
        profile_urls = pd.read_csv(filename)
    except Exception:
        print("Recheck your filename...")   
        return
    cname =profile_urls.columns[0]
    for i in range(len(profile_urls)):
        ls = profile_urls.loc[i, cname]
        list_url.append("https://mbasic" + ls[11:])
        # print(list_url.append(profile_urls.loc[i, cname]))
    return list_url

if __name__ == "__main__":
    ### Extracts credentials for the login and all of the profiles URL to scrape
    credentials = json_to_obj('credentials.json')
    profile_urls = dataframe_to_obj()
    # profile_urls = json_to_obj('profiles_urls.json')

    ### Block the notifications
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    ### Running at background without opening browser.
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options, executable_path=r'/usr/bin/chromedriver')

    driver.get(login_form_url)

    email = driver.find_element_by_xpath("//input[@id='email' or @name='email']")
    email.send_keys(credentials['email'])
    print("email entered...")
    password = driver.find_element_by_xpath("//input[@id='pass']")
    password.send_keys(credentials['pass'])
    print("pass entered...")
    button = driver.find_element_by_xpath("//button[@id='loginbutton']")
    button.click()
    print("button clicked...")

    time.sleep(5)
    print("login successfully...")

    for profile_url in profile_urls:
        ### Auto add friend and sent "xxx" message to
        sleep = random.randint(5,10)
        add_fri_sent_mess(profile_url)
        print("[***] Sleep for :", sleep)
        time.sleep(sleep)
