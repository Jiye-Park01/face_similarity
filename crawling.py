from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 검색할 키워드 입력
query = input('검색할 키워드를 입력하세요: ') + ' 사진'

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# ChromeDriver의 경로를 자동으로 관리
service = Service(ChromeDriverManager().install())

# Chrome 웹드라이버 초기화
driver = webdriver.Chrome(service=service, options=chrome_options)

# Google 웹사이트 접속
url = 'https://www.google.com/'
driver.get(url)
time.sleep(3)

# 검색창에 키워드 입력 후 엔터
search_box = driver.find_element(By.NAME, 'q')  # Google 검색창의 name 속성은 'q'
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(2)

# 폴더 생성
folder_name = query.replace(' ', '_')  # 폴더 이름에 공백이 있을 경우 대체
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# 이미지 탭 클릭
image_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="hdtb-sc"]/div/div/div[1]/div/div[2]/a')))
image_tab.click()
time.sleep(2)

# 스크롤을 통해 이미지 로드
elem = driver.find_element(By.TAG_NAME, 'body')
for _ in range(60):  # Scroll down 60 times
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# 이미지 링크들 가져오기
images = driver.find_elements(By.CSS_SELECTOR, 'img.Q4LuWd')  # 최신 이미지 선택자 사용
links = [image.get_attribute('src') for image in images if image.get_attribute('src') is not None]
print('찾은 이미지의 개수: ', len(links))

# 이미지 다운로드
for k, url in enumerate(links):
    try:
        urllib.request.urlretrieve(url, os.path.join(folder_name, f"{k+1}.jpg"))
    except Exception as e:
        print(f"Error downloading image {k+1}: {e}")

# 크롬 드라이버 종료
driver.quit()

print("크롤링 종료")
