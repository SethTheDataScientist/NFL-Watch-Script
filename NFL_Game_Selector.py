import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
import time
import os
import csv
import shutil
from datetime import datetime, timedelta
import random
import pyautogui

shuffled_df = pd.read_csv("shuffled_df.csv")


user_id = os.environ.get('nfl_plus_account')
password = os.environ.get('nfl_plus_password')



def get_driver(url):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')   
    chrome_options.add_argument('--disable-infobars') 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])    
    
     
    
    driver = webdriver.Chrome(service = Service(executable_path= 'chromedriver.exe'), options = chrome_options)
    driver.get(url)
    
    return driver
   


def Setup(url):
    print("starting process")

    driver = get_driver(url)
    # Remove Cookies bar
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/button'))) 
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/button').click()
    
    # Select Sign In
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/button'))) 
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/button').click()
    
    # SIGN IN
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email-input-field"]'))) 
    driver.find_element(By.XPATH, '//*[@id="email-input-field"]').send_keys(user_id)
     
    
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div'))) 
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div').click()


    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password-input-field"]'))) 
    driver.find_element(By.XPATH, '//*[@id="password-input-field"]').send_keys(password)   

    pyautogui.FAILSAFE = True

    screen_width, screen_height = pyautogui.size()
    
    pyautogui.moveTo(screen_width-5, 5)  
    
    time.sleep(3)
          
    condensed = False
    # Select Condensed Version if Possible
    for i in range(3):
        try:
            wait_til = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[text() = "Condensed Game Replay"]'))) 
            driver.find_element(By.XPATH, '//div[text() = "Condensed Game Replay"]').click()
            print("condensed version activated")
            condensed = True
            break
        except:
            print('doesnt have condensed version')
            
    fullscreen = False
    for i in range(3):
        # Select Full Screen
        try:
            wait_til = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/main/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[3]/div/div/div[2]/div[2]/button[2]/div'))) 
            driver.find_element(By.XPATH, '/html/body/div[3]/main/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[3]/div/div/div[2]/div[2]/button[2]/div').click()
            print("fullscreen enabled")
            fullscreen = True
            break
        except:
            print(f'cant do full screen, try #{i}')
        
            
    try:
        wait_til = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-testid = "controls-current-time"]'))) 
        element = driver.find_element(By.XPATH, '//*[@data-testid = "controls-current-time"]')
        text = element.text
        split_time = text.split('/')
        second_time = split_time[1].strip()
        minutes, seconds = map(int, second_time.split(':'))
        total_seconds = minutes * 60 + seconds
        
        if total_seconds > 0:
            print(total_seconds)
            print("time selected")
            time.sleep(total_seconds)   
        else:
            if condensed:
                time.sleep(2700)
                print('cant find time properly, doing average condensed game')
            else:
                time.sleep(7200)
                print('cant find time properly, doing average full game')
    except:
        if condensed:
            time.sleep(2700)
            print('cant find time properly, doing average condensed game')
        else:
            time.sleep(7200)
            print('cant find time properly, doing average full game')
    
           
    print("quitting now")

    driver.quit()
    
if __name__ == "__main__":
    
    try:
        shuffled_df = pd.read_csv("shuffled_df.csv")
        url = shuffled_df['url'][0]
        season = shuffled_df['season'][0]
        shuffled_df = shuffled_df.drop(index = shuffled_df.index[0])
        shuffled_df.to_csv('shuffled_df.csv', index = False)
        print('saved new shuffled')
        print(url)
        Setup(url)
    except Exception as e:
        print(f"could not run for {e}")
        pass
    