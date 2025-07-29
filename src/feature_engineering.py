import pandas as pd

def load_data(results_path, constructor_standings_path):
    results = pd.read_csv(results_path)
    standings = pd.read_csv(constructor_standings_path)
    
    # Clean columns
    results.columns = results.columns.str.strip().str.lower()
    standings.columns = standings.columns.str.strip().str.lower()
    
    return results, standings

def engineer_driver_features(results):
    # Add position = 1 for all rows (since only winners are present)
    results['position'] = 1

    # Wins per driver per season
    driver_wins = results.groupby(['season', 'driver']).size().reset_index(name='wins')

    # Total seasons participated
    seasons_participated = results.groupby('driver')['season'].nunique().reset_index(name='seasons_participated')

    # Merge
    driver_features = pd.merge(driver_wins, seasons_participated, on='driver')

    # Determine champion per season (most wins)
    driver_features['is_champion'] = driver_features.groupby('season')['wins'].transform(lambda x: x == x.max()).astype(int)

    return driver_features

def engineer_constructor_features(results, standings):
    # Add position = 1 for all rows
    results['position'] = 1

    # Wins per constructor per season
    constructor_wins = results.groupby(['season', 'constructor']).size().reset_index(name='wins')

    # Final championship positions from standings
    champ_position = standings.copy()
    champ_position.columns = champ_position.columns.str.strip().str.lower()

    # Filter: only top constructor per season (position == 1)
    top_constructors = champ_position[champ_position['position'] == 1][['season', 'constructor']].copy()
    top_constructors['is_champion'] = 1

    # Merge with win counts
    constructor_features = pd.merge(constructor_wins, top_constructors, on=['season', 'constructor'], how='left')
    constructor_features['is_champion'] = constructor_features['is_champion'].fillna(0).astype(int)

    return constructor_features
