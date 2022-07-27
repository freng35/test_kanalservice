import psycopg2
from psycopg2 import Error


try:
    # conn = psycopg2.connect(
    #                         database='postgres',
    #                         user='postgres',
    #                         password='1234',
    #                         host='localhost',
    #                         port='5432'
    # )
    conn = psycopg2.connect(
                            user='root',
                            password='1234',
                            host='supply_db',
                            port='5432'
    )
    cur = conn.cursor()

    # task = """
    #     CREATE TABLE IF NOT EXISTS project_supply(
    #     id INT,
    #     order_num INT,
    #     dollar_cost INT,
    #     date_supply TEXT,
    #     ruble_cost FLOAT
    #     );
    # """
    #
    # cur.execute(task)
    # try:
    #     cur.execute(task)
    # except (Exception, Error) as error:
    #     print("Error db", error)

except (Exception, Error) as error:
    print("Error db", error)


def drop_table():
    task = f"""
        DELETE FROM project_supply
	    WHERE id != -1
    """

    cur.execute(task)
    conn.commit()


def add_record(_id, order_num, dollar_cost, date_supply, ruble_cost):
    task = f"""
    INSERT INTO project_supply(id, order_num, dollar_cost, date_supply, ruble_cost)
    VALUES({_id}, {order_num}, {dollar_cost}, {repr(str(date_supply))}, {ruble_cost})
    """
    cur.execute(task)
    conn.commit()


def get_records():
    task = f"""
    SELECT * FROM project_supply
    """
    cur.execute(task)
    conn.commit()
    records = []
    for i in cur:
        records.append(i)
    return records

