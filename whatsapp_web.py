import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def custom_driver(path_to_driver, cookies_folder, headless):
    options = Options()
    options.add_argument("--window-size=1920,1080")
    cookies = cookies_folder
    options.add_experimental_option("prefs", {
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True})
    options.add_argument("--start-maximized")
    options.add_argument('--user-data-dir={}'.format(cookies))
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/73.0.3641.0 Safari/537.36")
    options.headless = headless
    driver = webdriver.Chrome(path_to_driver, options=options)
    return driver


def send_message(driver, contact, text):
    contact_xpath = '//span[@title = "{}"]'.format(contact)
    try:
        user = driver.find_element_by_xpath(contact_xpath)
        user.click()
    except NoSuchElementException:
        search_box_xpath = '//*[@id="side"]/div[1]/div/label/div/div[2]'
        search = WebDriverWait(driver, 3).until(ec.element_to_be_clickable((By.XPATH, search_box_xpath)))
        search.click()
        search.send_keys(contact)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, contact_xpath))).click()
    input_box_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
    input_box = driver.find_element_by_xpath(input_box_xpath)
    input_box.click()
    for line in text.split('\n'):
        ActionChains(driver).send_keys(line).perform()
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    '''The purpose of this function is to send whatsapp messages. Text whatsapp messages! It receives inputs
    as driver, who to send the message to, and text to send'''


def send_attachment(driver, contact, attachment):
    p = '//span[@title = "{}"]'.format('Therapy')
    WebDriverWait(driver, 90).until(ec.element_to_be_clickable((By.XPATH, p)))
    c = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    search = WebDriverWait(driver, 3).until(ec.element_to_be_clickable((By.XPATH, c)))
    search.click()
    search.send_keys(contact)
    p = '//span[@title = "{}"]'.format(contact)
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, p))).click()
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
    input_box = driver.find_element(By.XPATH, inp_xpath)
    input_box.click()
    driver.find_element(By.CSS_SELECTOR, "span[data-icon='clip']").click()
    item = driver.find_element(By.CSS_SELECTOR, "input[type='File']")
    item.send_keys(attachment)
    time.sleep(1)
    c = '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div/span'
    WebDriverWait(driver, 3).until(ec.element_to_be_clickable((By.XPATH, c))).click()
    time.sleep(5)
    '''In case you need to send a document instead of text, use this one instead'''


if __name__ == "__main__":
    pass
    # the first time running this keep the headless option False so you can scan the QR code with your phone
    #driver = custom_driver(path_to_driver, cookies_folder, False)
    #driver.get("https://web.whatsapp.com")
    # send_message(driver, 'Therapy', "Now it begins")
