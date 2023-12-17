from bs4 import BeautifulSoup
from database.database import *
import requests

class Scraper:
  def __init__(self):
    self.section_to_scrap_name = ''
    self.subsection_to_scrap_name = ''
    self.number_of_pages_to_scrap = 0
    self.main_page = requests.get('https://www.prodalit.ru/cat/ProductsRubrics-1')
    self.main_soup = BeautifulSoup(self.main_page.text, 'html.parser')

  def get_book_sections(self):
    elements = self.main_soup.find('div',  class_ = 'tg-widgetcontent').find_all('a', href=True)
    current_data = list()
    for element in elements:
      name_section = element.text
      url_section = 'https://www.prodalit.ru' + element['href']
      current_data.append([name_section, url_section])
      result = get_section_url(cur, name_section)
      if result != 'Пусто':
        continue
      else:
        add_section(cur, conn, name_section, url_section)
    return current_data

  def get_book_subsections(self):
    url_of_page_of_choosed_section = get_section_url(cur, self.section_to_scrap_name)
    page_of_choosed_section = requests.get(url_of_page_of_choosed_section)
    soup = BeautifulSoup(page_of_choosed_section.text, 'html.parser')
    elements = soup.find('div',  class_ = 'tg-widgetcontent').find_all('a', href=True)
    current_data = list()
    for element in elements:
      name_subsection = element.text
      url_subsection = 'https://www.prodalit.ru' + element['href']
      result = get_subsection_url(cur,  name_subsection)
      current_data.append([name_subsection, url_subsection])
      if result != 'Пусто':
        continue
      else:
        add_subsection(cur, conn, name_subsection, url_subsection)
    return current_data

  def get_number_of_pages(self):
    url_of_page_of_choosed_subsection = get_subsection_url(cur, self.subsection_to_scrap_name)
    page_of_choosed_subsection = requests.get(url_of_page_of_choosed_subsection)
    soup = BeautifulSoup(page_of_choosed_subsection.text, 'html.parser')
    number_of_pages = int(soup.find('ul',  class_ = 'pagination').find_all('li')[-2].text)
    return number_of_pages
  
  def get_books(self):
    url_of_page_of_choosed_subsection = get_subsection_url(cur, self.subsection_to_scrap_name)
    current_data = list()
    for i in range(1, self.number_of_pages_to_scrap + 1):
      pattern = f'?PageNumber={i}'
      url_of_i_page_of_choosed_subsection = url_of_page_of_choosed_subsection+pattern
      i_page_of_choosed_subsection = requests.get(url_of_i_page_of_choosed_subsection)
      soup = BeautifulSoup(i_page_of_choosed_subsection.text, 'html.parser')
      elements = soup.find_all('div', class_ = 'tg-postbookcontent')
      for element in elements:
        name = ''
        author = ''
        cost = ''
        url = ''
        try:
          name = element.find('div', class_ = 'tg-booktitle').find('a', href = True).text
        except:
          name = 'Имя не указан'
        try:
          author = element.find('div', class_ = 'tg-bookwriter').text
        except:
          author = 'Автор не указан'
        try:
          cost = element.find('div', class_ = 'tg-bookprice').find_all('div')[0].text[:-5]
        except:
          cost = 'Цена не указана'
        try:
          url = 'https://www.prodalit.ru' + element.find('div', class_ = 'tg-booktitle').find('a', href = True)['href']
        except:
          url = 'Ссылка не указана'
        current_data.append([name, author, cost, url])
        result = get_book(cur, url)
        if result != 'Пусто':
          continue
        else:
          add_book(cur, conn, name, author, cost, url)
    return current_data
  
  def get_database_of_books(self):
    books = get_all_books(cur)
    if len(books) == 0:
      return []
    return books
  
  def clear_database_of_books(self):
    books = get_all_books(cur)
    if len(books) == 0:
      return
    truncate_books(cur, conn)

