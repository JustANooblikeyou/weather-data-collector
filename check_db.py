import sqlite3

def check_database():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM weather")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    check_database()
