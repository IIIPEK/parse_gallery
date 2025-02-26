import ssl
import os
import time
import requests
from urllib.parse import unquote, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Проверяем, доступен ли модуль SSL
try:
    ssl.create_default_context()
except AttributeError:
    raise ImportError("Модуль SSL недоступен. Убедитесь, что Python установлен с поддержкой SSL.")

BASE_URL = "http://ru.tekirovadiving.com"
GALLERY_URL = "http://ru.tekirovadiving.com/foto-galereya"

# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Запуск без интерфейса
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def get_gallery_albums():
    """Получает элементы альбомов на странице галереи."""
    driver.get(GALLERY_URL)
    time.sleep(3)  # Ждём загрузки JS
    return driver.find_elements(By.CSS_SELECTOR, "div.fg-album-polaroid a")


def download_images_from_gallery(album_element):
    """Эмулирует клик по альбому и скачивает изображения."""
    ActionChains(driver).move_to_element(album_element).click().perform()
    time.sleep(3)  # Ждём загрузки изображений

    # img_tags = driver.find_elements(By.CSS_SELECTOR, "div.fg-gallery img")
    img_tags = driver.find_elements(By.CSS_SELECTOR, "img.fg-thumb")
    for img in img_tags:
        img_url = img.get_attribute("src")
        if "src=" in img_url:
            img_url = unquote(img_url.split("src=")[1].split("&")[0])  # Декодируем URL
        img_url = urljoin(BASE_URL, img_url)
        download_image(img_url)


def download_image(img_url):
    """Скачивает изображение и сохраняет его в папку."""
    os.makedirs("downloaded_images", exist_ok=True)
    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        filename = os.path.join("downloaded_images", os.path.basename(img_url))
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Скачано: {filename}")
    else:
        print(f"Ошибка загрузки: {img_url}")

def go_back_to_albums():
    """Эмулирует нажатие на кнопку возврата к альбомам."""
    back_button = driver.find_element(By.CSS_SELECTOR, "a.fg-pagination.fg-back-to-albums")
    ActionChains(driver).move_to_element(back_button).click().perform()
    time.sleep(2)  # Ждём возврата к списку галерей


if __name__ == "__main__":
    try:
        gallery_albums = get_gallery_albums()
        for album in gallery_albums:
            print("Открываем галерею...")
            download_images_from_gallery(album)
            go_back_to_albums()
    finally:
        driver.quit()
