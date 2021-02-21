from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from decouple import config


class Crawler:
    """
      |  Classe genérica de web crawler.
      |
      |   Atributos
      |  ----------
      |  driver : selenium.webdriver.Chrome
      |     Driver Chrome responsável por gerenciar, automatizar ações de
      |     navegação web usando o Chrome browser.
      |     Permite maior interação com a página e recuperar elementos de
      |     carregamento dinâmico.
      |
      |  ----------
      |
      |   Métodos
      |  ----------
      |     navigate_to(url)
      |     login(input_user_xpath, input_pwd_xpath)
      """

    def __init__(self):
        self.driver = Chrome(executable_path=config('chromedriver_path'))

    def navigate_to(self, url):
        self.driver.get(url)

    def login(self, input_user_xpath, input_pwd_xpath):
        try:
            WebDriverWait(
                self.driver, 10
            ).until(
                EC.element_to_be_clickable(
                    (By.XPATH, input_user_xpath))
            ).send_keys(config('user'))

            input_pwd = self.driver.find_element_by_xpath(input_pwd_xpath)
            input_pwd.send_keys(config('pwd'))
            input_pwd.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print('elemento não encontrado.')
