from requests_html import HTMLSession
from email.message import EmailMessage
import ssl
import smtplib


# Steam links for wishlist games
LINKS_FILE = "/Users/Wang/Desktop/WishList Links.txt"
# File that will include game name and price
WRITE_FILE = "/Users/Wang/Desktop/WishList Games and Prices.txt"

def discountChecker(linksFile, writeFile):
    """
    Given steam links in a file, writes out the names, prices, and/or discount 
    of the games in a separate file.  If the price of a game has decreased, an 
    email will be sent to notify.
    """

    urlList = list(filter(None, readFile(linksFile)))
    dict = {}

    for url in urlList:
        dict.update(checkPrice(url))
    
    clearFile(writeFile)

    for game in dict:
        writePrices(writeFile, game, dict[game])

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
    Returns a dictionary containing the name and price of the game from the url.
    Compares the current price to the previous price and sends an email if the current price is lower

    Parameter url(string): the url of the game on steam
    """
    session = HTMLSession()
    response = session.get(url)
    html = response.html
    
    gameName = html.find(".apphub_AppName", first = True).text

    priceElement = html.find('[data-price-final]', first = True)
    price = float(priceElement.attrs['data-price-final'])/100

    discountCountdownElement = html.find('.game_purchase_discount_countdown', first = True)
    if(discountCountdownElement is None): discountCountdown = "No discount"
    else: discountCountdown = discountCountdownElement.text + ": "

    discountPercentElement = html.find('.discount_pct', first = True)
    if(discountPercentElement is None): discountPercent = ""
    else: discountPercent = discountPercentElement.text
    
    gamePrice = "$" + str(price) + ", " + discountCountdown + discountPercent

    gameList = list(filter(None, readFile(WRITE_FILE)))
    if gameName in gameList: 
        prevPrice = gameList[gameList.index(gameName) + 1]
        prevPrice = float(prevPrice[prevPrice.index("$")+1: prevPrice.index(".")+3])
        if prevPrice>price: email(url, gameName, price, prevPrice)

    return {gameName:gamePrice}

def clearFile(file):
    """
    Deletes all the text in the file

    Parameter file(string): the location of the file to be cleared
    """

    f = open(file, 'w')
    f.write("")
    f.close()

def writePrices(file, game, price):
    """
    Writes the name of the game followed by the price in a new line.

    Parameter file(string): the location of the file to write to

    Parameter game(string): the name of the game

    Parameter price(string): the price of the game
    """

    f = open(file, 'a')
    f.write(game+"\n")
    f.write(price+"\n")
    f.write("\n")
    f.close()

def email(url, game, price, prevPrice):
    """
    Sends an email with the link of the game, the game name, the previous price,
    and the current price.

    Parameter url(string): the url of the game

    Parameter game(string): the name of the game

    Parameter price(string): the price of the game

    Parameter prevPrice(string): the price of the game from the last time the program was run
    """

    sender = "sw22green@gmail.com"
    password = "vibxhnfyqpcvmacv"
    receiver = "sw22green@gmail.com"

    subject = "Price Drop!"
    body = url + "\nThe price of " + game + " has dropped from " + prevPrice + " to " + price + "!"

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())    

discountChecker(LINKS_FILE, WRITE_FILE)
