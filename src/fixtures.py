from selenium import webdriver
import pytest

@pytest.fixture
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome(executable_path=r"chromedriver.exe")
    yield browser

