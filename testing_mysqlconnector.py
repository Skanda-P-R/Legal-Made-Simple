import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1803",
    database="legal"
)

cursor = mydb.cursor()

# cursor.execute("Select * from relevant_text_id")

# result = cursor.fetchall()

# print(result)


x = "dsfvjdsreknljgs/sbfsbl/esbfjb/"

list = x.split("/")

for i in list:
    cursor.execute(f"insert into test_words values ('{i}')")

cursor.execute("Select * from test_words")

result = cursor.fetchall()

print(result)