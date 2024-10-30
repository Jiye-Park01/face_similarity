
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm  # tqdm.notebook을 tqdm으로 변경
import os
import urllib.request
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains


search_words = ["IU", "에스파 카리나", "강동원", "이종석", "이준기", "조정석", "에스파 윈터", "트와이스 나연"]


# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")  # GUI 없는 환경에서 사용하기 위해 headless 모드 사용
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
chrome_options.add_argument('--window-size=1920x1080')  # 브라우저 창 크기

# # ChromeDriver의 경로를 자동으로 관리
# service = Service(ChromeDriverManager().install())

# # Chrome 웹드라이버 초기화
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Google 웹사이트 접속
# base_url = "https://www.google.co.kr/imghp"
# driver.get(base_url)
# time.sleep(2)

# PAUSE_TIME = 2

# # 스크롤 함수
# def selenium_scroll_option():
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollBy(0, 5000);")
#         time.sleep(PAUSE_TIME)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height

# # 이미지 검색 및 수집
# img_rst = []

# for search_word in search_words:
#     # 검색 입력
#     browser = driver.find_element(By.NAME, "q")
#     browser.clear()
#     browser.send_keys(search_word + " 사진")
#     browser.submit()

#     # 스크롤을 내려서 더 많은 이미지 로드
#     selenium_scroll_option()

#     # 이미지 요소 수집
#     img_elements = driver.find_elements(By.CLASS_NAME, "YQ4gaf")  # img 요소로 변경

#     for idx, img in enumerate(img_elements):
#         print(f"{search_word} : {idx+1}/{len(img_elements)} proceed...")

#         try:
#             # img.click()
#             # time.sleep(PAUSE_TIME)
            
#             driver.execute_script("arguments[0].scrollIntoView();", img)
#             time.sleep(1)  # 스크롤 후 잠시 대기

#             # ActionChains로 클릭 시도
#             ActionChains(driver).move_to_element(img).click().perform()
#             time.sleep(PAUSE_TIME)

#             # 이미지 src 가져오기
#             img_element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img'))
#             )

#             img_src = img_element.get_attribute('src')
#             img_alt = img_element.get_attribute('alt')

#             img_rst.append({
#                 'alt': img_alt,
#                 'src': img_src
#             })
#             print("big image ok")

#         except Exception as e:
#             print(f"Error: {e}")
#             continue

#     print(f"검색한 키워드 '{search_word}'에 대해 찾은 이미지 개수: {len(img_rst)}")

# # 드라이버 종료
# driver.quit()

# # 이미지 중복 제거
# images_url_df = pd.DataFrame(img_rst)
# unique_urls = images_url_df['src'].unique()

# # 전체 다운로드한 이미지 개수와 중복 제거 후 이미지 개수 출력
# print(f"전체 다운로드한 이미지 개수: {len(img_rst)}")
# print(f"동일한 이미지를 제거한 이미지 개수: {len(unique_urls)}")

# ChromeDriver의 경로를 자동으로 관리
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Google 이미지 검색 페이지 열기
base_url = "https://www.google.co.kr/imghp"
driver.get(base_url)
time.sleep(2)

PAUSE_TIME = 2

# 스크롤 함수 정의
def selenium_scroll_option():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 5000);")
        time.sleep(PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 이미지 수집 리스트
img_rst = []

for search_word in search_words:
    # 검색어 입력
    browser = driver.find_element(By.NAME, "q")
    browser.clear()
    browser.send_keys(search_word + " 사진")
    browser.submit()

    # 스크롤 실행하여 더 많은 이미지 로드
    selenium_scroll_option()

    # 이미지 요소 수집
    img_elements = driver.find_elements(By.CLASS_NAME, "YQ4gaf")

    for idx in range(len(img_elements)):
        print(f"{search_word} : {idx+1}/{len(img_elements)} proceed...")

        try:
            # img 요소를 새로 조회하여 stale 상태 방지
            img_elements = driver.find_elements(By.CLASS_NAME, "YQ4gaf")
            img = img_elements[idx]

            # 이미지 클릭 시도
            driver.execute_script("arguments[0].scrollIntoView(true);", img)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "YQ4gaf"))).click()
            time.sleep(PAUSE_TIME)

            # 큰 이미지의 src 가져오기
            img_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img'))
            )

            img_src = img_element.get_attribute('src')
            img_alt = img_element.get_attribute('alt')

            img_rst.append({
                'alt': img_alt,
                'src': img_src
            })
            print("big image ok")


        except Exception as e:
            print(f"Error: {e}")
            continue

    print(f"검색한 키워드 '{search_word}'에 대해 찾은 이미지 개수: {len(img_rst)}")

# 드라이버 종료
driver.quit()

# 중복 제거
images_url_df = pd.DataFrame(img_rst)
unique_urls = images_url_df['src'].unique()

# 결과 출력
print(f"전체 다운로드한 이미지 개수: {len(img_rst)}")
print(f"동일한 이미지를 제거한 이미지 개수: {len(unique_urls)}")