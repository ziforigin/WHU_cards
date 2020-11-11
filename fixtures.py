from selenium import webdriver
import pytest


@pytest.fixture
def browser():
    print("\nstart browser for test..")
    System.setProperty("webdriver.chrome.driver", "~/Downloads/WHU_cards/chromedriver")
    browser = webdriver.Chrome()
    yield browser
    print("\nquit browser..")
    browser.quit()
