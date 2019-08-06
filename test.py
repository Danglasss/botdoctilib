import re

def		main():
	li = "gfrg <supportage-themecom rezger>"
	mail = re.search(r'[\w\.-]+@[\w\.-]+', li)
	if mail is not None:
		print(mail.group(0))

if __name__ == "__main__":
	main()
