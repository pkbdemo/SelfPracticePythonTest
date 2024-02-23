# 從appium套件引用webdriver模組
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('automated_test.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
import time
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
    try:
        credit_card_items = credit_card_menu_content.find_elements(
            By.CLASS_NAME, 'cubre-a-menuLink')
    except Exception as e:
        logger.error(f"Error finding credit card items: {e}")

    # 遍歷所有的信用卡項目
    for item in credit_card_items:
        # 獲取當前項目的文字內容
        item_text = item.text
        # 檢查文字內容是否包含"卡片介紹"
        if "卡片介紹" in item_text:
            # 如果找到，則點擊該項目
            try:
                item.click()
            except Exception as e:
                logger.error(f"Error clicking item: {e}")
            break  # 點擊後退出循環

    # 等待最多20秒，直到網頁載入完成
    WebDriverWait(session_driver,
                  20).until(lambda driver: driver.execute_script(
                      "return document.readyState") == "complete")

    # 等待所有具有"cubre-m-compareCard__title"類別名稱的元素出現
    title_elements = WebDriverWait(session_driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'cubre-m-compareCard__title')))

    # 計算元素數量
    title_count = len(title_elements)

    # 輸出元素數量
    print(f"共有 {title_count} 個信用卡(含停發)。")

    # 等待元素出現並且可以互動
    element = WebDriverWait(session_driver, 20).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            ".cubre-o-slide.-cardList.swiper-container-initialized.swiper-container-horizontal"
        )))

    # 找到所有的切換按鈕
    try:
        pagination_bullets = session_driver.find_elements(
            By.CSS_SELECTOR,
            '.cubre-o-slide.-cardList.swiper-container-initialized.swiper-container-horizontal'
        )
    except Exception as e:
        logger.error(f"Error finding pagination bullets: {e}")

    # 截圖數量計數器
    screenshot_count = 0

    # 遍歷所有的切換按鈕並找到內部的子元素
    for index, bullet in enumerate(pagination_bullets):
        # 在每個切換按鈕內找到特定的子元素
        try:
            credit_cards = bullet.find_elements(By.CLASS_NAME,
                                                'swiper-pagination-bullet')
        except Exception as e:
            logger.error(f"Error finding credit cards within bullet: {e}")
        for card_index, single_card in enumerate(credit_cards):
            single_card.click()
            time.sleep(2)
            try:
                # 進行截圖
                screenshot_path = f'screenShot/credit_card_{index}_{card_index}.png'
                session_driver.get_screenshot_as_file(screenshot_path)
                print(f"Screenshot saved")
            except Exception as e:
                logger.error(f"Error saving screenshot: {e}")
            # 增加截圖數量計數器
            screenshot_count += 1

    # 檢查截圖數量是否與元素查找的數量一致
    if screenshot_count == title_count:
        logger.info("截圖數量與元素查找的數量一致。")
    else:
        logger.info("截圖數量與元素查找的數量不一致。")

    # 關閉瀏覽器
    session_driver.quit()
