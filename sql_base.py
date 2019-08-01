import mysql.connector as mysql

def main():
	db = mysql.connect(
    	host = "localhost",
    	user = "root",
    	passwd = "v7QVWVXu"
	)
	cursor = db.cursor()
#	cursor.execute("SHOW VARIABLES LIKE 'datadir'")
	cursor.execute("CREATE DATABASE hypnotherapeute")

if __name__ == "__main__":
	main()
