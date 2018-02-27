import sqlite3
from time import time

def replace_spaces(str):
	return str.replace(" ", "_")

def add_row(db_name, country_name, time, tweet_id, positive_magnitude, negative_magnitude):
	db = sqlite3.connect(db_name)
	cursor = db.cursor()
	cursor.execute('''INSERT INTO %s VALUES (%s, %s, %s, %s)''' % (country_name, time, tweet_id, positive_magnitude, negative_magnitude))
	db.commit()
	db.close()

def create_table(db_name, country_name):
	db = sqlite3.connect(db_name)
	cursor = db.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS %s(time TEXT PRIMARY KEY, tweet_id TEXT, positive_magnitude REAL, negative_magnitude REAL)''' % (country_name))
	db.commit()
	db.close()

#
def add_to_db(db_name, country_name, time, tweet_id, positive_magnitude, negative_magnitude):
	db_name, country_name, time, tweet_id, positive_magnitude, negative_magnitude = replace_spaces(db_name), replace_spaces(country_name), replace_spaces(time), replace_spaces(tweet_id), replace_spaces(positive_magnitude), replace_spaces(negative_magnitude)

	create_table(db_name, country_name)
	add_row(db_name, country_name, time, tweet_id, positive_magnitude, negative_magnitude)

if __name__ == '__main__':
	current_time = str(time())

	add_to_db("tut_databse", "Canada", current_time, "4132421", "3.2", "1214.21412")
	#add_to_db(replace_spaces("tut_databse"), replace_spaces("Canada"), replace_spaces(str(current_time)), replace_spaces("141342134"), replace_spaces("3.1"), replace_spaces("125.0031"))
	#add_to_db(replace_spaces("tut_databse"), replace_spaces("United States"), replace_spaces(str(current_time)), replace_spaces("4561185736"), replace_spaces("0.00001"), replace_spaces("125.0031"))