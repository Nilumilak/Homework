import psycopg2
import configparser
from pprint import pprint

config = configparser.ConfigParser()
config.read('settings.ini')

user = config['DB']['user']
password = config['DB']['password']
db_name = config['DB']['db_name']


def create_table_clients(conn):
    with conn.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS clients(
        PRIMARY KEY (id),
        id      SERIAL,
        name    VARCHAR(50) NOT NULL,
        surname VARCHAR(50) NOT NULL,
        email   VARCHAR(50) NOT NULL CHECK(email ~ '^[A-Za-z0-9][A-Za-z0-9_.-]+@\w+\.\w+$'));
        ''')
        conn.commit()


def create_table_numbers(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phones(
        PRIMARY KEY (id),
        id          SERIAL,
        client_id   INTEGER NOT NULL    REFERENCES clients(id)  ON DELETE CASCADE,
        number      VARCHAR(15)     CHECK(number ~ '^\+\d+$'));
        ''')
        conn.commit()


def add_client(conn, name, surname, email, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO clients(name, surname, email)
        VALUES(%s, %s, %s)
        RETURNING id;
        ''', (name, surname, email))
        if phones:
            client_id = cur.fetchone()[0]
            cur.execute('''
                    INSERT INTO phones(client_id, number)
                    VALUES(%s, %s)
                            ''', (client_id, phones))


def add_phones(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute('''
                    INSERT INTO phones(client_id, number)
                    VALUES(%s, %s)
                    ''', (client_id, number))
        conn.commit()


def update_client(conn, client_id, name=None, surname=None, email=None):
    with conn.cursor() as cur:
        cur.execute(f'''
                    UPDATE clients
                    SET {', '.join(list(filter(lambda x: x is not None, ['name=%s' if name else None,
                                                                         'surname=%s' if surname else None,
                                                                         'email=%s' if email else None])))}
                    WHERE id=%s
                    ''', tuple(filter(lambda x: x is not None, (name, surname, email, client_id))))
        conn.commit()


def del_number(conn, number_id):
    with conn.cursor() as cur:
        cur.execute(f'''
                    DELETE FROM phones
                    WHERE id=%s
                    ''', (number_id,))
        conn.commit()


def del_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(f'''
                    DELETE FROM clients
                    WHERE id=%s
                    ''', (client_id,))
        conn.commit()


def select_client(conn, name=None, surname=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute(f'''
                    SELECT clients.id, name, surname, email, number
                    FROM clients
                    JOIN phones
                    ON phones.client_id=clients.id
                    WHERE {', '.join(list(filter(lambda x: x is not None, ['name=%s' if name else None,
                                                                           'surname=%s' if surname else None,
                                                                           'email=%s' if email else None,
                                                                           'number=%s' if phones else None])))}
                    ''', tuple(filter(lambda x: x is not None, (name, surname, email, phones))))
        pprint(cur.fetchall())


def del_table(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()


if __name__ == '__main__':
    with psycopg2.connect(database=db_name, user=user, password=password) as conn:
        create_table_clients(conn)
        create_table_numbers(conn)

        add_client(conn, 'Renat', 'Kalimulin', 'my_email@mail.ru', '+123456789')
        add_client(conn, 'Ivan', 'Ivanov', 'ivan@mail.ru', '+123456789')
        add_client(conn, 'Petr', 'Petrov', 'petr@mail.ru', '+123456789')

        add_phones(conn, 1, '+987654321')
        add_phones(conn, 1, '+456123789')

        update_client(conn, 1, 'Other_name', email='my_other_email@mail.ru')

        del_number(conn, 1)

        del_client(conn, 2)

        select_client(conn, name='Petr')
        select_client(conn, phones='+123456789')

        del_table(conn, 'DROP TABLE phones')
        del_table(conn, 'DROP TABLE clients')
