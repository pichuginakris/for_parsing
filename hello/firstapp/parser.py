import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys



def write_csv_vk_parser_header():  # обновляет файл, добавляя в него заголовки
    with open('vk_parser.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Адрес группы', 'Сообщество', 'Номер телефона сообщества', 'Ссылка на сообщество', 'Наименование товара', 'Ссылка на товар',
                         'Цена товара', 'Изображение товара', 'Дата добавления товара'))


def write_csv_vk_parser(data):  # записывает данные в файл csv
    with open('vk_parser.csv', 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        row = (data['address'], data['group'], data['phone'], data['group_ref'], data['product_name'], data['product_ref'], data['product_price'], data['image'], data['time'])
        writer.writerow(row)


def write_csv_not_sorted_header():  # обновляет файл, добавляя в него заголовки
    with open('vk_parser_not_sorted.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Город', 'Улица', 'Сообщество', 'Номер телефона сообщества', 'Ссылка на сообщество',
                         'Наименование товара', 'Ссылка на товар', 'Цена товара', 'Изображение товара',
                         'Дата добавления товара'))


def write_sorted_csv_header():  # обновляет файл, добавляя в него заголовки
    with open('vk_parser_sorted.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Город', 'Улица', 'Сообщество', 'Номер телефона сообщества', 'Ссылка на сообщество',
                         'Информация о товарах'))


def write_csv_not_sorted(data):  # записывает данные в файл csv
    with open('vk_parser_not_sorted.csv', 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        row = (data['city'], data['street'], data['group'], data['phone'], data['group_ref'],
               data['product_name'], data['product_ref'], data['product_price'], data['image'], data['time'])
        writer.writerow(row)


def write_sort(sorted_list):  # записывает в файл отсортированный список
    write_sorted_csv_header()
    with open('vk_parser_sorted.csv', 'a', encoding='utf8', newline='') as file:
        i = 0
        while i < (len(sorted_list)):
            product_number = 1
            product_info = 'Товар №' + str(product_number) + ' Наименование товара: ' + str(sorted_list[i]['Наименование товара']) + ' Ссылка на товар: ' + str(sorted_list[i]['Ссылка на товар']) + ' Цена товара: ' + str(sorted_list[i]['Цена товара']) + ' Изображение товара: ' + str(sorted_list[i]['Изображение товара']) + ' Дата добавления товара: ' + str(sorted_list[i]['Дата добавления товара'])
            while (i < (len(sorted_list)-2)) and (sorted_list[i]['Сообщество'] == sorted_list[i+1]['Сообщество']):  # проверяет повтор имени в списке
                i = i + 1
                product_number = product_number + 1
                product_info = product_info + ' Товар №' + str(product_number) + ' Наименование товара: ' + str(sorted_list[i+1]['Наименование товара']) + ' Ссылка на товар: '+ str(sorted_list[i+1]['Ссылка на товар']) + ' Цена товара: ' + str(sorted_list[i+1]['Цена товара']) + ' Изображение товара: ' + str(sorted_list[i+1]['Изображение товара']) + ' Дата добавления товара: ' + str(sorted_list[i+1]['Дата добавления товара'])
                if i > (len(sorted_list)-2):
                    i = i - 1
            writer = csv.writer(file)
            writer.writerow((sorted_list[i]['Город'], sorted_list[i]['Улица'], sorted_list[i]['Сообщество'],
                             sorted_list[i]['Номер телефона сообщества'], sorted_list[i]['Ссылка на сообщество'],
                             str(product_info)))
            i = i + 1


def read_vk_parser_csv():  # сортирует полученный список по имени и городу
    with open('vk_parser.csv', encoding='utf8') as f:
        fieldnames = ['address', 'group', 'phone', 'group_ref', 'product_name', 'product_ref', 'product_price', 'image', 'time']
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            lst = row['address'].split(',')
            city = lst[len(lst)-1]
            i = 0
            street = ''
            for i in range(len(lst)-1):
                street = street + lst[i]
            data = {
                'city': city,
                'street': street,
                'group': row['group'],
                'phone': row['phone'],
                'group_ref': row['group_ref'],
                'product_name': row['product_name'],
                'product_ref': row['product_ref'],
                'product_price': row['product_price'],
                'image': row['image'],
                'time': row['time'],
            }
            if data['city'] != 'Адрес группы':
                write_csv_not_sorted(data)


def read_and_sort_csv():  # сортирует полученный список по имени и городу
    with open('vk_parser_not_sorted.csv', encoding='utf8') as f:
        reader = csv.DictReader(f)
        sorted_list = sorted(reader, key=lambda row: (row['Сообщество']), reverse=False)
        sorted_list = sorted(sorted_list, key=lambda row: (row['Город']), reverse=False)
    write_sort(sorted_list)



def main_prod(categories_input, city_input):

    login = '+79919024639'
    password = 'd81d7kR6'
    url = 'https://vk.com/market' + '?city=2&country=1&groups=1&sort=1010&q='

    try:
        categories_input = categories_input.split(' ')
        for category_input in categories_input:
            url = url + category_input + '%20'
        driver = webdriver.Chrome()
        driver.get(url)
    except:
        return 'Неверно введены данные'

    try:
        inputElement_mail = driver.find_element_by_id('email')
        inputElement_pass = driver.find_element_by_id('pass')
        inputElement_pass.send_keys(password)
        inputElement_mail.send_keys(login)
        inputElement_pass.send_keys(Keys.ENTER)
        inputElement_mail.send_keys(Keys.ENTER)
        time.sleep(1)
        inputElement_city = driver.find_element_by_xpath(
            "//div[@id='cCity']/div[@id='container4']/table/tbody/tr/td[@class='selector']/input[@type='text']").clear()
        time.sleep(1)
        inputElement_city = driver.find_element_by_xpath(
            "//div[@id='cCity']/div[@id='container4']/table/tbody/tr/td[@class='selector']/input[@type='text']").send_keys(city_input)
        time.sleep(1)
        inputElement_city = driver.find_element_by_xpath(
            "//div[@id='cCity']/div[@id='container4']/table/tbody/tr/td[@class='selector']/input[@type='text']").send_keys(Keys.ENTER)
        time.sleep(1)
        SCROLL_PAUSE_TIME = 1  # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:  # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)  # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(1)
        source = driver.page_source
        soup = BeautifulSoup(source, 'lxml')
    except:
        return 0
    not_found = soup.find('div', id_='not_found')

    row_names = soup.find_all('div', class_='market_row_inner_cont')
    write_csv_vk_parser_header()
    just_for_fun = 0
    beginning = 'Всего найдено ' + str(len(row_names)) + ' товаров.'
    seconds = len(row_names) * 3
    minutes = seconds // 60
    seconds = seconds % 60
    worktime = 'Примерное работа программы: ' + str(minutes) + ' мин. ' + str(seconds) + ' сек.'

    for obj in row_names:
        just_for_fun = just_for_fun + 1
        print('Товар №' + str(just_for_fun))
        product_name = obj.find('div', class_='market_row_name').text
        product_price = obj.find('div', class_='market_row_price').text
        group_name = obj.find('div', class_='market_row_user').text
        group_reference = obj.find('div', class_='market_row_user').find('a').get('href')
        dat = obj.find('div', class_='market_row_time').text
        image = obj.find('img', class_='market_row_img').get('src')
        image_ref = obj.find('div', class_='market_row_photo bordered-thumb').find('a').get('href')
        group_reference = 'https://vk.com' + str(group_reference)
        image_reference = 'https://vk.com/market' + str(image_ref)
        time.sleep(1)

        driver.get(group_reference)
        try:
            source2 = driver.page_source
        except:
            return 0
        soup2 = BeautifulSoup(source2, 'lxml')
        try:
            group_address = soup2.find('div', class_="group_info_row address").find('a').text
        except:
            group_address = 'Не указан в сообществе'
        try:
            phone = soup2.find('div', class_="group_info_row phone").find('a').text
        except:
            phone = 'Не указан в сообществе'

        data = {'address': group_address,
                'group': group_name,
                'phone': phone,
                'group_ref': group_reference,
                'product_name': product_name,
                'product_ref': image_reference,
                'product_price': product_price,
                'image': image,
                'time': dat
                }
        write_csv_vk_parser(data)

    write_csv_not_sorted_header()
    read_vk_parser_csv()
    read_and_sort_csv()
    return ('Конец работы программы. Можете скачать или просмотреть полученный файл')


