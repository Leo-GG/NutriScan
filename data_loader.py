import pandas as pd
import os

# Define data directory path
DATA_DIR = "data"

def load_reference_values():
    """
    Load nutrient reference values from CSV file
    
    Returns:
        Tuple[Dict, pd.DataFrame]: 
        - Dictionary mapping nutrient names to reference values
        - DataFrame containing full reference data
    """
    reference_df = pd.read_csv(os.path.join(DATA_DIR, 'Indicators_brief.csv'))
    return dict(zip(reference_df['Indicator'], reference_df['Value'])), reference_df

def load_faostat_data():
    """
    Load and preprocess FAOSTAT dietary data
    
    Returns:
        pd.DataFrame: Processed FAOSTAT data with cleaned survey names
    """
    faostat_df = pd.read_csv(os.path.join(DATA_DIR, 'FAOSTAT_total_intakes.csv'))
    # Clean survey names by removing text after dash
    faostat_df['Survey'] = [i.split(' -')[0] for i in faostat_df['Survey'].values]
    return faostat_df

def get_faostat_profile(faostat_df, country, subpopulation, reference_values):
    """
    Extract dietary profile for specific country and subpopulation
    
    Args:
        faostat_df: DataFrame containing FAOSTAT data
        country: Country name
        subpopulation: Subpopulation identifier
        reference_values: Dictionary of reference values
    
    Returns:
        Dict: Dietary profile containing nutrient intakes
        Returns only nutrients that are in the reference values list
    """
    # Filter data for specific country and subpopulation
    profile = faostat_df[(faostat_df['Survey'] == country) & 
                        (faostat_df['Geographic Level'] == subpopulation)]
    
    result = {}
    for _, row in profile.iterrows():
        indicator = row['Indicator']
        value = row['Value']
        # Only include values that are not null and have a reference value
        if pd.notnull(value) and indicator in reference_values:
            result[indicator] = float(value)
    
    return result
