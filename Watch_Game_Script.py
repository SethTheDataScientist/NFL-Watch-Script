import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
import time
import csv
import shutil
from datetime import datetime, timedelta
import random
import pyautogui
import os



user_id = os.environ.get('nfl_plus_account')
password = os.environ.get('nfl_plus_password')


def get_driver(url):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')   
    chrome_options.add_argument('--disable-infobars') 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])    
    
     
    
    driver = webdriver.Chrome(options = chrome_options)
    driver.get(url)
    
    return driver  

def Watch_Game(url, verbose = False):
    if verbose:
        print("starting process")

    driver = get_driver(url)
    # Remove Cookies bar
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/button'))) 
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/button').click()
    
    if verbose:
        print("Removed Cookies bar")

    time.sleep(2)
    
    # Select Sign In
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/button'))) 
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/button').click()
    
    if verbose:
        print("Selected Sign In Link")

    # Input username
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email-input-field"]'))) 
    driver.find_element(By.XPATH, '//*[@id="email-input-field"]').send_keys(user_id)
    
    if verbose:
        print("Input Username")

    time.sleep(2)

    # Select Continue
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div[3]/button/div/div/div/div'))) 
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[3]/button/div/div/div/div').click()
    
    if verbose:
        print("Selected Continue")

    #Input password
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password-input-field"]'))) 
    driver.find_element(By.XPATH, '//*[@id="password-input-field"]').send_keys(password)    
    
    if verbose:
        print("Input password")

    time.sleep(2)
    
    # Select Sign in again
    wait_til = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[4]/button/div/div'))) 
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[4]/button/div/div').click()
    
    if verbose:
        print("Selected Sign in Again")

    screen_width, screen_height = pyautogui.size()
    
    pyautogui.moveTo(screen_width-5, 5)  
    
          
    condensed = False
    # Select Condensed Version if Possible
    for i in range(3):
        try:
            time.sleep(1)
            wait_til = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[text() = "Condensed Game Replay"]'))) 
            driver.find_element(By.XPATH, '//div[text() = "Condensed Game Replay"]').click()
            if verbose:
                print("condensed version activated")
            condensed = True
            break
        except:
            if verbose:
                print('doesnt have condensed version')
        
    
    # Scroll down 100 units
    pyautogui.scroll(-100)

    fullscreen = False
    for i in range(3):
        # Select Full Screen
        try:
            time.sleep(1)
            wait_til = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/main/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[3]/div/div/div[2]/div[2]/button[2]/div'))) 
            driver.find_element(By.XPATH, '/html/body/div[3]/main/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[3]/div/div/div[2]/div[2]/button[2]/div').click()
            if verbose:
                print("fullscreen enabled")
            fullscreen = True
            break
        except:
            if verbose:
                print(f'cant do full screen, try #{i}')
            
    try:
        time.sleep(5)
        wait_til = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-testid = "controls-current-time"]'))) 
        element = driver.find_element(By.XPATH, '//*[@data-testid = "controls-current-time"]')
        text = element.text
        split_time = text.split('/')
        second_time = split_time[1].strip()
        minutes, seconds = map(int, second_time.split(':'))
        total_seconds = minutes * 60 + seconds
        
        print(total_seconds)
        if verbose:
            print("time selected")
        time.sleep(total_seconds)   
    except:
        if condensed:
            time.sleep(2700)
            if verbose:
                print('cant find time properly, doing average condensed game')
        else:
            time.sleep(7200)
            if verbose:
                print('cant find time properly, doing average full game')
    
        
    if verbose:
        print("quitting now")

    driver.quit()