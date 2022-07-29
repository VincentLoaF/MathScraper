import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


url = 'https://www.sciencedirect.com/science/article/pii/S2588840421000019'
# url = 'https://www.tuhh.de/MathJax/test/sample-tex.html'
expr_list = []


def parse(url):
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)

    # wait
    wait = WebDriverWait(driver, timeout=10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#MathJax-Element-1-Frame")))

    source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(source, "html.parser")
    return soup


def scrape(soup):
    # found = soup.find_all('script', attrs={'type': 'math/tex; mode=display'})
    # found = soup.find_all('script', attrs={'id': 'MathJax-Element-a'})
    # found = soup.find_all('script', attrs={'id': 'MathJax-Element-1'})
    found = soup.find_all('script', attrs={'id': re.compile(r'^MathJax')})

    if found:
        return_value = True

        for expr in found:
            expr_list.append(expr.string)

        return True

    return False


def get_expressions():
    if expr_list:
        for idx, expr in enumerate(expr_list):
            print('Expression {idx}: {expr}'.format(idx=idx, expr=expr))

    else:
        print('No expressions were scraped')


soup = parse(url)
scrape(soup)
get_expressions()
