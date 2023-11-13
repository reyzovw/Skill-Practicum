class Query:
    def __init__(self, __connection, __query):
        self.__connection = __connection
        self.__query = __query

    def __enter__(self):
        try:
            cursor = self.__connection.cursor()
            if type(self.__query) is tuple:
                cursor.execute(self.__query[0], (self.__query[1]))
            else:
                cursor.execute(self.__query)
            return cursor.fetchall()
        except Exception as e:
            raise e
    
    def __exit__(self, type, value, traceback):
        self.__connection.commit()