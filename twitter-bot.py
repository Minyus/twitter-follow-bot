import csv
import random
import time
from configparser import ConfigParser
from getpass import getpass

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from util import _get_exception_msg


def read_handles(filename):
    handles = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            handles.append(row[0])
    return handles


def login(driver, username, password):
    driver.get("https://twitter.com/i/flow/login")
    driver.set_window_size(1323, 824)
    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, ".r-1wzrnnt").click()
    driver.find_element(By.NAME, "text").send_keys(username)
    driver.find_element(By.NAME, "text").send_keys(Keys.ENTER)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(
        By.CSS_SELECTOR, ".css-18t94o4 > .css-901oao > .css-901oao > .css-901oao"
    ).click()

    if "Login on Twitter" in driver.title:
        return False
    else:
        return True


def follow(driver, handle):
    try:
        driver.get("https://twitter.com/" + handle)
        driver.set_window_size(1324, 825)
        driver.implicitly_wait(8)
        # driver.find_element(
        # By.CSS_SELECTOR,
        # ".css-1dbjc4n:nth-child(2) > .css-1dbjc4n > .css-18t94o4 > .css-901oao > .css-901oao > .css-901oao",
        # ).click()
        # driver.find_element(
        # By.XPATH,
        # "//div[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/span/span",
        # ).click()
        driver.find_element(By.XPATH, "//div[2]/div/div/div/span/span").click()
    except Exception:
        print(_get_exception_msg())
        return


def main():
    filename = input("[?] The filename of the csv: ") or "input.csv"
    try:
        handles = read_handles(filename)
    except FileNotFoundError:
        print("[?] File not found! Try again...")
        return

    config_file = ConfigParser()
    config_file.read("config.ini")
    settings = config_file["SETTINGS"]

    try:
        username = settings["Username"]
    except KeyError:
        username = input("[?] Twitter Username: ")
    try:
        password = settings["Password"]
    except KeyError:
        password = getpass("[?] Twitter Password for {}: ".format(settings["USERNAME"]))

    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)
    if not login(driver, username, password):
        print("[*] Could not login to Twitter. Check your credentials.")
        return

    for handle in handles:
        print("[*] Following user: {username}... ".format(username=handle), end="")
        follow(driver, handle)
        time.sleep(random.randint(int(settings["Mintime"]), int(settings["Maxtime"])))
        print("Done!")


if __name__ == "__main__":
    main()
