from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from decouple import config
from math import ceil
import pandas as pd
import time
import os
from src.Crawler import Crawler


class InstaBot(Crawler):
    def __init__(self):
        super().__init__()

    def get_followers_from_accounts(self, accounts):
        for account in accounts:
            account_followers = []
            self.navigate_to(config('base') + '/' + account)
            total_followers = self.driver.find_element_by_xpath(
                '//header//li//a[contains(@href, "followers")]//span').text
            if '.' in total_followers:
                total_followers = total_followers.replace('.', '')
            total_followers = int(total_followers)
            try:
                WebDriverWait(
                    self.driver, 10
                ).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//a[contains(@href, "followers")]'))
                ).click()
                modal = self.driver.find_element_by_xpath("//div[@class='isgrP']")
                scroll = 0
                limit_to_scroll = ceil(total_followers / 6)
                while scroll < limit_to_scroll:
                    self.driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', modal)
                    time.sleep(1)
                    scroll += 1

                li_tag_elements = modal.find_elements_by_tag_name('li')

                for element in li_tag_elements:
                    account_followers.append(element.find_element_by_css_selector('a').get_attribute('href'))
                export_users(account, list(account_followers))
            except NoSuchElementException:
                print('Elemento não foi encontrado na página.')
                export_users(account, list(account_followers))

    def follow_user(self, user):
        pass

    def unfollow_user(self, user):
        pass

    def like_fist_post(self, user):
        pass


def export_users(account, data):
    if 'user_accounts.csv' in os.listdir('data'):
        df = pd.read_csv('data/user_accounts.csv')
    else:
        df = pd.DataFrame()
    temp = pd.DataFrame(data={'followers': data})
    temp['account'] = account
    df = pd.concat([
        df,
        temp
    ])
    df.to_csv('data/user_accounts.csv', index=False)
