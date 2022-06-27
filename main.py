import aita_reddit_stories
import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    aita_reddit_stories.main_func("AmITheAsshole", "month")

