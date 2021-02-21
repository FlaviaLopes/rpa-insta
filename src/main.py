# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from decouple import config
from time import time
from src.InstaBot import InstaBot


def main():
    begin = time()
    data = {
        'input_user_xpath': '//*[@id="loginForm"]//input[@name="username"]',
        'input_pwd_xpath': '//*[@id="loginForm"]//input[@name="password"]',
        'target_pages': [
            'womentech_',
            'sexting.seguro',
            'women.techmakers',
        ]
    }
    robot = InstaBot()
    robot.driver.maximize_window()
    robot.navigate_to(config('base'))

    robot.login(
        input_user_xpath=data['input_user_xpath'],
        input_pwd_xpath=data['input_pwd_xpath']
    )

    WebDriverWait(
        robot.driver, 1000
    ).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(),"Agora não")]')
        )
    ).click()

    robot.get_followers_from_accounts(data['target_pages'])
    print(f'Total: {round((time() - begin), 2)} s')


if __name__ == '__main__':
    main()
