DB_HOST = input("Enter host: ")
DB_URL = "url"
DB_USER = input("Enter user: ")
DB_PASSWORD = input("Enter pass: ")
MYSQL_JDBC_URL = "jdbc:mysql://"+DB_HOST+":3306/"+DB_URL+"?useUnicode=yes&characterEncoding=UTF8"
DRIVER_MYSQL_CLASS = "com.mysql.jdbc.Driver"
MYSQL_BATCH_SIZE_INSERT = '1000'
