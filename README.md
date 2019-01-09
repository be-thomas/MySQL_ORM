# MySQL_ORM



##Installation
1st instal MySQLdb

###Windows
[check this out](https://gist.github.com/johnmiroki/e655d7e93a00864b65f10528731bbf40)

###Linux & Mac
[check this out](https://stackoverflow.com/questions/25865270/how-to-install-python-mysqldb-module")

Finally, this step is common for all operating systems -
download MySQL_ORM.py from this repository and put it in same folder as your project. you case start using after importing it(<mark>import MySQL_ORM</mark>).




##Usage


###Initialize
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")   #use your password instead of pwd
'''


###Initialize and Set Database
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd", dbName="db")    #use your password instead of pwd
'''


###Initialize MySQL from different host(Default is 'localhost')
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd", dbName="db", host='123.45.67.89', port=80)    #use your password instead of pwd
'''



###Get List of all databases
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
print(mysql.get_databases())
'''


###Check if Database exists
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
print(mysql.database_exists("db"))
'''


###Set Database and print all tables in it
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
print(mysql.get_tables())
'''


###Create Table
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")

mysql.set_database("db")
mysql.create_table("tableName",
	MySQL_Column('id', MySQL_Integer(), primary_key=True),
	MySQL_Column('name', MySQL_Varchar(100)),
	MySQL_Column('marks', MySQL_Double()),
	MySQL_Column('id1', MySQL_Integer(), unique=True)
	MySQL_Column('attendance', MySQL_Integer(), nullable=True)
)'''


###Check if table exists in Database
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
print(mysql.table_exists("table"))
'''


###Insert into table
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
table = mysql.table("table")
table.insert({
	'id': 1,
	'name': 'John'
})
'''


###print all rows in table
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
for row in mysql.table("table").get():
    print(row)
'''


###print all rows in table in descending order by name
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
for row in mysql.table("table").order_by(["name"], "desc").get():
    print(row)


###print all rows in table whose name starts with A
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
for row in mysql.table("table").filter_by(MySQL_Condition('name', 'like', 'A_%').get():
    print(row)
'''


###print all rows in table whose id is in range 1-10 in descending order limiting output to 3 rows
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
ids = mysql.table("table").filter_by(MySQL_Conditions(MySQL_Condition('id', '>=', 1), 'and', MySQL_Condition('id', '<=', 10))
for id in ids.order_by(['id'], 'desc').limit(3).get():
    print(id)
'''


###Set column values in Table
'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
table = mysql.table("table")
table.set({
	"name": 1
})
'''


###Direct Query Execution(Not recommended)
Since this is a very thin and light wrapper there will negligible improvements in excuting query directly.
This wrapper was made with 3 things in mind -
1) Security
2) Performance
3) Simple to use

You need to keep in mind about the security vulnerabilities while executing query directly

'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
mysql.execute_query("SELECT * FROM table;")
'''

To escape values you can use '%s' placeholder in query string and pass a 2nd argument(tuple with a values) -

'''from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
id = 1
mysql.execute_query("INSERT INTO table(id) VALUES(%s);", (id,))
'''
