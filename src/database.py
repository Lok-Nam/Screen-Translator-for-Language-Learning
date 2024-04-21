import sqlite3


class Database:
    def __init__(self, db_name="src\\database\\database.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.ini_database()

    # open and close connections
    def openConnection(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def closeConnection(self):
        self.cursor.close()
        self.conn.close()

    def ini_database(self):
        self.openConnection()
        sql_create_vocabulary_table = """ CREATE TABLE IF NOT EXISTS vocabulary (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            word text NOT NULL,
                                            part_of_speech text,
                                            meaning text,
                                            frequency integer DEFAULT 1,
                                            date_added date DEFAULT CURRENT_DATE
                                        ); """
        self.cursor.execute(sql_create_vocabulary_table)
        self.conn.commit()
        sql_create_flashcard_table = """ CREATE TABLE IF NOT EXISTS flashcard (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            next_review DATE,
                                            state text,
                                            card BLOB,
                                            vocabularyId INTEGER,
                                            FOREIGN KEY (vocabularyId) REFERENCES vocabulary(id)
                                        );"""
        self.cursor.execute(sql_create_flashcard_table)
        self.conn.commit()
        self.closeConnection()

    def create_table(self, table_name, columns):
        try:
            self.cursor.execute(f"CREATE TABLE {table_name} ({', '.join(columns)});")
            self.conn.commit()
            print(f"Table {table_name} created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, table_name, columns, data):
        # construct placeholders and column names strings
        placeholders = ', '.join('?' for _ in data)
        columns_str = ', '.join(columns)
        
        # prepare the query
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"
        print("Executing query:", sql)
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")


    def fetch_data(self, table_name, columns, condition=None):
        try:
            if condition:
                query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {condition};"
            else:
                query = f"SELECT {', '.join(columns)} FROM {table_name};"

            # print the query to the console before execution
            print("Executing query:", query)

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")

    def fetch_data_custom_query(self, query):
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Error fetching data with custom query: {e}")
            return []

    def update_data(self, table_name, data, condition):
        try:
            self.cursor.execute(f"UPDATE {table_name} SET {', '.join([f'{key} = ?' for key in data.keys()])} WHERE {condition};", list(data.values()))
            self.conn.commit()
            print(f"Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    def delete_data(self, table_name, condition):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition};")
            self.conn.commit()
            print(f"Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    def drop_table(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE {table_name};")
            self.conn.commit()
            print(f"Table {table_name} dropped successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")

    def get_id(self):
        return self.cursor.lastrowid