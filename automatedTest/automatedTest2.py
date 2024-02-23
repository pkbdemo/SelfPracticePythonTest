# 從appium套件引用webdriver模組
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import os
os.makedirs('logs', exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# 創建logger實例
logger = logging.getLogger(__name__)
log_file_path = os.path.join('logs', 'automated_test.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
# 定義desired_caps變數
desired_caps = dict()

#安卓設置
desired_caps = {
    'platformName': 'Android',  # 平台名
    'platformVersion': '8.1.0',  # 版本
    'deviceName': '192.168.232.2:5554',  # 設備名
    'browserName': 'Chrome',  # 瀏覽器
    'autoGrantPermissions': True  # 賦予權限
}
#IOS設置
# desired_caps = {
#     'platformName': 'iOS',  # 平台名
#     'platformVersion': '14.0',  # 版本
#     'deviceName': 'iPhone 12', # 設備名
#     'browserName': 'Chrome', # 瀏覽器
#     'autoGrantPermissions': True,
# }

try:
    session_driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                      desired_caps)
except Exception as e:
    logger.error(f"Error creating webdriver session: {e}")
    session_driver = None  # 確保session_driver在這裡被定義，即使在try區塊中沒有成功創建
    # 等待最多20 秒，直到網頁載入完成
    WebDriverWait(session_driver,
                  20).until(lambda driver: driver.execute_script(
                      "return document.readyState") == "complete")
logger.info("Opening Chrome browser.")
# 打開Chrome瀏覽器
if session_driver is not None:
    session_driver.get('https://www.cathaybk.com.tw/cathaybk/')
    # 等待網頁載入完成
    WebDriverWait(session_driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'cubre-a-burger')))
    logger.info("Chrome browser opened successfully.")
    try:
        # 點擊"個人金融"菜單項目
        personal_finance_menu = session_driver.find_element(
            By.CLASS_NAME, 'cubre-a-burger')
        personal_finance_menu.click()
    except Exception as e:
        logger.error(f"Error finding or clicking the personal finance menu: {e}")

    # 等待"產品介紹"項目載入完成
    WebDriverWait(session_driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH,
            '//div[contains(@class, "cubre-a-menuSortBtn -l1") and text()="產品介紹"]'
        )))

    try:
        #  使用 XPath 找到"產品介紹"的元素
        product_introduction_menu = session_driver.find_element(
            By.XPATH,
            '//div[contains(@class, "cubre-a-menuSortBtn -l1") and text()="產品介紹"]'
        )
        product_introduction_menu.click()
    except Exception as e:
        logger.error(f"Error finding or clicking the product introduction menu: {e}")

    # 等待"信用卡"項目載入完成
    WebDriverWait(session_driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//div[contains(@class, "cubre-a-menuSortBtn") and text()="信用卡"]'
             )))

    # 找到"信用卡"項目並點擊
    try:
        credit_card_menu = session_driver.find_element(
            By.XPATH,
            '//div[contains(@class, "cubre-a-menuSortBtn") and text()="信用卡"]')
        credit_card_menu.click()
    except Exception as e:
        logger.error(f"Error finding or clicking the credit card menu: {e}")

    #  等待"信用卡"明細載入完成
    WebDriverWait(session_driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.cubre-o-menuLinkList__item.is-L2open')))

    # 找到所有的"信用卡"明細項目
    try:
        credit_card_menu_content = session_driver.find_element(
            By.CSS_SELECTOR, '.cubre-o-menuLinkList__item.is-L2open')
    except Exception as e:
        logger.error(f"Error finding the credit card menu content: {e}")

    # 在這個父元素內部找到所有具有"cubre-a-menuLink"類別名稱的元素
    credit_card_items = credit_card_menu_content.find_elements(
        By.CLASS_NAME, 'cubre-a-menuLink')

    # 計算並logging"信用卡"菜單裡面的項目數量
    logger.info(f"信用卡菜單裡面有 {len(credit_card_items)} 個項目。")

    # 進行截圖
    try:
        screenshot_path = 'screenShot/creditCardMenuList.png'
        session_driver.get_screenshot_as_file(screenshot_path)
        print(f"Screenshot saved")
    except Exception as e:
        logger.error(f"Error saving screenshot: {e}")

    # 關閉瀏覽器
    session_driver.quit()
