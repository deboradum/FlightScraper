from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import date
import undetected_chromedriver.v2 as uc
import csv
import re

# TODO:
#   - Mailen
#   - link naar ticket
#   - Als er een error has occured komt opnieuw doen - hoe?

# Initialises driver.
try:
    # Detection avoidance
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    ser = Service("/usr/local/bin/chromedriver")

    driver = webdriver.Chrome(options=options, service=ser)

    # Undetected chrome
    # driver = uc.Chrome(executable_path='/usr/local/bin/chromedriver')
except Exception as e:
    print(e)

return_ticket = "//input[@id='fsc-trip-type-selector-return']"
oneway_ticket = "//input[@id='fsc-trip-type-selector-one-way']"


def open_site(site_url):
    driver.get(site_url)
    time.sleep(5)


# Chooses the departure city
def dep_city_chooser(dep_city):
    # Gets element
    fly_from_box = driver.find_element(by=By.XPATH, value="//input[@id='search-departure-station']")
    fly_from_box.clear()
    time.sleep(0.8)
    fly_from_box.send_keys(' ' + dep_city)
    time.sleep(0.9)
    fly_from_box.send_keys(Keys.RETURN)
    time.sleep(1)


# Clicks the search button
def search_flights():
    # Gets element
    search_button = driver.find_element(by=By.XPATH, value="//button[@class='trip-planner__submit base-button base-button--medium base-button--primary base-button--full-width']")
    search_button.click()


# Chooses the 1-3 days option
def one_to_three_days():
    # Gets element
    duration_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[1]/div/div/input")
    duration_btn.click()
    time.sleep(0.5)
    one_to_three_days_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[3]/ul/li[1]/label/strong")
    one_to_three_days_btn.click()
    time.sleep(0.6)

# Chooses the 4-8 days option
def four_to_eigth_days():
    # Gets element
    duration_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[1]/div/div/input")
    duration_btn.click()
    time.sleep(0.5)
    one_to_three_days_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[3]/ul/li[2]/label")
    one_to_three_days_btn.click()
    time.sleep(0.6)


# Chooses the 1 week option
def one_week():
    duration_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[1]/div/div/input")
    duration_btn.click()
    time.sleep(0.5)
    one_to_three_days_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[3]/ul/li[3]/label/strong")
    one_to_three_days_btn.click()
    time.sleep(0.6)


# Chooses the 9-90 option
def nine_to_ninety_days():
    # Gets element
    duration_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[1]/div/div/input")
    duration_btn.click()
    time.sleep(0.5)
    one_to_three_days_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[3]/ul/li[4]/label/strong")
    one_to_three_days_btn.click()
    time.sleep(0.6)

# Chooses the weekend option
def weekend():
    # Gets element
    duration_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[1]/div/div/input")
    duration_btn.click()
    time.sleep(0.5)
    one_to_three_days_btn = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div/div/div/div[1]/div/form/div[3]/div[3]/ul/li[5]/label/strong")
    one_to_three_days_btn.click()
    time.sleep(0.6)


def get_results(dep_city):
    # Gets destination cities
    destinations = driver.find_elements(by=By.XPATH, value="//h1[@class='heading heading--2 trip-planner-card__title']")
    destinations_list = [city.text for city in destinations]

    # Gets city descriptions
    descriptions = driver.find_elements(by=By.XPATH, value="//p[@class='trip-planner-card__description']")
    descriptions_list = [description.text for description in descriptions]

    # Gets the return price
    non_decimal = re.compile(r'[^\d.]+')
    return_prices = driver.find_elements(by=By.XPATH, value="//h4[@class='heading heading--3']")
    return_prices_list = [float(non_decimal.sub('', price.text)) for price in return_prices]

    # Gets the return price
    dates = driver.find_elements(by=By.XPATH, value="//small[@data-test='trip-planner-card-flight-details-meta']")
    dates_list = [date.text for date in dates]

    today_list = [date.today()] * 5
    departure_list = [dep_city] * 5

    data = list(zip(today_list, departure_list, destinations_list, return_prices_list, dates_list))

    return data


def accept_cookies():
    try:
        X_button = driver.find_element(by=By.XPATH, value="/html/body/div[2]/span/article/div/div/button")
        X_button.click()
    except Exception as e:
        pass


def data_to_csv(data, file):
    with open('csvswizz/'+file+'.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)

        for d in data:
            writer.writerow(list(d))


def get_one_three(dep_city):
    one_to_three_days()
    search_flights()
    ot_data = get_results(dep_city)
    data_to_csv(ot_data, "one_to_three_days")
    time.sleep(2.69)


def get_four_eigth(dep_city):
    four_to_eigth_days()
    search_flights()
    fe_data = get_results(dep_city)
    data_to_csv(fe_data, "four_to_eigth_days")
    time.sleep(2.69)


def get_week(dep_city):
    one_week()
    search_flights()
    ow_data = get_results(dep_city)
    data_to_csv(ow_data, "one_week")
    time.sleep(2.69)


def get_weekend(dep_city):
    weekend()
    search_flights()
    wknd_data = get_results(dep_city)
    data_to_csv(wknd_data, "weekend")
    time.sleep(2.69)


def main():
    open_site("https://wizzair.com/en-gb/flights/trip-planner#/EIN")
    accept_cookies()
    dep_city = "eindhoven"
    dep_city_chooser(dep_city)
    get_one_three(dep_city)
    get_four_eigth(dep_city)
    get_week(dep_city)
    get_weekend(dep_city)


if __name__ == '__main__':
    main()
