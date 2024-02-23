# 從appium套件引用webdriver模組
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
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
    # 等待最多20秒，直到網頁載入完成
    WebDriverWait(session_driver,
                  20).until(lambda driver: driver.execute_script(
                      "return document.readyState") == "complete")
logger.info("Opening Chrome browser.")
# 打開Chrome瀏覽器
if session_driver is not None:
    session_driver.get('https://www.cathaybk.com.tw/cathaybk/')
    # 等待最多20秒，直到網頁載入完成
    WebDriverWait(session_driver,
                  20).until(lambda driver: driver.execute_script(
                      "return document.readyState") == "complete")
    logger.info("Chrome browser opened successfully.")
    # 進行截圖
    try:
        screenshot_path = 'screenShot/bankHome.png'
        session_driver.get_screenshot_as_file(screenshot_path)
        print(f"Screenshot saved")
    except Exception as e:
        logger.error(f"Error saving screenshot: {e}")

    # 關閉瀏覽器
    session_driver.quit()
