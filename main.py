import requests
import sqlite3
import time
from datetime import datetime, timezone
from config import API_KEY, BASE_URL




def create_database():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        humidity INTEGER,
        description TEXT,
        datetime INTEGER,
        data_type TEXT
    )
    """)
    conn.commit()
    conn.close()

# Call this function when the script starts to ensure the schema is updated
create_database()
current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def fetch_and_store(city, data_type):
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "datetime": current_time
        }
        # Convert timestamp to human-readable time
        # readable_time = datetime.fromtimestamp(weather_data["datetime"], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


        # Save to database
        conn = sqlite3.connect("weather_data.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO weather (city, temperature, humidity, description, datetime, data_type)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (weather_data["city"], weather_data["temperature"], weather_data["humidity"],
              weather_data["description"], weather_data["datetime"], data_type))
        conn.commit()
        conn.close()

        # Confirmation with real-time timestamp
        print(f"Weather data saved: {weather_data['city']} at {weather_data['datetime']} as {data_type}")
    else:
        print(f"Error: {response.json().get('message', 'Unable to fetch data')}")

# def run_until_midnight(city):
#     print("Starting weather data collection...")
#     while True:
#         now = datetime.now()
#         # Check if it's past midnight
#         if now.hour == 0 and now.minute == 0:
#             print("It's midnight. Stopping data collection.")
#             break

#         # Fetch and store weather data
#         fetch_and_store(city)

#         # Wait for 30 minutes
#         time.sleep(30 * 60)
           

def run_scheduled(city):
    while True:
        fetch_and_store(city, "history")
        time.sleep(30 * 60)  # Collect every 30 minutes

def view_data():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    # Fetch all data
    cursor.execute("SELECT * FROM weather ORDER BY datetime ASC")
    all_entries = cursor.fetchall()
    conn.close()

    # Separate and display data
    print("\nHistorical Data:")
    for entry in all_entries:
        if entry[6] == "history":  # Check data_type
            readable_time = datetime.utcfromtimestamp(entry[5]).strftime('%Y-%m-%d %H:%M:%S')
            print(f"ID: {entry[0]}, City: {entry[1]}, Temp: {entry[2]}°C, Humidity: {entry[3]}%, "
                  f"Description: {entry[4]}, Time: {readable_time}")

    print("\nNew Queries:")
    for entry in all_entries:
        if entry[6] == "new_query":  # Check data_type
            # readable_time = datetime.utcfromtimestamp(entry[5]).strftime('%Y-%m-%d %H:%M:%S')
            print(f"ID: {entry[0]}, City: {entry[1]}, Temp: {entry[2]}°C, Humidity: {entry[3]}%, "
                  f"Description: {entry[4]}, Time: {current_time}")


if __name__ == "__main__":
    # scheduled_task()
    city = input("Enter a city to check weather: ")
    fetch_and_store(city, "new_query")
    view_data()
    # fetch_and_store()
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)