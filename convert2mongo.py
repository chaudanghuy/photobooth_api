import sqlite3
import mysql.connector

# ==== CONFIG ====
SQLITE_DB_PATH = "db.sqlite3"  # path to SQLite file
MYSQL_CONFIG = {
    'host': 'mysql-photobooth.alwaysdata.net',         # MySQL host (use your MySQL server / free host)
    'user': '425879',              # MySQL username
    'password': 'wSYBv_RQ5Tjw@#3', # MySQL password
    'database': 'photobooth_test'      # MySQL database name (must exist first)
}

# ==== CONNECT ====
sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
sqlite_cursor = sqlite_conn.cursor()

mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
mysql_cursor = mysql_conn.cursor()

# ==== GET TABLES FROM SQLITE ====
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table_name_tuple in tables:
    table_name = table_name_tuple[0]
    print(f"Processing table: {table_name}")

    # Get CREATE TABLE SQL from SQLite
    sqlite_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    create_table_sql = sqlite_cursor.fetchone()[0]

    # Adjust SQLite CREATE TABLE syntax to MySQL
    create_table_sql_mysql = (
        create_table_sql
        .replace("AUTOINCREMENT", "AUTO_INCREMENT")
        .replace("INTEGER PRIMARY KEY", "INT PRIMARY KEY")
        .replace("TEXT", "VARCHAR(255)")
        .replace("REAL", "DOUBLE")
    )

    try:
        mysql_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
        mysql_cursor.execute(create_table_sql_mysql)
    except mysql.connector.Error as e:
        print(f"Error creating table {table_name}: {e}")
        continue

    # Copy data
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    col_names = [description[0] for description in sqlite_cursor.description]

    if rows:
        placeholders = ", ".join(["%s"] * len(col_names))
        insert_sql = f"INSERT INTO `{table_name}` ({', '.join(col_names)}) VALUES ({placeholders})"
        mysql_cursor.executemany(insert_sql, rows)
        mysql_conn.commit()

    print(f"Inserted {len(rows)} rows into {table_name}")

# ==== CLOSE CONNECTIONS ====
sqlite_conn.close()
mysql_cursor.close()
mysql_conn.close()

print("Migration completed successfully!")
