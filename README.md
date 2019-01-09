# MySQL_ORM
&nbsp;

## Installation
1st instal MySQLdb
##### Windows [check this out](https://gist.github.com/johnmiroki/e655d7e93a00864b65f10528731bbf40)

##### Linux & Mac [check this out](https://stackoverflow.com/questions/25865270/how-to-install-python-mysqldb-module")

Finally, this step is common for all operating systems -
download MySQL_ORM.py from this repository and put it in same folder as your project. you case start using after importing it(<mark>import MySQL_ORM</mark>).

&nbsp;
&nbsp;
&nbsp;

# Initialize
&nbsp;
#### Initialize
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")   #use your password instead of pwd
```
&nbsp;

#### Initialize And Set Database
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd", dbName="db")    #use your password instead of pwd
```

&nbsp;

#### Initialize MySQL From Different Host(Default is 'localhost')
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd", dbName="db", host='123.45.67.89', port=80)    #use your password instead of pwd
```

&nbsp;
&nbsp;
&nbsp;

# Databases

#### Get List Of All Databases
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
print(mysql.get_databases())
```

&nbsp;

#### Check If Database Exists
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
print(mysql.database_exists("db"))
```

&nbsp;
&nbsp;
&nbsp;

# Tables

#### Set Database And Print All Tables In It
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
print(mysql.get_tables())
```

&nbsp;

#### Create Table
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")

mysql.set_database("db")
mysql.create_table("tableName",
	MySQL_Column('id', MySQL_Integer(), primary_key=True),
	MySQL_Column('name', MySQL_Varchar(100)),
	MySQL_Column('marks', MySQL_Double()),
	MySQL_Column('id1', MySQL_Integer(), unique=True)
	MySQL_Column('attendance', MySQL_Integer(), nullable=True)
)
```

&nbsp;

#### Check If Table Exists In Database
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
print(mysql.table_exists("table"))
```


#### Insert Into Table
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
table = mysql.table("table")
table.insert({
	'id': 1,
	'name': 'John'
})
```

&nbsp;

#### Print All Rows In Table
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
for row in mysql.table("table").get():
    print(row)
```

&nbsp;

#### Print All Rows In Table In Descending Order By Name
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
for row in mysql.table("table").order_by(["name"], "desc").get():
    print(row)
```

&nbsp;

#### Print All Rows In Table Whose Name Starts With 'A'
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
for row in mysql.table("table").filter_by(MySQL_Condition('name', 'like', 'A_%').get():
    print(row)
```

&nbsp;

#### Print All Rows In Table Whose Id Is In Range 1-10 In Descending Order Limiting Output To 3 Rows
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
ids = mysql.table("table").filter_by(MySQL_Conditions(MySQL_Condition('id', '>=', 1), 'and', MySQL_Condition('id', '<=', 10))
for id in ids.order_by(['id'], 'desc').limit(3).get():
    print(id)
```

&nbsp;

#### Set Column Values In Table
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
table = mysql.table("table")
table.set({
	"name": 1
})
```

&nbsp;

#### Set Column Values In Table Where Name is 'Thomas'
```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
table = mysql.table("table")
table.where(MySQL_Condition("name", "=", "Thomas")).set({"id" : 1})
```

&nbsp;
&nbsp;
&nbsp;

# Directly Excute Query

#### Direct Query Execution(Not recommended)
Since this is a very thin and light wrapper there will negligible improvements in excuting query directly.
This wrapper was made with 3 things in mind -
1) Security
2) Performance
3) Simple to use

You need to keep in mind about the security vulnerabilities while executing query directly

```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
mysql.execute_query("SELECT * FROM table;")
```

To escape values you can use '%s' placeholder in query string and pass a 2nd argument(tuple with a values) -

```
from MySQL_ORM import *

mysql = MySQL("root", "pwd")
mysql.set_database("db")
id = 1
mysql.execute_query("INSERT INTO table(id) VALUES(%s);", (id,))
```
