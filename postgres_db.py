import psycopg2
from decouple import config

connect_db = {
    'dbname': config('DB_NAME'),
    'user': config('DB_USER'),
    'host': config('DB_HOST'),
    'password': config('DB_PASSWORD'),
    'port': config('DB_PORT')
}

def connect():

    try:
        conn = psycopg2.connect(**connect_db)
        cursor = conn.cursor()

        create_table = (
            """
            CREATE TABLE IF NOT EXISTS student_management (
                id SERIAL PRIMARY KEY,
                roll_num NUMERIC(100),
                name VARCHAR(100),
                class_var VARCHAR(100),
                section VARCHAR(50)
                contact VARCHAR(100),
                fathersnm VARCHAR(100),
                address VARCHAR(100),
                gender VARCHAR(100),
                dob VARCHAR(100),
                date_attended DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            
            );

            CREATE TABLE IF NOT EXIST user_authentication (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100),
                password VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            
            );
            """
        
        )

        cursor.execute(create_table)
        conn.commit()
        print('Table has been created successfully')
        return conn
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(e)
        return None

