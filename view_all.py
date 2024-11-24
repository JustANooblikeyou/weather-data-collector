import sqlite3
from datetime import datetime

def view_all_weather():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    # Query all entries
    cursor.execute("SELECT * FROM weather ORDER BY id ASC")
    all_entries = cursor.fetchall()
    conn.close()

    # Print all entries with readable timestamps
    print("\nAll Weather Data Stored:")
    for entry in all_entries:
        readable_time = datetime.utcfromtimestamp(entry[5]).strftime('%Y-%m-%d %H:%M:%S')
        print(f"ID: {entry[0]}, City: {entry[1]}, Temp: {entry[2]}°C, Humidity: {entry[3]}%, "
              f"Description: {entry[4]}, Time: {readable_time}")

if __name__ == "__main__":
    view_all_weather()
