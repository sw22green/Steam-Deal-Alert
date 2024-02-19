from requests_html import HTMLSession
from email.message import EmailMessage
import smtplib
import ssl
from typing import List, Dict
from datetime import datetime

# Constants for file paths
LINKS_FILE = "project/src/wishlist_games.txt"
WRITE_FILE = "project/src/wishlist_prices.txt"

def discount_checker(links_file: str, write_file: str) -> None:
    """
    Given Steam links in a file, writes out the names, prices, and/or discounts
    of the games in a separate file. If the price of a game has decreased, an
    email will be sent to notify.

    Parameters:
    - links_file (str): Path to the file containing Steam links.
    - write_file (str): Path to the file where game data will be written.
    """
    url_list = list(filter(None, read_file(links_file)))
    game_data = {}

    for url in url_list:
        game_data.update(check_price(url))

    clear_file(write_file)
    write_intro()

    for game_name, game_price in game_data.items():
        write_prices(write_file, game_name, game_price)

def read_file(filename: str) -> List[str]:
    """
    Returns a list where the elements are when a new line is created.

    Parameters:
    - filename (str): The name of the file to be read (including the path).

    Returns:
    - List[str]: List of strings, each element representing a line in the file.
    """
    try:
        with open(filename, "r") as file:
            data = file.read()
        return data.split('\n')
    except FileNotFoundError:
        print(f"File '{filename}' does not exist.")
        return []

def check_price(url: str) -> Dict[str, str]:
    """
    Returns a dictionary containing the name and price of the game from the URL.
    Compares the current price to the previous price and sends an email if the current price is lower.

    Parameters:
    - url (str): The URL of the game on Steam.

    Returns:
    - Dict[str, str]: A dictionary with game name as key and game price as value.
    """
    session = HTMLSession()
    response = session.get(url)
    html = response.html

    game_element = html.find(".apphub_AppName", first=True)
    game_name = game_element.text if game_element else "Failed to get game name"

    price_element = html.find('[data-price-final]', first=True)
    price = float(price_element.attrs['data-price-final']) / 100 if price_element else "Failed to get price"

    discount_countdown_element = html.find('.game_purchase_discount_countdown', first=True)
    discount_countdown = discount_countdown_element.text + ": " if discount_countdown_element else "No discount"

    discount_percent_element = html.find('.discount_pct', first=True)
    discount_percent = discount_percent_element.text if discount_percent_element else ""
    if(discount_countdown == "No discount"): discount_percent = ""

    game_price = f"${price}, {discount_countdown}{discount_percent}"

    game_list = list(filter(None, read_file(WRITE_FILE)))
    if game_name in game_list:
        prev_price = float(game_list[game_list.index(game_name) + 1].split("$")[1][:4])
        if prev_price > price:
            email(url, game_name, game_price, game_list[game_list.index(game_name) + 1])

    return {game_name: game_price}

def clear_file(filename: str) -> None:
    """
    Deletes all the text in the file.

    Parameters:
    - filename (str): The name of the file to be cleared (including the path).
    """
    try:
        with open(filename, 'w') as file:
            file.write("")
    except FileNotFoundError:
        print(f"File '{filename}' does not exist. Unable to clear the file.")

def write_intro() -> None:
    """
    Writes the current date and time to the file.
    """
    with open(WRITE_FILE, 'a') as file:
        file.write(f"Prices as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

def write_prices(filename: str, game_name: str, game_price: str) -> None:
    """
    Writes the name of the game followed by the price in a new line.

    Parameters:
    - filename (str): The name of the file to write to (including the path).
    - game_name (str): The name of the game.
    - game_price (str): The price of the game.
    """

    with open(filename, 'a') as file:
        file.write(f"{game_name}\n{game_price}\n\n")

def email(url: str, game_name: str, game_price: str, prev_price: str) -> None:
    """
    Sends an email with the link of the game, the game name, the previous price,
    and the current price.

    Parameters:
    - url (str): The URL of the game.
    - game_name (str): The name of the game.
    - game_price (str): The price of the game.
    - prev_price (str): The price of the game from the last time the program was run.
    """

    sender = "sw22green@gmail.com"
    password = "vibxhnfyqpcvmacv"
    receiver = "sw22green@gmail.com"
    # For SSL connection
    port = 465

    subject = "Price Drop!"
    body = f"{url}\nThe price of {game_name} has dropped from {prev_price} to {game_price}!"

    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = receiver
    msg['subject'] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())

# Call the main function
discount_checker(LINKS_FILE, WRITE_FILE)
