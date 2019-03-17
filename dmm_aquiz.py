import sys
import os
import pandas
import glob
import re
import traceback
import random
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def access_page():
    """
    description : dmm クイズ買取のサイトにアクセスする
    """
    rtn = False

    # 環境変数からchromedriverのパスを取得取得
    environ = os.environ
    MAIL = environ['MAIL']
    PASS = environ['PASS_AQUIZ']
    CHROME_DRIVER_PATH = environ['CHROME_DRIVER_PATH']
    URL_BASE = "https://aquiz.org/answers"  # economy
    URL_BASE = "https://aquiz.org/session/new"
    URL_TEC = "https://aquiz.org/categories/211"
    WAIT_SEC = 10

    try:
        # //////////////////////////////////
        # // chrome driver
        # //////////////////////////////////
        # prefs = {"download.default_directory": dl_dir}   # ダウンロード先設定
        # chop.add_experimental_option("prefs", prefs)
        # chop.add_argument('--ignore-certificate-errors')  # SSL対策
        # chop.add_argument('--headless') # headless 設定
        # chop.add_argument('--disable-gpu') # gpu error 対策
        # chop.add_argument('--window-size=1024,1000')
        # chop.add_argument('--disable-extensions')
        # chromeドライバ取得
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

        driver.get(URL_BASE)
        driver.implicitly_wait(WAIT_SEC)
        # -------------------
        # Login
        # -------------------
        driver.find_element_by_xpath(
            '/html/body/main/div/div/div/form/div[1]/input'
            ).send_keys(MAIL)
        driver.find_element_by_xpath(
            '/html/body/main/div/div/div/form/div[2]/input'
        ).send_keys(PASS)
        driver.find_element_by_xpath(
            '/html/body/main/div/div/div/form/div[3]/input'
        ).click()

        # ------------------
        # 画面遷移
        # ------------------
        # クイズ回答
        li_num = random.randint(1, 8)
        xpath = '/html/body/main/ul/li[{}]/a'.format(li_num)

        driver.find_element_by_xpath(
            '/html/body/main/ul[2]/li[1]/a'
            ).click()
        driver.find_element_by_xpath(
            xpath
        ).click()
        driver.find_element_by_xpath(
            '/html/body/main/ul/li[5]/a'
        ).click()
        driver.find_element_by_xpath(
            '/html/body/main/ul/li/div/a'
        ).click()
        driver.implicitly_wait(WAIT_SEC)
        # 現在のURLを取得
        cur_url = driver.current_url
        # 現在のURLが'sorry?type=done'を含む場合
        if cur_url.find('sorry?type=done') > -1:
            sleep(2)
            driver.close()
            return "End"

        # ------------------
        # 回答
        # ------------------
        count = 10000
        xpath_select = 1
        xpath_get_1y = 1
        for i in range(count):
            el_num = 0
            WAIT_SEC = random.randint(1, 4)
            # ------------------
            # 要素数取得
            # ------------------
            text_contents = [el.text for el in driver.find_elements_by_xpath('//*[@id="select-list"]/li')]
            for i in text_contents:
                el_num += 1
            try:
                # 回答を選択
                if xpath_select == 1:
                    sel_num = random.randint(1, el_num)
                    driver.find_element_by_xpath(
                        '//*[@id="select-{}"]'.format(sel_num)
                    ).click()

                if xpath_select == 2:
                    driver.find_element_by_xpath(
                       '//*[@id="select-list"]/li[1]'
                    )

                # 次のクイズへ
                if xpath_get_1y == 1:
                    driver.find_element_by_xpath(
                        '//*[@id="next-question"]/a'
                    ).click()
                if xpath_get_1y == 2:
                    driver.find_element_by_xpath(
                        '//*[@id="next-question"]'
                    ).click()
                driver.implicitly_wait(WAIT_SEC)
                # 現在のURLを取得
                cur_url = driver.current_url
                # 現在のURLが'complete'を含む場合
                if cur_url.find('complete') > -1:
                    sleep(2)
                    driver.find_element_by_xpath(
                        '/html/body/main/div/div[2]/a[2]'
                    ).click()

                xpath_select = 1
                xpath_get_1y = 1
            except NoSuchElementException:
                xpath_select += 1
                xpath_get_1y += 1
                sleep(1)
            except StaleElementReferenceException:
                driver.implicitly_wait(WAIT_SEC)
                sleep(1)
        rtn = True
    except:
        traceback.print_exc()
        rtn = False
        # クローズ処理
        driver.close()

    return rtn

# //////////////////////////////
# // main process
# //////////////////////////////
if __name__ == '__main__':

    for i in range(100):
        if access_page() == "End":
            break
