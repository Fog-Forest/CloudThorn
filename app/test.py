import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException

from app.services.services import get_driver


def test_baidu_connection():
    try:
        # 启动 Chrome 浏览器
        driver = get_driver()

        # 访问百度
        driver.get('https://www.baidu.com')

        # 获取页面标题
        page_title = driver.title
        print(f"页面标题: {page_title}")

        # 关闭浏览器
        driver.quit()

        return True
    except WebDriverException as e:
        print(f"访问百度时出现错误: {e}")
        return False


if __name__ == "__main__":
    result = test_baidu_connection()
    if result:
        print("成功访问百度！")
    else:
        print("无法访问百度。")
