import MySQLdb
import re

MySQL_Identifier_regex = re.compile("^[0-9a-zA-Z$_]+$")


class MySQL_InvalidColumnNameError(Exception): pass
class MySQL_InvalidTableNameError(Exception): pass
class MySQL_InvalidDatabaseNameError(Exception): pass
class MySQL_TableError(Exception): pass
class MySQL_LimitTypeError(Exception): pass
class MySQL_ConditionTypeError(Exception): pass
class MySQL_ConditionFormatError(Exception): pass
class MySQL_InavlidSizeError(Exception): pass

class MySQL_Object: pass
class MySQL_Integer(MySQL_Object):
    def render(self): return "INT"
class MySQL_BigInteger(MySQL_Object):
    def render(self): return "BIGINT"
class MySQL_Float(MySQL_Object):
    def render(self): return "FLOAT"
class MySQL_Double(MySQL_Object):
    def render(self): return "DOUBLE"
class MySQL_Boolean(MySQL_Object):
    def render(self): return "BOOLEAN"
class MySQL_Char(MySQL_Object):
    def __init__(self, n):
        if n<0 or n>255: raise MySQL_InvalidSizeError("MySQL Invalid size for CHAR: " + n)
        else: self.n = n
    def render(self): return "CHAR(" + str(self.n) + ")"
class MySQL_Varchar(MySQL_Object):
    def __init__(self, n):
        if n<0 or n>65535: raise MySQL_InvalidSizeError("MySQL Invalid size for VARCHAR: " + n)
        else: self.n = n
    def render(self): return "VARCHAR(" + str(self.n) + ")"
class MySQL_VarcharBinary(MySQL_Object):
    def __init__(self, n):
        if n<0 or n>65535: raise MySQL_InvalidSizeError("MySQL Invalid size for VARCHAR: " + n)
        else: self.n = n
    def render(self): return "VARCHAR(" + str(self.n) + ") BINARY" 
class MySQL_Text(MySQL_Object):
    def render(self): return "TEXT"
class MySQL_Blob(MySQL_Object):
    def __init__(self, n=65535):
        self.t = ''
        if n>0 and n<=255:  self.t = 'TINYBLOB'
        elif n<=65535: self.t = 'BLOB'
        elif n<=16777216: self.t = 'MEDIUMBLOB'
        elif n<=4294967296: self.t = 'LONGBLOB'
        else: raise MySQL_InvalidSizeError("MySQL Invalid size for TINYBLOB: " + n)
    def render(self): return self.t


class MySQL_Condition:

    def __init__(self, columnName, relationalOperator, value):
        global MySQL_Identifier__regex
        relationalOperator = relationalOperator.lower()
        if relationalOperator not in ['=', '!=', '>=', '<=', '<', '>', 'like']:
            raise  MySQL_ConditionFormatError("invalid relational operator '" + relationalOperator + "'")
        if MySQL_Identifier_regex.match(columnName):
            self.columnName, self.relationalOperator, self.value = columnName, relationalOperator, value
        else:
            raise MySQL_InvalidColumnNameError("invalid column name ")

    def render(self):
        return self.columnName + " " + self.relationalOperator + " %s", [self.value]


class MySQL_Conditions:

    def __init__(self, condtion1, logical_operator, condition2):
        if logical_operator.lower() not in ['and', 'or']:
            raise MySQL_ConditionFormatError("MySQL Condition Format Error, invalid logical operator: " + logical_operator)
        self.condition1, self.logical_operator, self.condition2 = condtion1.render(), logical_operator, condition2.render()

    def render(self):
        values = []
        for value in self.condition1[1]: values.append(value)
        for value in self.condition2[1]: values.append(value)
        return self.condition1[0] + " " + self.logical_operator + " " + self.condition2[0], values


class MySQL_Columns:
    def __init__(self):
        global MySQL_Identifier_regex
        self.regex, self.columns = MySQL_Identifier_regex, []

    def add(self, *args):
        for arg in args:
            if self.regex.match(arg):
                self.columns.append(arg)
            else:
                self.columns = []
                return False
        return True

    def render(self):
        if len(self.columns) == 0:
            return "*"
        else:
            return ",".join(self.columns)

    def clear(self):
        self.columns = []



class MySQL_Column:

    def __init__(self, name, type_s, primary_key=False, nullable=False, unique=False):
        if MySQL_Identifier_regex.match(name):
            self.name, self.t, self.is_pk, self.nullable, self.unique = name, type_s.render(), primary_key, nullable, unique
        else:
            raise MySQL_InvalidColumnNameError("MySQL Invalid Column Name Error: " + name)


class MySQL_Table:

    def __init__(self, sql, tableName, dbName):
        self.name, self.sql, self.dbName, self.condition, self.order, self.where_str = tableName, sql, dbName, '', '', ''
        self.columns, self.values, self.values1 = MySQL_Columns(), [], []

    def exists(self):
        cur_dbName = self.sql.current_dbName
        exists = self.sql.set_database(self.dbName).table_exists(self.name)
        self.sql.set_database(cur_dbName)
        return exists

    def insert(self, values):
        cols = self.get_columns()
        keys, vals = [], []
        for k in values:
            v = values[k]
            if k not in cols:
                raise MySQL_InvalidColumnNameError("MySQL Invalid Column Name Error: " + k)
            keys.append(k)
            vals.append(v)
        query = "INSERT INTO " + self.name + "(" + ",".join(keys) + ") VALUES(" + ",".join(["%s"]*len(keys)) + ")"
        self.sql.execute_query (
            query, vals
            )

    def get_columns(self):
        data = self.sql.execute_query (
                """SELECT column_name
                   FROM information_schema.columns
                   WHERE table_schema = %s AND table_name = %s
                """, (self.dbName, self.name)
            )
        return [x[0] for x in data]

    def set(self, *alist):
        o, o1 = [], []
        for a in alist:
            if MySQL_Identifier_regex.match(a[0]): o.append(a[0] + "=%s"); o1.append(a[1])
            else:  raise MySQL_InvalidColumnNameError("MySQL Invalid Column name: " + a[0])
        cur_dbName = self.sql.current_dbName
        self.sql.set_database(self.dbName).execute_query (
                "UPDATE " + self.name + " SET " + ",".join(o) + self.where_str, o1 + self.values1
            )
        self.sql.set_database(cur_dbName)

    def where(self, condition):
        if isinstance(condition, (MySQL_Condition, MySQL_Conditions)):
            self.where_str, self.values1 = condition.render()
            self.where_str = " WHERE " + self.where_str
        else:
            raise MySQL_ConditionTypeError("MySQL Condition Type Error, expection MySQL_Conditions got " + str(type(condition)))
        return self


    def describe(self):
        cur_dbName = self.sql.current_dbName
        data = self.sql.set_database(self.dbName).execute_query (
                "DESCRIBE " + self.name + ";"
            )
        self.sql.set_database(cur_dbName)
        return data

    def get(self, *columns):
        if len(columns) == 1 and isinstance(columns[0], MySQL_Columns):
            self.columns = columns
        else:
            if not self.columns.add(*columns):
                raise MySQL_InvalidColumnNameError("Invalid MySQL Column Name")
        cur_dbName = self.sql.current_dbName
        query = "SELECT " + self.columns.render() + " FROM " + self.name + self.condition + self.order + ";" 
        data = self.sql.set_database(self.dbName).execute_query( query , self.values)
        self.sql.set_database(cur_dbName)
        return data


    def limit(self, n):
        if isinstance(n, int) and n>=0:
            self.limit = n
        else:
            raise MySQL_LimitTypeError("MySQL Limit Type Error, expected positive integer got " + str(type(n)))
        return self

    def filter_by(self, condition):
        self.columns.clear()
        if isinstance(condition, (MySQL_Conditions, MySQL_Condition)):
            self.condition, self.values = condition.render()
            self.condition = " WHERE " + self.condition
        else:
            raise MySQL_ConditionTypeError("MySQL Condition Type Error, expection MySQL_Conditions got " + str(type(condition)))
        return self

    def order_by(self, columns, order_type):
        order_type = order_type.lower()
        if order_type == 'asc' or order_type == 'desc' and len(columns) > 0:
            cols = MySQL_Columns()
            if cols.add(*columns):
                self.order = " ORDER BY " + cols.render() + " " + order_type
            else:
                raise MySQL_InvalidColumnNameError("Invalid Column name was given in order_by")
        return self




class MySQL:

    def __init__(self, user, passwd, dbName=None, host='localhost'):
        if dbName is None:
            self.current_dbName = None
            self.connection = MySQLdb.connect(
                host = host, user = user, passwd = passwd
            )
        else:
            self.current_dbName = dbName
            self.connection = MySQLdb.connect(
                host = host, db = dbName,
                user = user, passwd = passwd,
            )
        self.cursor = self.connection.cursor()


    def execute_query(self, code, values=[]):
        try:
            if len(values) == 0:
                self.cursor.execute(code);
            else:
                self.cursor.execute(code, values);
        except MySQLdb.Error as e:
            self.connection.rollback()
            raise e
        return self.cursor.fetchall()


    def get_databases(self):
        data = self.execute_query (
                """SELECT schema_name
                   FROM information_schema.schemata;"""
            )
        return [x[0] for x in data]

    def get_tables(self):
        if self.current_dbName is None:
            raise MySQL_TableError("MySQL Database not specified before accessing tables")
        else:
            data = self.execute_query (
                    """SELECT table_name
                       FROM information_schema.tables
                       WHERE table_schema = %s""", (self.current_dbName,))
            return [x[0] for x in data]


    def database_exists(self, dbName):
        exists = self.execute_query (
                """SELECT EXISTS (
                    SELECT 1 FROM information_schema.schemata
                    WHERE schema_name = %s
                );""", (dbName,)
            )
        return exists[0][0] == 1


    def set_database(self, dbName):
        global MySQL_Identifier_regex

        if MySQL_Identifier_regex.match(dbName):
            if self.current_dbName != dbName:
                self.execute_query (
                    "use " + dbName + ";"
                )
                self.current_dbName = dbName
        else:
            raise MySQL_InvalidDatabaseNameError("Invalid Database Name Error: " + dbName)
        return self


    def table_exists(self, tableName):
        exists = self.execute_query (
                """SELECT EXISTS(
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = %s  AND  table_name = %s
                );""", (self.current_dbName, tableName)
            )
        return exists[0][0] == 1

    def table(self, tableName):
        if self.current_dbName is None:
            raise MySQL_TableError("MySQL Database not specified before accessing table")
        elif MySQL_Identifier_regex.match(tableName):
            return MySQL_Table(self, tableName, self.current_dbName)
        else:
            raise MySQL_InvalidTableNameError("MySQL Invalid Table Name: " + tableName)

    def create_table(self, table_name, *args):
        primary_keys, o, unique_keys = [], [], []
        for arg in args:
            if arg.is_pk: primary_keys.append(arg.name)
            if arg.unique: unique_keys.append(arg.name)
            if arg.nullable:
                o.append(arg.name + " " + arg.t + " NULL")
            else:
                o.append(arg.name + " " + arg.t + " NOT NULL")
        if len(primary_keys) > 0:
            o.append("PRIMARY KEY (" + ",".join(primary_keys) + ")")
        if len(unique_keys) > 0:
            o.append("UNIQUE (" + ",".join(unique_keys) + ")")
        query = "CREATE TABLE " + table_name + "(" + ",".join(o) + ");"
        self.execute_query (
                query
            )
    
    def delete_table(self, table_name):
        self.execute_query ("drop table " + table_name )

    def commit(self):
        self.connection.commit()


    def close(self):
        self.cursor.close()
        self.connection.close()

