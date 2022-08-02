from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
import time
from datetime import date
import csv
import re

# Als chromedriver niet werkt, nieuwe versie downloaden op https://chromedriver.chromium.org/downloads
# Dan in /usr/local/bin zetten en oude chromedriver verwijderen daar.

months_list = ["aug", "sep", "okt", "nov", "dec", "jan"]
week_days_list = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
length_list = [4, 5, 6, 7, 8, 9, 10]

# TODO:
#   - Mailen
#   - link naar ticket
#   - Specifieke datum

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
    time.sleep(0.5)


# Chooses the departure city
def dep_city_chooser(dep_city):
    # Gets element
    fly_from_box = driver.find_element(by=By.XPATH, value="/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div[1]/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/div/fsw-flight-search-widget-controls-container/fsw-flight-search-widget-controls/div/fsw-input-button/div/input")
    time.sleep(0.25)
    fly_from_box.click()
    fly_from_box.clear()
    time.sleep(0.25)
    fly_from_box.send_keys(dep_city)
    time.sleep(0.25)
    fly_from_box.send_keys(Keys.RETURN)
    time.sleep(0.25)


# Chooses the departure city
def arr_city_chooser(month, length, day):
    # Gets element
    fly_from_box = driver.find_element(by=By.XPATH, value="/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/div/fsw-flight-search-widget-controls-container/fsw-flight-search-widget-controls/div/div/fsw-input-button/div/input")
    time.sleep(0.3)
    fly_from_box.click()
    time.sleep(0.2)
    random_city = driver.find_element(by=By.XPATH, value="/html/body/ry-tooltip/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-destination-container/fsw-airports/fsw-countries/fsw-any-destination-banner/div/div/div/span[1]")
    random_city.click()
    time.sleep(0.2)
    flex_dates(month, length, day)


def flex_dates(month, length, day):
    try:
        time.sleep(0.4)
        flexible_dates = driver.find_element(by=By.XPATH, value="//*[@id='ry-tooltip-9']/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-flexible-datepicker-container/fsw-datepicker-tabs-container/button[2]")
        flexible_dates.click()
    except Exception:
        pass

    time.sleep(0.4)
    month_xpath = "//*[contains(text(),'%s')]" % month
    month_btn = driver.find_element(by=By.XPATH, value=month_xpath)
    month_btn.click()

    length_slider = driver.find_element(by=By.XPATH, value="//*[@id='ry-tooltip-8']/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-flexible-datepicker-container/fsw-flexible-datepicker/div/fsw-flexible-section[2]/div[3]/fsw-range-item/div[1]/input")
    move = ActionChains(driver)
    offset = 21.6 * length - 183
    move.click_and_hold(length_slider).move_by_offset(offset, 0).release().perform()
    time.sleep(0.2)

    day_xpath = "//*[contains(text(),'%s')]" % day
    dep_day = driver.find_element(by=By.XPATH, value=day_xpath)
    dep_day.click()


# Clicks the search button
def search_flights():
    # Gets element
    search_button = driver.find_element(by=By.XPATH, value="/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/div/div/div/button")
    search_button.click()


def get_results(dep_city, month, duration, max_price):

    period_carr = driver.find_element(by=By.XPATH, value="//div[contains(@class,'carousel-container ng-star-inserted')]")
    period_li = period_carr.find_elements(by=By.TAG_NAME, value="li")
    dest_list = []
    for j in range(5):
        try:
            dest_list.append(re.sub("naar", '-', period_li[j].text.splitlines()[0]))
        except Exception:
            pass

    try:
        for i in range(5):
            period_carr = driver.find_element(by=By.XPATH, value="//div[contains(@class,'carousel-container ng-star-inserted')]")
            period_li = period_carr.find_elements(by=By.TAG_NAME, value="li")
            period_li[i].click()
            time.sleep(1)

            # Gets destination cities
            destinations = driver.find_elements(by=By.XPATH, value="//h2[@class='country-card__country h4']")
            destinations_list = [re.sub("[\s][\d][\D]*", '', city.text) for city in destinations]

            # Gets the return price
            non_decimal = re.compile(r'[^\d.]+')
            return_prices = driver.find_elements(by=By.XPATH, value="//span[@class='country-card__price h4']")
            return_prices_list = [float(non_decimal.sub('', price.text)) for price in return_prices]

            today_list = [date.today()] * 7
            departure_list = [dep_city] * 7
            duration_list = [str(duration) + " dagen"] * 7

            period_list = [dest_list[i]] * 7
            data = list(zip(today_list, departure_list, destinations_list, return_prices_list, duration_list, period_list))

            data_to_csv(data, max_price)
    except Exception:
        pass

    return


def accept_cookies():
    try:
        X_button = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[3]/button[2]")
        X_button.click()
    except Exception:
        pass


def data_to_csv(data, max_price):
    with open('csvsryan/aug.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)

        for d in data:
            if d[3] < max_price:
                writer.writerow(list(d))


def run(site_url, dep_city, travel_month, travel_duration, dep_day, max_price):
    # Opens website.
    open_site(site_url)
    # Accepts cookies if asked for.
    accept_cookies()
    # Chooses city of departure.
    dep_city_chooser(dep_city)
    time.sleep(0.2)
    arr_city_chooser(travel_month, travel_duration, dep_day)
    time.sleep(0.3)
    search_flights()
    time.sleep(1)
    get_results(dep_city, travel_month, travel_duration, max_price)


def all_possibilities():
    for month in months_list:
        for length in length_list:
            for day in week_days_list:
                try:
                    run("https://www.ryanair.com/nl/nl", "Eindhoven", month, length, day, 45)
                except Exception as e:
                    print("\nError at month: " + month + ", length: " + str(length) + " days, on: " + day)
                    print(e)


def main():
    # run("https://www.ryanair.com/nl/nl", "Eindhoven", "jul", 6, "maandag", 99.0)
    all_possibilities()

    driver.quit()


if __name__ == '__main__':
    main()
