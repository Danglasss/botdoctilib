from sql_base import *
import sys
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def main():
	ville = sys.argv[1]
	metier = sys.argv[2]
	page = get_html("https://www.doctolib.fr/" + metier + "/" + ville)
	swipe_page(page, 1, ville, metier)

def	swipe_page(page, numero, ville, metier):
	ret = None
	if page == None:
		return	
	page = page.find_all('a')
	for link in page:
		lien = link.get("href")
		if lien is not None and lien.count("?page="):
			numero = numero + 1
			page = get_html("https://www.doctolib.fr/" + metier + "/" + ville + "?page=" + str(numero))
			swipe_page(page, numero, ville, metier)
			break
		if lien is not None and lien.count(metier) and lien.count("https://") == 0:
			if ret != lien:
				page = "https://www.doctolib.fr" + lien
				page = get_html(page)
				if page is not None:
					get_profile(page, ville, metier)
				ret = lien

def	get_profile(page, ville, metier):
	nom = None; url = None; numero = None; email = None; http = "yes"
	name = page.find_all('span', {'itemprop': 'name'})
	for nom in name:
		if nom is not None:
			nom = nom.text
	website = page.find_all('a', {'rel': 'nofollow'})
	for link in website:
		if link is not None:
			url = link.get("href")
	data_num = page.find_all('div', {'class': 'dl-display-flex'})
	for num in data_num:
		if num is not None:
			numero = num.text
	mail = None
	if url is not None:
		mail = get_mail_accueil(url)
		if	url.count("https"):
			http = "no"
	if mail is not None:
		email = re.search(r'[\w\.-]+@[\w\.-]+', mail)
		if email is not None:
			mail = email.group(0)
	remplire_sql(ville, metier, nom, numero, email, http)
	#if numero is not None:
	#	print("numero == " + numero)
	#if url is not None:
	#	print("url    == " + url)
	#if nom is not None:
	#	print("nom    == " + nom)
	#if mail is not None:
	#	print("mail   == " + mail)
	#print("\n")

def get_mail_accueil(url_p):
	page_contact = None
	page = get_html(url_p)
	mail = find_mail(page)
	if mail is not None:
		return mail
	if page is None:
		return None
	return get_mail_contact(url_p, page, page_contact)

def get_mail_contact(url_p, page, page_contact):	
	page = page.find_all(['a', 'li'])
	for link in page:
		url = link.get("href")
		if url is not None:
			url_lower = url.lower()
			if url_lower.count("contact") and url_lower.count("http"):
				page_contact = url
				page = get_html(url)
				mail = find_mail(page)
				if mail is not None:
					return mail
			elif url_lower.count("contact"):
				if url.startswith('/') and url_p.endswith('/'):
					page_contact = url_p[:-1] + url
				elif url[0] != '/' and url_p[-1] != '/':
					page_contact = url_p + "/" + url
				else :
					page_contact = url_p + url
				page = get_html(page_contact)
				mail = find_mail(page)
				if mail is not None:
					return mail
	return page_contact

def find_mail(page):
	if page == None:
		return None
	page = page.find_all(['p', 'li', 'br', 'a', 'span'])
	for link in page:
		if link is not None:
			text = link.text
			if text.count("@") and text.count("."):
				return text
	return None

def get_html(reg_url):
	headers = {'User-Agent': 'Mozilla/5.0 (Window NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2228.0 Safari/537.3'}
	req = Request(url=reg_url, headers=headers)
	page = None
	if req is not None :
		try :
			html = urlopen(req).read()
		except :
  			return (None)
		if html is not None :
			page = BeautifulSoup(html, 'lxml')
	return (page)

if __name__ == "__main__":
	main()
