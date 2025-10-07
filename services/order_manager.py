from services.db_connector import *

def get_drivers():
    conn, c = connect_to_db()
    c.execute("SELECT imie_nazwisko FROM uzytkownicy WHERE rola='Kierowca'")
    drivers = c.fetchall()
    close_db(conn)
    return drivers

def get_trucks():
    conn, c = connect_to_db()
    c.execute("SELECT rejestracja FROM pojazdy")
    trucks = c.fetchall()
    close_db(conn)
    return trucks  

def add_order(customer, vehicle, driver, status, loading_location, unloading_localization, loading_data, unloading_data):
    conn, c = connect_to_db()
    c.execute("""INSERT INTO zlecenia
              (klient, pojazd, kierowca, status, miejsce_zaladunku, miejsce_rozladunku, data_zaladunku, data_rozladunku)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
              (customer, vehicle, driver, status, loading_location, unloading_localization, loading_data, unloading_data))
    conn.commit()
    close_db(conn)

def edit_order(order_id, customer, vehicle, driver, status, loading_location, unloading_location, loading_data, unloading_data):
    conn, c = connect_to_db()
    c.execute("""UPDATE zlecenia
              SET klient = ?, pojazd = ?, kierowca = ?, status = ?, miejsce_zaladunku = ?, miejsce_rozladunku = ?, data_zaladunku = ?, data_rozladunku = ?
              WHERE oID = ?""",
              (customer, vehicle, driver, status, loading_location, unloading_location, loading_data, unloading_data, order_id))
    conn.commit()
    close_db(conn)
    
def update_order(order_id, status):
    conn, c = connect_to_db()
    c.execute("UPDATE zlecenia SET status = ? WHERE oID = ?", (status, order_id))
    conn.commit()
    close_db(conn)
