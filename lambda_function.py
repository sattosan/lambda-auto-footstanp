import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

def facebookLogin(driver):
    # Facebookログインボタンをクリック
    driver.find_element_by_xpath('//*[@id="registerBtn1"]').click()
    # Facebookログインページにフォーカス
    driver.switch_to.window(driver.window_handles[-1])
    # メールアドレスとパスワードの入力
    driver.find_element_by_name("email").send_keys(os.environ['EMAIL'])
    driver.find_element_by_name("pass").send_keys(os.environ['PASS'])
    # どこかクリックしないと送信ボタンが押せないので，適当に押す
    driver.find_element_by_xpath('//*[@id="email_container"]/div/label').click()
    # ログインボタンをクリック
    driver.find_element_by_xpath('//*[@id="u_0_0"]').click()
    # ログイン後，メインページにフォーカスを戻す
    driver.switch_to.window(driver.window_handles[0])

def execFootStanp(driver, n):
    print(f"=========={n}人に足跡をつけます==========")
    # n人に到達するまで繰り返す（足跡間隔はランダムで3〜4秒の間）
    for i in range(1, n+1):
        driver.get(f"https://pairs.lv/#/search/one/{i}")
        time.sleep(random.randint(3,5))
        print(f"{i}人目に足跡ぺた〜")
    print(f"=========={n}人に足跡をつけました==========")

def lambda_handler(event, context):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--v=99")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")
    options.binary_location = "./bin/headless-chromium"

    # Headless Chromeブラウザに接続
    driver = webdriver.Chrome(
        "./bin/chromedriver", chrome_options=options)
    try:
        # seleniumの動作タイムアウトを10秒間に設定
        driver.implicitly_wait(10)
        # pairsのログインページ遷移
        driver.get("https://pairs.lv/#/login")
        # facebookを使ってログイン
        facebookLogin(driver)
        # 自動足跡を実行
        execFootStanp(driver, 100)
    # 例外処理
    except ElementClickInterceptedException as ecie:
        print(f"exception!\n{ecie}")
    except TimeoutException as te:
        print(f"timeout!\n{te}")
    except KeyboardInterrupt:
        print("\napp shutdown!")
    finally:
        # 終了
        driver.close()
        driver.quit()

    return


if __name__ == "__main__":
    lambda_handler(None, None)