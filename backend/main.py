from fastapi import FastAPI, Request
from backend.scraper import Scraper
from fastapi.templating import Jinja2Templates

app = FastAPI()
scraper = Scraper()
templates = Jinja2Templates(directory="./backend/templates")

@app.get("/")
def start(request: Request):
  return templates.TemplateResponse("start.html", {"request" : request})

@app.get("/choose_section_for_scrap")
def choose_section_for_scrap(request: Request):
  sections = scraper.get_book_sections()
  return templates.TemplateResponse("choose_section.html", {"request" : request, "sections" : sections})

@app.get("/{section_to_scrap_name}/choose_subsection_for_scrap")
def choose_subsection_for_scrap(section_to_scrap_name: str, request: Request):
  scraper.section_to_scrap_name = section_to_scrap_name.replace('%20', ' ')
  subsections = scraper.get_book_subsections()
  return templates.TemplateResponse("choose_subsection.html", {"request" : request, "subsections" : subsections})

@app.get("/{subsection_to_scrap_name}/choose_number_of_pages_to_scrap/")
def choose_number_of_pages_to_scrap(subsection_to_scrap_name: str, request: Request):
  scraper.subsection_to_scrap_name = subsection_to_scrap_name.replace('%20', ' ')
  number_of_pages = scraper.get_number_of_pages()
  return templates.TemplateResponse("choose_number_of_pages.html", {"request" : request, "number_of_pages" : number_of_pages})

@app.get('/{number_of_pages_to_scrap}/books')
def get_books(number_of_pages_to_scrap : str, request: Request):
  scraper.number_of_pages_to_scrap = int(number_of_pages_to_scrap)
  books = scraper.get_books()
  return templates.TemplateResponse("books.html", {"request" : request, "books" : books})

@app.get('/database')
def get_database_of_books(request: Request):
  books = scraper.get_database_of_books()
  return templates.TemplateResponse("books.html", {"request" : request, "books" : books})

@app.get('/clear_database')
def clear_database_of_books(request: Request):
  scraper.clear_database_of_books()
  return templates.TemplateResponse("cleared_database.html", {"request" : request})