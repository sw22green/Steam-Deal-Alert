from bs4 import BeautifulSoup
import time
from email.message import EmailMessage
import ssl
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Amazon links for wishlist items
LINKS = "/Users/Wang/Desktop/WishList Links.txt"
# File that will include product name and price
WRITE_FILE = "/Users/Wang/Desktop/WishList Items and Prices.txt"

def discountChecker():
    """
    Given amazon links in a file, writes out the names and prices of the products
    in a separate file.  If the price of a product has decreased, an email will
    be sent to notify.
    """

    urlList = list(filter(None, readFile(LINKS)))
    dict = {}

    for url in urlList:
        dict.update(checkPrice(url))
    
    clearFile(WRITE_FILE)

    for item in dict:
        writePrices(WRITE_FILE, item, dict[item])

def readFile(file):
    """
    Returns a list where the elements are when a new line is created

    Parameter file(string): the location of the file to be read
    """

    with open(file, "r") as file:
        data = file.read() 
    return data.split('\n')

def checkPrice(url):
    """
    Returns a dictionary containing the name and price of the product from the url.
    Compares the current price to the previous price and sends an email if the current price is lower

    Parameter url(string): the url of the product on amazon
    """
    
    options = Options()
    # Runs chrome without opening browser
    options.add_argument("--headless=new")
    # Removes Navigator.Webdriver Flag
    options.add_argument('--disable-blink-features=AutomationControlled')
    # Using a User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    browser = webdriver.Chrome(options=options)

    browser.get(url)
    html = browser.page_source.encode('utf-8').strip()
    soup1 = BeautifulSoup(html, 'lxml')
    try:
        item = (soup.find(id='title').get_text()).strip()
    except:
        item = "Could not load product name"
    try:
        price = soup.find(id = 'tp_price_block_total_price_ww').find('span', {'class': 'a-offscreen'}).text.strip()
    except:
        price = "Could not load price"
    browser.close()

    itemList = list(filter(None, readFile(WRITE_FILE)))
    if item in itemList: 
        prevPrice = itemList[itemList.index(item) + 1]
        if prevPrice>price: email(url, item, price, prevPrice)

    return {item:price}

def clearFile(file):
    """
    Deletes all the text in the file

    Parameter file(string): the location of the file to be cleared
    """

    f = open(file, 'w')
    f.write("")
    f.close()

def writePrices(file, item, price):
    """
    Writes the name of the item followed by the price in a new line.

    Parameter file(string): the location of the file to write to

    Parameter item(string): the name of the product

    Parameter price(string): the price of the product
    """

    f = open(file, 'a')
    f.write(item+"\n")
    f.write(price+"\n")
    f.write("\n")
    f.close()

def email(url, item, price, prevPrice):
    """
    Sends an email with the link of the product, the product name, the previous price,
    and the current price.

    Parameter url(string): the url of the product

    Parameter item(string): the name of the product

    Parameter price(string): the price of the product

    Parameter prevPrice(string): the price of the product from the last time the program was run
    """

    sender = "sw22green@gmail.com"
    password = "vibxhnfyqpcvmacv"
    receiver = "sw22green@gmail.com"

    subject = "Price Drop!"
    body = url + "\nThe price of " + item + " has dropped from " + prevPrice + " to " + price + "!"

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())

while(True):
    """
    Runs the program once a day
    """

    discountChecker()
    time.sleep(86400)
