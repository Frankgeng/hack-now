from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json, time
# return: list of productIds of this product
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.add_argument("--start-maximized")

def target_id_scraper(productName, num):
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
    browser.get("https://www.target.com/s?searchTerm={0}".format(productName))
    try:
        product_id_list = []
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        waitItem = WebDriverWait(browser, 50).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h2.Heading__StyledHeading-sc-1m9kw5a-0.eZNcif.hideAuxtext"))
        )
        links = browser.find_elements(By.CSS_SELECTOR, "a.Link-sc-1khjl8b-0.kTulu.h-display-block")
        itemUrl_list = []
        for i in range(num):
            itemUrl_list.append(links[i].get_attribute("href"))
        for url in itemUrl_list:
            browser.get(url)
            expandBtn = browser.find_element(
                By.CSS_SELECTOR, "button.Button-bwu3xu-0.kFNHSR")
            expandBtn.click()
            specItems = browser.find_elements(
                By.CSS_SELECTOR, "div.Col-favj32-0.fVmltG.h-padding-h-default div"
            )
            for j in range(len(specItems)):
                num = specItems[j].get_attribute("innerText").split(" ")[-1]
                parts = num.split("-")
                if len(parts) == 3:
                    product_id_list.append("".join(parts))
        return product_id_list
    finally:
        browser.close()


def walmart_id_scraper(productName, num):
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
    browser.get(
        "https://www.walmart.com/search/?query={0}".format(productName))
    product_id_list = []
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    links = WebDriverWait(browser, 50).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.search-result-productimage.gridview.display-block"))
    )
    for i in range(num):
        product_id_list.append(
            links[i].get_attribute("href").split("/")[-1].split("?")[0])
    return product_id_list

def walmart_id_scraper2(productName, num):
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
    browser.get("https://brickseek.com/walmart-inventory-checker/")
    link = browser.find_element(
            By.CSS_SELECTOR, "span.inventory-checker-form__launch-sku-finder.js-link")
    link.click()
    inputBox = browser.find_element(
            By.ID, "sku-finder-form-query")
    inputBox.send_keys(productName)
    inputBox.submit()
    product_id_list = []
    sku_eles = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "sku-finder-form-results__name"))
        )
    for i in range(num):
        product_id_list.append(sku_eles[i].get_attribute("innerText").replace(" ","").split("SKU:")[1])
    return product_id_list

def cvs_id_scraper(productName, num):
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
    browser.delete_all_cookies()
    browser.get(
        "https://www.cvs.com/search/?searchTerm={0}".format(productName))
    try:
        product_id_list = []
        links = WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.css-4rbku5.css-18t94o4.css-1dbjc4n.r-14lw9ot.r-1lz4bg0.r-rs99b7.r-s211iu.r-1loqt21.r-1pi2tsx.r-1udh08x.r-19yat4t.r-1j3t67a.r-1otgn73.r-13qz1uu")
            )
        )
        for i in range(num):
            product_id_list.append(links[i].get_attribute(
                "href").split("/")[-1].split("-")[-1])
        return product_id_list
    finally:
        browser.close()

# return: a dictionary of this object

def cvs_id_scraper2(productName, num):
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
    browser.get("https://brickseek.com/cvs-inventory-checker/")
    link = browser.find_element(
            By.CSS_SELECTOR, "span.inventory-checker-form__launch-sku-finder.js-link")
    link.click()
    inputBox = browser.find_element(
            By.ID, "sku-finder-form-query")
    inputBox.send_keys(productName)
    inputBox.submit()
    product_id_list = []
    sku_eles = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "sku-finder-form-results__name"))
        )
    for i in range(num):
        product_id_list.append(sku_eles[i].get_attribute("innerText").replace(" ","").split("SKU:")[1])
    return product_id_list
    

def brickseek_scraper(productId, _zip, retailer):
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
    browser.get("http://brickseek.com/{0}-inventory-checker/?sku={1}-{2}-{3}".format(
        retailer,
        productId[0:3], productId[3:5], productId[5:9]))
    zipcode = browser.find_element(
        By.CSS_SELECTOR, "#inventory-checker-form-zip")
    zipcode.send_keys(_zip)
    try:
        image = browser.find_element(
            By.CSS_SELECTOR, ".item-overview__image-wrap img"
        )
        product = browser.find_element(
            By.CSS_SELECTOR, "h2.item-overview__title"
        )
        imageUrl = image.get_attribute("src")
        productName = product.get_attribute("innerText").replace('"',"")
    except:
        return {}
    button = browser.find_element(
        By.CSS_SELECTOR, "div.grid__item-content button"
    )
    button.submit()
    shop_list = []
    addr_list = []
    available_list = []
    distance_list = []
    dollar_list = []
    cent_list = []
    price_list = []
    try:
        browser.implicitly_wait(10)
        addr_eles = browser.find_elements(By.CLASS_NAME, "address")
        available_eles = browser.find_elements(
            By.CLASS_NAME, "availability-status-indicator__text"
        )
        distance_eles = browser.find_elements(
            By.CLASS_NAME, "address__below"
        )
        dollar_eles = browser.find_elements(
            By.CLASS_NAME, "price-formatted__dollars"
        )
        cent_eles = browser.find_elements(
            By.CLASS_NAME, "price-formatted__cents"
        )
        for ele in addr_eles:
            addr_list.append(ele.get_attribute("innerText"))
        for ele in available_eles:
            available_list.append(ele.get_attribute("innerText"))
        for ele in distance_eles:
            distance_list.append(ele.get_attribute("innerText"))
        for ele in dollar_eles:
            dollar_list.append(ele.get_attribute("innerText"))
        for ele in cent_eles:
            cent_list.append(ele.get_attribute("innerText"))
        for i in range(len(addr_list)):
            addr_list[i] = addr_list[i].split(
                "\n")[0] + addr_list[i].split("\n")[1]
        for i in range(len(available_list)):
            if available_list[i] == "In Stock":
                available_list[i] = True
            else:
                available_list[i] = False
        for i in range(len(distance_list)):
            distance_list[i] = distance_list[i].replace("(", "").split(" ")[0]
        for i in range(len(dollar_list)):
            price_list.append(str(round(float(dollar_list[i]) + float(cent_list[i]) / 100, 1)))
        return {
            "product_name": productName,
            "product_id": productId,
            "imageUrl": imageUrl,
            "address": addr_list,
            "availability": available_list,
            "distance": distance_list,
            "price": price_list,
            "zipcode" : str(_zip)
        }
    except:
        return {}
    finally:
        browser.close()


def searchWithIds(productName, number, _zip, retailer):
    search_result = []
    product_id_list = []
    if retailer == "walmart":
       product_id_list = walmart_id_scraper2(productName, number)
    elif retailer == "target":
       product_id_list = target_id_scraper(productName, number)
    elif retailer == "cvs":
       product_id_list = cvs_id_scraper2(productName, number)
    for productId in product_id_list:
       print("Search with id: {0}".format(productId))
       search_result.append(brickseek_scraper(productId, _zip, retailer))
    return search_result

def test():
    print(json.dumps(searchWithIds("chips", 5, "90024", "target"), sort_keys=True, indent=4))
    print(json.dumps(searchWithIds("fruit", 5, "90024", "walmart"), sort_keys=True, indent=4))
    print(json.dumps(searchWithIds("water", 5, "90024", "cvs"), sort_keys=True, indent=4))

