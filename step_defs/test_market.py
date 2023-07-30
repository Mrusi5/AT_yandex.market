import logging
import random
from pytest_bdd import given, when, then, scenarios
from conftest import browser
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

def check_cap(browser):
    if 'showcaptcha' in browser.current_url:
        element = browser.find_element('id', 'js-button')
        element.click()

scenarios('../features/market.feature')




@given("Открыть браузер и развернуть на весь экран")
def open_browser(browser):
    browser.maximize_window()
    logging.info("Браузер открыт и развернут на весь экран")



@when("Зайти на market.yandex.ru")
def go_to_market(browser):
    browser.get("https://market.yandex.ru/")
    logging.info("Зашел на market.yandex.ru")


@when('В разделе "Каталог → Электроника" выбрать "Смартфоны"')
def select_smartphones(browser):
    check_cap(browser)
    catalog_menu = browser.find_element("xpath", "//button[@id='catalogPopupButton']")
    catalog_menu.click()
    electronics_menu = browser.find_element("xpath", "//a[contains(@href, 'catalog--elektronika') and contains(@class, '_1010X')]")
    ActionChains(browser).move_to_element(electronics_menu).perform()
    smartphones_and_g = browser.find_element("xpath", "//a[contains(@href, 'catalog--smartfony') and contains(@class, 'egKyN _1mqvV _1wg9X')]")
    smartphones_and_g.click()
    logging.info('В разделе "Каталог → Электроника" выбрал "Смартфоны"')

@when('Перейти в "Все фильтры"')
def open_filters(browser):
    check_cap(browser)
    all_filters = browser.find_element("xpath", "//button[@class='_2AMPZ _1N_0H _1ghok']")
    all_filters.click()
    logging.info('Перешел в "Все фильтры"')

@when('Задать параметр поиска до 20000 рублей и Диагональ экрана от 3 дюймов')
def set_filters(browser):
    check_cap(browser)
    price_filter = browser.find_element("xpath", "//input[@class='_2xtC2' and @data-auto='range-filter-input-max']")
    price_filter.clear()
    price_filter.send_keys("20000")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    screen_size_button = browser.find_element("xpath", "//button[@class='_1RgR0' and @aria-controls='14805766']")
    screen_size_button.click()
    screen_size_filter = browser.find_element("xpath", "//div[@id='14805766']/div[@class='_1SfMJ l1f-a']/div[@class='yXKAc _1H_kO' and @data-prefix='от' and @data-tid='db0c1889']/input[@class='_2xtC2' and @data-auto='range-filter-input-min']")
    screen_size_filter.clear()
    screen_size_filter.send_keys("3")
    logging.info('Задал параметр поиска до 20000 рублей и Диагональ экрана от 3 дюймов')
    time.sleep(3)


@when("Выбрать не менее 5 любых производителей")
def select_manufacturers(browser):
    check_cap(browser)
    manufacturers = browser.find_elements("xpath", "//div[@data-filter-id='7893318']/div[@class='_8yOdX']/label[@class='cyT3Q']")
    selected_manufacturers = random.sample(manufacturers, 10)
    selected_manufacturers_names = set()
    res = 0
    for manufacturer in selected_manufacturers:
        if res < 5:
            name = manufacturer.text
            print(name)
            try:
                if name not in selected_manufacturers_names:
                    manufacturer.click()
                    time.sleep(2)
                    selected_manufacturers_names.add(name)
                    res += 1
            except StaleElementReferenceException:
                pass

    logging.info("Выбрано 5 производителей")


@when('Нажать кнопку "Показать"')
def click_show_button(browser):
    check_cap(browser)
    show_button = browser.find_element("xpath", "//a[@class='_2qvOO _3qN-v _1Rc6L']")
    show_button.click()
    logging.info('Нажал кнопку "Показать"')   


@when("Посчитать кол-во смартфонов на одной странице")
def count_smartphones(browser):
    global smartphones
    check_cap(browser)
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    smartphones = browser.find_elements("xpath", "//h3[@class='f0MCF _2tgvL cia-cs']/a[@class='egKyN _2Fl2z']")
    count = len(smartphones)
    logging.info("Посчитал кол-во смартфонов на одной странице")  
    print(f"Количество смартфонов на странице: {count}")
     



@when("Запомнить последний из списка")
def remember_last_smartphone(browser):
    global last_smartphone
    check_cap(browser)
    last_smartphone = smartphones[-1].text
    logging.info("Запомнил последний из списка")
    print(f"Последний смартфон в списке: {last_smartphone}")


@when('Изменить Сортировку на другую (по цене/по рейтингу/по скидке)')
def change_sorting(browser):
    check_cap(browser)
    sorting_dropdown = browser.find_element("xpath", "//button[@data-autotest-id='rorp']")
    sorting_dropdown.click()
    logging.info("Изменил сортировку на другую (по рейтингу)")   
    time.sleep(3)
    

@when('Найти и нажать по имени запомненного объекта')
def click_last_smartphone(browser):
    check_cap(browser)
    found = False
    while not found:
        try:
            check_cap(browser)
            time.sleep(5)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            element = browser.find_element('xpath',f'//img[@alt="{last_smartphone}"]')
            parent_element = element.find_element('xpath', '..')
            pp_element = parent_element.find_element('xpath', '..')
            pp_element.click()
            logging.info("Нашел и нажал по имени запомненного объекта")
            found = True
            time.sleep(3)
        except NoSuchElementException:
            next_page = browser.find_element("xpath", "//span[@class='_3e9Bd']")
            next_page.click()
             


@then("Вывести рейтинг выбранного товара")
def print_rating(browser):
    
    window_handles = browser.window_handles
    browser.switch_to.window(window_handles[-1])
    check_cap(browser)
    time.sleep(5)
    try:
        rating_element = browser.find_element("xpath", "//span[contains(text(), 'Рейтинг')]")
        r_rating_element = rating_element.find_element("xpath", "..")
        rating = r_rating_element.get_attribute("textContent")
        print("Рейтинг выбранного товара:", rating)
        logging.info("Вывел рейтинг выбранного товара")  
    except NoSuchElementException:
        logging.info("Рейтинг выбранного товара не найден")  

    time.sleep(3) 