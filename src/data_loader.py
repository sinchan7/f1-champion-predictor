import requests
import pandas as pd
import os
from time import sleep

BASE_URL = "https://ergast.com/api/f1"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_json(url):
    response = requests.get(url)
    return response.json()

def fetch_driver_standings(year):
    url = f"{BASE_URL}/{year}/driverStandings.json?limit=1000"
    data = fetch_json(url)
    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    return pd.json_normalize(standings)

def fetch_constructor_standings(year):
    url = f"{BASE_URL}/{year}/constructorStandings.json?limit=1000"
    data = fetch_json(url)
    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    return pd.json_normalize(standings)

def fetch_race_results(year):
    url = f"{BASE_URL}/{year}/results.json?limit=1000"
    data = fetch_json(url)
    races = data['MRData']['RaceTable']['Races']
    if not races:
        return pd.DataFrame()
    
    # Normalize nested 'Results' under each race
    all_results = []
    for race in races:
        for result in race['Results']:
            entry = {**race, **result}
            all_results.append(entry)
    return pd.json_normalize(all_results)

def save_data(start_year=2014, end_year=2023):
    all_driver_standings = []
    all_constructor_standings = []
    all_race_results = []

    for year in range(start_year, end_year + 1):
        print(f"Fetching data for {year}...")

        try:
            # Driver standings
            driver_df = fetch_driver_standings(year)
            driver_df['season'] = year
            all_driver_standings.append(driver_df)

            # Constructor standings
            constructor_df = fetch_constructor_standings(year)
            constructor_df['season'] = year
            all_constructor_standings.append(constructor_df)

            # Race results
            race_df = fetch_race_results(year)
            race_df['season'] = year
            all_race_results.append(race_df)

            sleep(1)  # be nice to the API

        except Exception as e:
            print(f"Error fetching year {year}: {e}")
            continue

    # Save to CSV
    pd.concat(all_driver_standings).to_csv(f"{DATA_DIR}/driver_standings.csv", index=False)
    pd.concat(all_constructor_standings).to_csv(f"{DATA_DIR}/constructor_standings.csv", index=False)
    pd.concat(all_race_results).to_csv(f"{DATA_DIR}/race_results.csv", index=False)

    print("✅ All data fetched and saved to /data folder.")

if __name__ == "__main__":
    save_data()
