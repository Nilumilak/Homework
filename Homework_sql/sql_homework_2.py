import psycopg2
import configparser
from pprint import  pprint

config = configparser.ConfigParser()
config.read('settings.ini')

user = config['DB']['user']
password = config['DB']['password']
db_name = config['DB']['db_name']


def db_decorator(func):
    def wrapper(*args):
        try:
            # connect to exist database
            connection = psycopg2.connect(
                user=user,
                password=password,
                database=db_name
            )

            connection.autocommit = True

            result = func(connection, *args)
            return result

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
        finally:
            if connection:
                connection.close()
                print('[INFO] PostgreSQL connection closed')
    return wrapper


@db_decorator
def create_table_clients(conn):
    with conn.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS clients(
        PRIMARY KEY (id),
        id      SERIAL,
        name    VARCHAR(50) NOT NULL,
        surname VARCHAR(50) NOT NULL,
        email   VARCHAR(50) NOT NULL CHECK(email ~ '^[A-Za-z0-9][A-Za-z0-9_.-]+@\w+\.\w+$'));
        ''')


@db_decorator
def create_table_numbers(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phones(
        PRIMARY KEY (id),
        id          SERIAL,
        client_id   INTEGER NOT NULL    REFERENCES clients(id)  ON DELETE CASCADE,
        number      VARCHAR(15)     CHECK(number ~ '^\+\d+$'));
        ''')


@db_decorator
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


@db_decorator
def add_phones(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute('''
                    INSERT INTO phones(client_id, number)
                    VALUES(%s, %s)
                    ''', (client_id, number))


@db_decorator
def update_client(conn, client_id, name=None, surname=None, email=None):
    with conn.cursor() as cur:
        cur.execute(f'''
                    UPDATE clients
                    SET {', '.join(list(filter(lambda x: x is not None, ['name=%s' if name else None,
                                                                         'surname=%s' if surname else None,
                                                                         'email=%s' if email else None])))}
                    WHERE id=%s
                    ''', tuple(filter(lambda x: x is not None, (name, surname, email, client_id))))


@db_decorator
def del_number(conn, number_id):
    with conn.cursor() as cur:
        cur.execute(f'''
                    DELETE FROM phones
                    WHERE id=%s
                    ''', (number_id,))


@db_decorator
def del_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(f'''
                    DELETE FROM clients
                    WHERE id=%s
                    ''', (client_id,))


@db_decorator
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


@db_decorator
def del_table(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)


if __name__ == '__main__':
    create_table_clients()
    create_table_numbers()

    add_client('Renat', 'Kalimulin', 'my_email@mail.ru', '+123456789')
    add_client('Ivan', 'Ivanov', 'ivan@mail.ru', '+123456789')
    add_client('Petr', 'Petrov', 'petr@mail.ru', '+123456789')

    add_phones(1, '+987654321')
    add_phones(1, '+456123789')

    update_client(1, 'Other_name', None, 'my_other_email@mail.ru')

    del_number(1)

    del_client(2)

    select_client('Petr')
    select_client(None, None, None, '+123456789')

    del_table('DROP TABLE phones')
    del_table('DROP TABLE clients')
