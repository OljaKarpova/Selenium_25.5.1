import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

@pytest.fixture(autouse=True)
def driver():
   # Инициализируем веб-драйвера
   driver = webdriver.Chrome()
   # Задаем максимальное время ожидания элемента на странице
   driver.implicitly_wait(10)
   # Возвращаем объект драйвера
   yield driver
   # Закрытие браузера после завершения тестов
   driver.quit()

def test_1_all_my_pets(driver):
   # Переходим на главную страницу
   driver.get("https://petfriends.skillfactory.ru/")
   # Нажимаем на кнопку "Зарегистрироваться"
   driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]").click()
   # Нажимаем на ссылку "У меня уже есть аккаунт"
   driver.find_element(By.LINK_TEXT, "У меня уже есть аккаунт").click()
   # Вводим email, предварительно очищая предзаполненное поле
   email = driver.find_element(By.ID, 'email')
   email.clear()
   email.send_keys('ola@mail.ru')
   # Вводим пароль, предварительно очищая предзаполненное поле
   password = driver.find_element(By.ID, 'pass')
   password.clear()
   password.send_keys('000999')
   # Нажимаем на кнопку "Войти"
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проходим по ссылке "Мои питомцы", подключаем явное ожидание этой ссылки
   WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/my_pets"]'))).click()

   # Записываем количество питомцев в соответствии со статистикой пользователя
   pet_number_text = driver.find_element(By.XPATH, "//div[contains(@class, 'col-sm-4 left')]").text
   pet_number_list = re.search(r'Питомцев: (\d+)', pet_number_text)
   pet_number_statistics = int(pet_number_list.group(1))
   # Считаем количество карточек питомцев
   pet_number_cards = len(driver.find_elements(By.CSS_SELECTOR, 'tbody tr'))
   # Сверяем числа
   assert pet_number_statistics == pet_number_cards
   # Выводим результат теста
   print("В профиле пользователя присутствуют все питомцы")

def test_2_pets_photos(driver):
   # Переходим на главную страницу
   driver.get("https://petfriends.skillfactory.ru/")
   # Нажимаем на кнопку "Зарегистрироваться"
   driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]").click()
   # Нажимаем на ссылку "У меня уже есть аккаунт"
   driver.find_element(By.LINK_TEXT, "У меня уже есть аккаунт").click()
   # Вводим email, предварительно очищая предзаполненное поле
   email = driver.find_element(By.ID, 'email')
   email.clear()
   email.send_keys('ola@mail.ru')
   # Вводим пароль, предварительно очищая предзаполненное поле
   password = driver.find_element(By.ID, 'pass')
   password.clear()
   password.send_keys('000999')
   # Нажимаем на кнопку "Войти"
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проходим по ссылке "Мои питомцы", подключаем явное ожидание этой ссылки
   WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/my_pets"]'))).click()
   # Проверяем, что мы оказались на нужной странице
   assert driver.current_url == "https://petfriends.skillfactory.ru/my_pets"

   pets_without_photo = len(driver.find_elements(By.XPATH, '//img[@src=""]'))
   pets_quantity = len(driver.find_elements(By.CSS_SELECTOR, 'tbody tr'))
   # Проверяем, что количество питомцев с фотографиями больше или равно половине общего количества питомцев
   assert pets_without_photo <= pets_quantity / 2
   # Выводим сообщение об успешном выполнении теста
   print("У половины или более карточек питомцев есть фотографии")

def test_3_pets_descriptions(driver):
   # Переходим на главную страницу
   driver.get("https://petfriends.skillfactory.ru/")
   # Нажимаем на кнопку "Зарегистрироваться"
   driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]").click()
   # Нажимаем на ссылку "У меня уже есть аккаунт"
   driver.find_element(By.LINK_TEXT, "У меня уже есть аккаунт").click()
   # Вводим email, предварительно очищая предзаполненное поле
   email = driver.find_element(By.ID, 'email')
   email.clear()
   email.send_keys('ola@mail.ru')
   # Вводим пароль, предварительно очищая предзаполненное поле
   password = driver.find_element(By.ID, 'pass')
   password.clear()
   password.send_keys('000999')
   # Нажимаем на кнопку "Войти"
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проходим по ссылке "Мои питомцы", подключаем явное ожидание этой ссылки
   WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/my_pets"]'))).click()
   # Проверяем, что мы оказались на нужной странице
   assert driver.current_url == "https://petfriends.skillfactory.ru/my_pets"

   pets = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr")
   for i in pets:
      names = i.find_element(By.XPATH, "./td[2]")
      ages = i.find_element(By.XPATH, "./td[4]")
      breeds = i.find_element(By.XPATH, "./td[3]")

      pet_name = names.text.strip()
      pet_age = ages.text.strip()
      pet_breed = breeds.text.strip()

      assert pet_name != "", "У питомца отсутствует имя"
      assert pet_age != "", "У питомца отсутствует возраст"
      assert pet_breed != "", "У питомца отсутствует порода"

   # Вывод сообщения об успешном результате выполнения теста
   print("У всех питомцев есть имя, возраст и порода")


def test_4_unique_pet_names(driver):
   # Переходим на главную страницу
   driver.get("https://petfriends.skillfactory.ru/")
   # Нажимаем на кнопку "Зарегистрироваться"
   driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]").click()
   # Нажимаем на ссылку "У меня уже есть аккаунт"
   driver.find_element(By.LINK_TEXT, "У меня уже есть аккаунт").click()
   # Вводим email, предварительно очищая предзаполненное поле
   email = driver.find_element(By.ID, 'email')
   email.clear()
   email.send_keys('ola@mail.ru')
   # Вводим пароль, предварительно очищая предзаполненное поле
   password = driver.find_element(By.ID, 'pass')
   password.clear()
   password.send_keys('000999')
   # Нажимаем на кнопку "Войти"
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проходим по ссылке "Мои питомцы", подключаем явное ожидание этой ссылки
   WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/my_pets"]'))).click()
   # Проверяем, что мы оказались на нужной странице
   assert driver.current_url == "https://petfriends.skillfactory.ru/my_pets"

   pet_name_elements = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[1]")
   pet_names = []
   for element in pet_name_elements:
      pet_name = element.text.strip()
      pet_names.append(pet_name)

   assert len(set(pet_names)) == len(pet_names), "Найдены повторяющиеся имена питомцев"

   # Вывод сообщения об успешном результате выполнения теста
   print("У всех питомцев уникальные имена")


def test_5_unique_pets(driver):
   # Переходим на главную страницу
   driver.get("https://petfriends.skillfactory.ru/")
   # Нажимаем на кнопку "Зарегистрироваться"
   driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]").click()
   # Нажимаем на ссылку "У меня уже есть аккаунт"
   driver.find_element(By.LINK_TEXT, "У меня уже есть аккаунт").click()
   # Вводим email, предварительно очищая предзаполненное поле
   email = driver.find_element(By.ID, 'email')
   email.clear()
   email.send_keys('ola@mail.ru')
   # Вводим пароль, предварительно очищая предзаполненное поле
   password = driver.find_element(By.ID, 'pass')
   password.clear()
   password.send_keys('000999')
   # Нажимаем на кнопку "Войти"
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проходим по ссылке "Мои питомцы", подключаем явное ожидание этой ссылки
   WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/my_pets"]'))).click()
   # Проверяем, что мы оказались на нужной странице
   assert driver.current_url == "https://petfriends.skillfactory.ru/my_pets"

   pet_elements = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr")
   pets = []
   for element in pet_elements:
      pet_name = element.text.strip()
      pets.append(pet_name)

   assert len(set(pets)) == len(pets), "Найдены повторяющиеся питомцы"

   # Вывод сообщения об успешном результате выполнения теста
   print("Все питомцы уникальны")