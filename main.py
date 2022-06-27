import aita_reddit_stories
import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    aita_reddit_stories.main_func("AmITheAsshole", "month")
    # driver = webdriver.Chrome('/Users/adityarathi/PycharmProjects/RedditTok/chromedriver')
    # driver.get('https://www.tiktok.com/login')  # Manually login
    # time.sleep(50)
    # driver.get('https://www.tiktok.com/upload/?lang=en') # go on main page
    # time.sleep(3)
    #
    # driver.quit()

