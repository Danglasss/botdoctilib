import mysql.connector as mysql

def remplire_sql(ville, metier, nom, numeros, email_re, http):
	email = None
	if email_re is not None:
		email = str(email_re.group(0))
	db = mysql.connect(
    	host = "localhost",
    	user = "root",
    	passwd = "danglass",
    	database = "data"
	)
	cursor = db.cursor()
	if if_exists(cursor, nom, numeros, email):
		return
	reference = (ville, metier, nom, numeros, email, http)
	cursor.execute("""INSERT INTO hypno (ville, metier, nom, numeros, email, http) VALUES(%s, %s, %s, %s, %s, %s)""", reference)
	db.commit()
	cursor.execute("""SELECT * FROM hypno""")
	for row in cursor:
		print(row)

def if_exists(cursor, nom, numeros, email):
	i = 0
	if nom is not None:
		cursor.execute("""SELECT * FROM hypno where nom = nom""")
		if len(cursor.fetchall()):
			i += 1
	if numeros is None:
		i += 1
	if numeros is not None:
		cursor.execute("""SELECT * FROM hypno where numeros = %s""", numeros)	
		if len(cursor.fetchall()):
			i += 1
	if email is not None:		
		cursor.execute("""SELECT * FROM hypno where email = %s""", email)	
		if len(cursor.fetchall()):
			return 1
	if i == 2:
		return 1
	return 0
	