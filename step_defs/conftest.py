import pytest
from selenium import webdriver
import logging
from selenium.webdriver.chrome.service import Service
from pytest_bdd import scenarios

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

scenarios('../features/market.feature')

@pytest.fixture(scope='session')
def browser():
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_extension('step_defs/User-Agent Switcher for Chrome - Интернет-магазин Chrome 1.1.0.0.crx')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit() 
