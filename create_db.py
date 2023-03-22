import mysql.connector
#mydb = mysql.connector.connect(user='root', password='password', host='127.0.0.1',port=5000,database='test',auth_plugin='mysql_native_password')
mydb = mysql.connector.connect(user='root', password='password', host='localhost', port=33060, database='flask')



my_cursor = mydb.cursor()
try:
    my_cursor.execute("""

    DROP TABLE IF EXISTS flask.users;

    CREATE TABLE flask.users (
    id CHAR(36) NOT NULL,
    first_name varchar(50) NULL,
    last_name varchar(50) NULL,
    age INT NULL,
    biography TEXT NULL,
    city varchar(50) NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    password_hash varchar(255) NOT NULL,
    CONSTRAINT users_PK PRIMARY KEY (id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_0900_ai_ci;
    """, multi=True)
    mydb.commit()
except mysql.connector.Error as err:
    print(err.msg)
else:
    print("users table created")

my_cursor = mydb.cursor()
try:
    my_cursor.execute("""
    DROP TABLE IF EXISTS flask.friends;
    
    CREATE TABLE flask.friends (
        id CHAR(36) NOT NULL,
        user CHAR(36) NOT NULL,
        friend CHAR(36) NOT NULL,
        CONSTRAINT friends_PK PRIMARY KEY (id),
        CONSTRAINT friends_FK FOREIGN KEY (user) REFERENCES flask.users(id),
        CONSTRAINT friends_FK_1 FOREIGN KEY (friend) REFERENCES flask.users(id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_0900_ai_ci;
    
    CREATE INDEX friends_user_IDX USING BTREE ON flask.friends (user);
    CREATE INDEX friends_friend_IDX USING BTREE ON flask.friends (friend);
    """, multi=True)
    mydb.commit()
except mysql.connector.Error as err:
    print(err.msg)
else:
    print("friends table created")

my_cursor = mydb.cursor()
try:
    my_cursor.execute("""
    DROP TABLE IF EXISTS flask.posts;

    CREATE TABLE flask.posts (
        id char(36) NOT NULL,
        author_user_id char(36) NULL,
        `text` TEXT NULL,
        created_at DATETIME NOT NULL,
        CONSTRAINT posts_PK PRIMARY KEY (id),
        CONSTRAINT posts_FK FOREIGN KEY (author_user_id) REFERENCES flask.users(id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_0900_ai_ci;
    """, multi=True)
    mydb.commit()
except mysql.connector.Error as err:
    print(err.msg)
else:
    print("posts table created")

my_cursor.close()
mydb.close()