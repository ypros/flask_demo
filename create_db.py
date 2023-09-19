import mysql.connector
from mysql.connector import errorcode

#mydb = mysql.connector.connect(user='root', password='password', host='127.0.0.1',port=5000,database='test',auth_plugin='mysql_native_password')
#cnx = mysql.connector.connect(user='root', password='password', host='localhost', port=33060, database='flask')
cnx = mysql.connector.connect(user='root', password='password', host='localhost', port=33060, database='flask')

cursor = cnx.cursor()

tables = {}

tables['users'] = (
    "CREATE TABLE `users` ("
    "  `id` char(36) NOT NULL,"
    "  `first_name` varchar(50) NULL,"
    "  `last_name` varchar(50) NULL,"
    "  `age` INT NULL,"
    "  `biography` TEXT NULL,"
    "  `city` varchar(50) NULL,"
    "  `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  `password_hash` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

tables['friends'] = (
    "CREATE TABLE `friends` ("
    "  `id` char(36) NOT NULL,"
    "  `user` char(36) NOT NULL,"
    "  `friend` char(36) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `friends_user_FK` FOREIGN KEY (`user`) REFERENCES `users` (`id`),"
    "  CONSTRAINT `friends_friend_FK` FOREIGN KEY (`friend`) REFERENCES `users` (`id`)"
    ") ENGINE=InnoDB;")

tables['ind_friends1'] = (
    "  CREATE INDEX `friends_user_IDX` USING BTREE ON `friends` (`user`);")

tables['ind_friends2'] = (
    "  CREATE INDEX `friends_friend_IDX` USING BTREE ON `friends` (`friend`);")




tables['posts'] = (
    "CREATE TABLE `posts` ("
    "  `id` char(36) NOT NULL,"
    "  `author_user_id` char(36) NOT NULL,"
    "  `text` text NOT NULL,"
    "  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT posts_FK FOREIGN KEY (author_user_id) REFERENCES flask.users(id)"
    ") ENGINE=InnoDB")



def create_tables(tables):
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table/index {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()

create_tables(tables)


