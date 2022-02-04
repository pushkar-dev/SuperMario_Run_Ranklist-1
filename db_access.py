import psycopg2

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(database="d8ca9i3t46cqib", user="vfjnvlvukklbay", password="2d9aedb9713f7c6a3063e8b8f4a66871a963a9eaf2ccbe3e2c865c8426ce4ab7", host="ec2-35-153-35-94.compute-1.amazonaws.com", port="5432")
        except Exception as e:
            print(e)
        self.cursor = self.connection.cursor()

        
    def execute(self, query):
        self.cursor.execute(query)
        return list(self.cursor.fetchall())

    def update(self, count, handle):
        self.cursor.execute(f"Update data set Questions_Solved = {count} where Handle = {handle}")
        self.connection.commit()

    def show(self, handle):
        entries = self.execute(f"SELECT * from data where \"Handle\" = '{handle}';") 
        return entries


    def __del__(self):
        self.connection.close()

db = Database()