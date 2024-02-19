# Steam Deal Alert
A program that obtains the names, prices, and discount information of games you want from Steam. If a price drop has been detected or if a deal will end in less than 24hrs, an email will be sent to notify you.

# How to use
- Replace "xxxxxxxx" in the code with your own relevant information
  - sender: a Gmail account that will be sending you the email notification
  - password: personalized app password from the sender Gmail.
    - https://support.google.com/accounts/answer/185833?sjid=8523303725147904486-NA
  - receiver: a Gmail account that will be receiving the email notification
- Running the program
  - Recommend using Windows Task Scheduler(windows) or cronjob(macOS and Linux) to run the program in the background once a day.
    -https://medium.com/analytics-vidhya/easiest-way-to-run-a-python-script-in-the-background-4aada206cf29#:~:text=The%20easiest%20way%20of%20running,can%20use%20Windows%20Task%20Scheduler.&text=You%20can%20then%20give%20the,by%20giving%20the%20time%20particulars.
- Disclaimer: Data will not load for games that require age verification

# What I learned
- Web scraping
  - Beautiful Soup and Requests - very fast and good for scraping static websites but does not work for dynamic websites
    - Does not fetch Javascript content(used by most E-commerce sites)
  - Selenium - can scrape dynamic websites but slow
    - useful when you need to interact with buttons on the site
  - Request-HTML - faster than Selenium and it loads Javascript content but it can't interact with buttons

# Improvements
  -  It might be possible to just use Requests instead of Requests-HTML by analyzing the network tab when loading the page
  -  Could use Selenium instead of Requests-HTML to get data for games that require age verification 

