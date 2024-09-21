from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import sys
import pandas as pd

option = webdriver.ChromeOptions()
option.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'

service = Service('E:\\engenrring Hema\\Data Engineeing\\python\\web scraping\\learning\\course\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')


browser = webdriver.Chrome(service = service , options = option)

browser.get('https://www.amazon.com/gp/goldbox?ref_=nav_cs_gb&discounts-widget=%2522%257B%255C%2522state%255C%2522%253A%257B%255C%2522refinementFilters%255C%2522%253A%257B%257D%257D%252C%255C%2522version%255C%2522%253A1%257D%2522')

browser.execute_script('window.scrollBy(0,400)')
until = WebDriverWait(browser , 10).until(EC.presence_of_element_located((By.ID , 'nav-logo-sprites')))

productsIndexs = []
productsLinks = []

conatiner = browser.find_elements(By.XPATH , "//div[contains(@class , 'DesktopDiscountAsinGrid')]")[3]
productsBox = conatiner.find_elements(By.XPATH , ".//div[contains(@class , 'GridItem-module__container_PW2gdkwTj1GQzdwJjejN')]")


while productsBox : 
    numProducts = len(productsBox)
    for num in range(len(productsBox)) : 
        product = productsBox.pop(0)
        productIndex = product.get_attribute('data-test-index')
        if productIndex not in productsIndexs :
            productsIndexs.append(productIndex)
            productsLinks.append(product.find_element(By.XPATH , './/a').get_attribute('href'))
    if int(productIndex) > 2: 
        break
    if not productsBox: 
        browser.execute_script('window.scrollBy(0,400)')
        time.sleep(1)
        productsBox = conatiner.find_elements(By.XPATH , ".//div[contains(@class , 'GridItem-module__container_PW2gdkwTj1GQzdwJjejN')]")


productTitle = []
productPrice = []
rating = []
numberRatings = []
numberSoldPastMonth = []
discountPercentage = []
ProductInfo = []

print(len(productsLinks))


for link in productsLinks : 
    browser.get(link)
    try : 
        productTitle.append(browser.find_element(By.ID , 'productTitle').text)
    except Exception as e : 
        productTitle.append("No Title")
    try : 
        # PriceBox = browser.find_element(By.ID , 'apex_offerDisplay_desktop')
        productPrice.append(browser.find_element(By.ID , 'apex_offerDisplay_desktop').text)
    except Exception as e : 
        try : 
            productPrice.append(browser.find_element(By.XPATH , "//span[@data-a-color= 'price']").text)
        except Exception as e : 
            productPrice.append("No Price")
    try : 
        ratingBox = browser.find_element(By.ID , 'averageCustomerReviews')
        rating.append(ratingBox.find_element(By.XPATH , ".//span[@id ='acrPopover']/span/a/span").text)
    except Exception as e : 
        rating.append("No Rating")
    try : 
        numberRatings.append(ratingBox.find_element(By.ID , 'acrCustomerReviewText').text)
    except Exception as e : 
        numberRatings.append("No Nubmer of ratings")
    try : 
        # numberSoldsBox = browser.find_element(By.ID , 'socialProofingAsinFaceout_feature_div')
        numberSold = browser.find_element(By.XPATH , '//div[@id = "socialProofingAsinFaceout_feature_div"]').text
        if numberSold == '' : 
            numberSoldPastMonth.append("No Nubmer of Sold Past Month")
        else : 
            numberSoldPastMonth.append(numberSold)
    except Exception as e : 
        numberSoldPastMonth.append("No Nubmer of Sold Past Month")
    try : 
        discountNumber = browser.find_elements(By.XPATH , "//span[contains(@class ,'a-color-price')]")[1].text
        if discountNumber == '' : 
            discountPercentage.append(0)
        else :
            discountPercentage.append(discountNumber)
    except Exception as e : 
        try : 
            priceBox = browser.find_element(By.ID , 'corePrice_desktop')
            discountNumber = priceBox.find_element(By.XPATH , ".//span[contains(@class ,'a-color-price')]").text
            if discountNumber == '' : 
                discountPercentage.append(0)
            else :
                discountPercentage.append(discountNumber)
        except Exception as e :
            discountPercentage.append(0)
    try :
        infoConatienr = browser.find_element(By.XPATH , ".//div[@id = 'productOverview_feature_div']/div/table")
        infoAll = infoConatienr.find_elements(By.XPATH , ".//tr")
        # making a list to get all info in one list 
        infoAppended = []
        for info in infoAll : 
            infoKey = info.find_element(By.XPATH , ".//td[@class = 'a-span3']").text
            infoValue = info.find_element(By.XPATH , ".//td[@class = 'a-span9']").text
            infoAppended.append({infoKey : infoValue})
        ProductInfo.append(infoAppended)
    except Exception as e : 
        ProductInfo.append('No Information')




df = pd.DataFrame({"Product Indexs" : productsIndexs , "Title" : productTitle , "Price" : productPrice , "Rating" : rating ,
                 "Number of Ratings" : numberRatings , "Number of Sold Past Month" : numberSoldPastMonth ,
                  "Discount Percentage" : discountPercentage , "Product Info" : ProductInfo}
                )


df.to_csv("amazonDailyProducts.csv" , index=False)
