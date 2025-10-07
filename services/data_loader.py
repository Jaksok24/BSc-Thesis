import pandas as pd
from services.db_connector import connect_to_db, close_db

def get_data_to_dataframe(querry):
    conn, c = connect_to_db()
    c.execute(querry)
    rows = c.fetchall()
    column_names = [description[0] for description in c.description]
    df = pd.DataFrame(rows, columns=column_names)
    close_db(conn)
    return df
