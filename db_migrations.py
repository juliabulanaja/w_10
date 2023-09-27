import configparser

import pymongo
import psycopg2


config = configparser.ConfigParser()
config.read('config.ini')
config_mongodb = config['MONGO']
config_postgresql = config['POSTGRESQL']

mongo_user = config_mongodb["USERNAME"]
mongodb_pass = config_mongodb["PASSWORD"]
mongodb_name = config_mongodb["NAME"]
mongo_domain = config_mongodb["DOMAIN"]

postgresql_user = config_postgresql["USER"]
postgresql_pass = config_postgresql["PASSWORD"]
postgresql_db = config_postgresql["DATABASE"]
postgresql_host = config_postgresql["HOST"]
postgresql_port = config_postgresql["PORT"]


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect with MongoDB
        client = pymongo.MongoClient(
            f"mongodb+srv://{mongo_user}:{mongodb_pass}@{mongo_domain}/{mongodb_name}?retryWrites=true&w=majority",
            tls=True, tlsAllowInvalidCertificates=True)
        m_db = client["quotes"]
        authors_col = m_db["author"]
        quotes_col = m_db["quote"]

        # connect with PostgreSQL
        conn = psycopg2.connect(
            database=postgresql_db, user=postgresql_user, password=postgresql_pass, host=postgresql_host,
            port=postgresql_port
        )

        cursor = conn.cursor()
        authors = list(authors_col.find())
        quotes = list(quotes_col.find())

        for a in authors:
            fullname = a['fullname']
            born_date = a['born_date']
            born_location = a['born_location']
            description = a['description']

            cursor.execute("""INSERT INTO quotes_author (fullname, born_date, born_location, description)
                           VALUES (%s, %s, %s, %s);""", (fullname, born_date, born_location, description))
            conn.commit()

        for q in quotes:
            quote = q['quote']
            author_id_ = q['author']
            tags = q['tags']

            author_fullname = list(map(lambda x: x['fullname'], list(filter(lambda x: x['_id'] == author_id_, authors))))[0]

            cursor.execute("""SELECT id FROM quotes_author WHERE fullname=%s""", (author_fullname, ))
            author_id = cursor.fetchone()
            author_id = author_id[0] if author_id else None
            if not author_id:
                print("Quote can't be added without author!")
                continue

            cursor.execute("""INSERT INTO quotes_quote (quote, author_id)
                                       VALUES (%s, %s) RETURNING id""", (quote, author_id))

            conn.commit()
            quote_id = cursor.fetchone()[0]

            for tag in tags:
                # check if such tag already exists in db
                cursor.execute("""SELECT id FROM quotes_tag WHERE name=%s""", (tag,))
                t = cursor.fetchone()

                if not t:
                    cursor.execute("""INSERT INTO quotes_tag (name) 
                                      VALUES (%s) RETURNING id""", (tag,))
                    conn.commit()
                    tag_id = cursor.fetchone()[0]
                else:
                    tag_id = t[0]

                cursor.execute("""INSERT INTO quotes_quote_tags (quote_id, tag_id) 
                                VALUES (%s, %s) RETURNING id""", (quote_id, tag_id))
                conn.commit()

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error, 'error')
    except IndexError:
        print("Incorrect data can't be added")
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
