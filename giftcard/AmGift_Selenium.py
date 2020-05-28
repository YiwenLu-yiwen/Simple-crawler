import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import pandas as pd

def check_gf(cardnum, date, year, password):
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=Chrome Path") # open chrome://version, replace Chrome Path
    driver = webdriver.Chrome(chrome_options=option)   # open chrome
    
    #firefox=webdriver.FirefoxProfile("Firefox profiles path")  #get firefox profile path
    #driver = webdriver.Firefox(firefox, executable_path='Downloads/geckodriver')

    driver.get("https://balance.amexgiftcard.com/")
    time.sleep(2)
    driver.find_element_by_id("cardNumber").click()
    driver.find_element_by_id("cardNumber").clear()
    driver.find_element_by_id("cardNumber").send_keys(str(cardnum))
    driver.find_element_by_id("expirationMonth").click()
    driver.find_element_by_id("expirationMonth").clear()
    driver.find_element_by_id("expirationMonth").send_keys(str(date))
    driver.find_element_by_id("expirationYear").click()
    driver.find_element_by_id("expirationYear").clear()
    driver.find_element_by_id("expirationYear").send_keys(str(year))
    driver.find_element_by_id("cvv").click()
    driver.find_element_by_id("cvv").clear()
    driver.find_element_by_id("cvv").send_keys(str(password))

    # google recaptcha
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

    usr_input = input('Input Balance:  ') # record credit
    path = 'Downloads/GF credit/'
    filename = path + usr_input +" " + str(cardnum) + '.png'
    driver.get_screenshot_as_file(filename)
    driver.quit()
    return usr_input


def new_df(Credit, Card_Num, Date, Password):
    df = pd.DataFrame({'Credit':[Credit], 'Card_Num':[Card_Num], 'Date':[Date], 'Password': [Password]})
    return df

df = pd.DataFrame({'Credit':[], 'Card_Num':[], 'Date':[], 'Password': []})
total_list = []
with open ('credit.txt', 'r') as  f:  # format is in credit.txt
    for line_num, line in enumerate(f.readlines()):
        sublist = line.split()
        total_list.append(sublist)
f.close()


cnt = 0
for each in total_list:
    
    card_num = each[0]
    date = each[1]
    year = each[2]
    pass_word = each[3]
    com_date = str(date) +'/' + str(year)
    
    credit = check_gf(card_num, date, year, pass_word)
    print(cnt, card_num, date, year) # print current credit card
    
    sub_df = new_df(credit, card_num, com_date, pass_word)
    df = pd.concat([df, sub_df], ignore_index=True)
    df.to_csv('Credit.csv', index= False) # save csv to current directory
    
    cnt += 1