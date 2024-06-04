import mysql.connector
import pytest
import time
import logging
import random
import string


LOGGER = logging.getLogger(__name__)

PATTERN = 'test%'

@pytest.fixture(scope='module')
def db_connection()->mysql.connector.MySQLConnection:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='example',
        database='testdb'
    )
    assert connection.is_connected(), "Не удалось подключиться к базе данных"
    return connection


def test_db_conn(db_connection:mysql.connector.MySQLConnection)->None:
    cursor = db_connection.cursor()
    query = 'SELECT * from test_table'
    cursor.execute(query)
    rows = cursor.fetchall()
    LOGGER.info(f'Database values: {rows}')
    assert rows!=[]
    assert rows is not None
    cursor.close()

def test_str_like(db_connection:mysql.connector.MySQLConnection)->None:
    cursor = db_connection.cursor()

    query = f"SELECT * FROM test_table WHERE str LIKE '{PATTERN}'"
    cursor.execute(query)
    results_without_index = cursor.fetchall()
    LOGGER.info(f'No_index data: {results_without_index}')

    query = "CREATE INDEX str_index ON test_table (str)"
    cursor.execute(query)
    db_connection.commit()

    query = f"SELECT * FROM test_table WHERE str LIKE '{PATTERN}'"
    cursor.execute(query)
    results_with_index = cursor.fetchall()
    LOGGER.info(f'With_index data: {results_with_index}')

    query = "DROP INDEX str_index ON test_table"
    cursor.execute(query)

    db_connection.commit()
    cursor.close()

    assert results_without_index == results_with_index


def test_perfomance_like(db_connection:mysql.connector.MySQLConnection)->None:
    def random_strings()->list:
        pattern_to_random = ['test','bruhmmm','Sasha','Masha','']
        length = 20 
        count = 100
        generated_strings = []
        for _ in range(count):
            substring = random.choice(pattern_to_random)
            random_string = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            index = random.randint(0, length - len(substring))
            generated_string = random_string[:index] + substring + random_string[index + len(substring):]

            generated_strings.append(generated_string)

        return generated_strings

    def insert_to_db(db_connection: mysql.connector.MySQLConnection, generated_strings:list)->None:
        cursor = db_connection.cursor()
        cursor.executemany(
            "INSERT INTO test_table (str) VALUES (%s)",
            [(insert_string,) for insert_string in generated_strings])
        db_connection.commit()

    def clear_db(db_connection: mysql.connector.MySQLConnection)->None:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM test_table WHERE id > 5")
        db_connection.commit()

    ## End of functions
    strings_to_send = random_strings()
    insert_to_db(db_connection,strings_to_send)


    cursor = db_connection.cursor()
    query = f"SELECT * FROM test_table WHERE str LIKE '{PATTERN}'"
    start_time = time.time()
    cursor.execute(query)
    res1 = set(cursor.fetchall())
    end_time = time.time()
    time_without_index = end_time - start_time
    LOGGER.info(f'TTE without index: {time_without_index}') # TTE = time to execute, kak TTK - time to kill v pubg:)

    query = "CREATE INDEX str_index ON test_table (str)"
    cursor.execute(query)
    db_connection.commit()
    cursor.close()

    cursor = db_connection.cursor()
    query = f"SELECT * FROM test_table WHERE str LIKE '{PATTERN}'"
    start_time = time.time()
    cursor.execute(query)
    res2 = set(cursor.fetchall())
    end_time = time.time()
    time_with_index = end_time - start_time
    LOGGER.info(f'TTE with index: {time_with_index}')
    
    query = "DROP INDEX str_index ON test_table"
    cursor.execute(query)

    clear_db(db_connection)
    cursor.close

    assert time_with_index < time_without_index
    assert res1==res2


def test_when_index_is_not_used(db_connection:mysql.connector.MySQLConnection)->None:
    cursor = db_connection.cursor()

    #First table
    query = "CREATE INDEX str_index ON break_index1 (str)"
    cursor.execute(query)
    db_connection.commit()
    
    query = "EXPLAIN SELECT * FROM break_index1 WHERE LOWER(str) LIKE 'a'"
    res = cursor.execute(query)
    res = cursor.fetchone()
    LOGGER.info(f'First example first table: {res}')

    query = "EXPLAIN SELECT * FROM break_index1 WHERE str LIKE 'a%'"
    res = cursor.execute(query)
    res = cursor.fetchone()
    LOGGER.info(f'Second example first table: {res}')

    query = "EXPLAIN SELECT * FROM break_index1 WHERE str LIKE NULL"
    res = cursor.execute(query)
    res = cursor.fetchone()
    LOGGER.info(f'Third example first table: {res}')

    query = "EXPLAIN SELECT * FROM break_index1 WHERE str LIKE '%a%';"
    res = cursor.execute(query)
    res = cursor.fetchone()
    LOGGER.info(f'Fourth example first table: {res}')

    query = "DROP INDEX str_index ON break_index1"
    cursor.execute(query)
    db_connection.commit()


    #Second table
    query = "CREATE INDEX str_index ON break_index2 (strtext(10))"
    cursor.execute(query)
    db_connection.commit()
    
    query = "EXPLAIN SELECT * FROM break_index2 WHERE LOWER(strtext) LIKE 'a'"
    res = cursor.execute(query)
    res = cursor.fetchone()
    LOGGER.info(f'First example second table: {res}')

    query = "EXPLAIN SELECT * FROM break_index2 WHERE strtext LIKE 'a%'"
    res = cursor.execute(query)
    res = cursor.fetchone()
    LOGGER.info(f'Second example second table: {res}')

    query = "EXPLAIN SELECT * FROM break_index2 WHERE strtext LIKE NULL"
    res = cursor.execute(query)
    res = cursor.fetchone()
    LOGGER.info(f'Third example second table: {res}')

    query = "EXPLAIN SELECT * FROM break_index2 WHERE strtext LIKE '%a%';"
    res = cursor.execute(query)
    res = cursor.fetchone()
    LOGGER.info(f'Fourth example second table: {res}')

    query = "DROP INDEX str_index ON break_index2"
    cursor.execute(query)
    db_connection.commit()


    cursor.close