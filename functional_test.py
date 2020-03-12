from selenium import webdriver

path = "/mnt/c/Users/65848/documents/projects/pytest/geckodriver.exe"
browser = webdriver.Firefox(executable_path=path)
browser.get('http://localhost:8000')

assert 'Django' in browser.title