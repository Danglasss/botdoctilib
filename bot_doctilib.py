from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def main():
	page = get_html("https://www.doctolib.fr/hypnotherapeute/paris")
	swipe_page(page)

def	swipe_page(page):
	ret = None
	page = page.find_all('a')
	for link in page:
		lien = link.get("href")
		if lien is not None and lien.count("?page="):
			page = get_html("https://www.doctolib.fr/" + lien)
			swipe_page(page)
			break
		if lien is not None and lien.count("hypnotherapeute") and lien.count("https://") == 0:
			if ret != lien:
				page = "https://www.doctolib.fr" + lien
				page = get_html(page)
				get_profile(page)
				ret = lien

def	get_profile(page):
	nom = None; url = None; numero = None
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
	print(numero)
	print(url)
	print(nom)

def get_html(reg_url):
	headers = {'User-Agent': 'Mozilla/5.0 (Window NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2228.0 Safari/537.3'}
	req = Request(url=reg_url, headers=headers)
	page = None
	if req is not None :
		html = urlopen(req).read()
		if html is not None :
			page = BeautifulSoup(html, 'lxml')
	return (page)

if __name__ == "__main__":
	main()
