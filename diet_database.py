import sqlite3
import pandas as pd
import os

def create_nutrient_sources_table(db_path="data/nutrient_sources.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS nutrient_sources
                 (nutrient TEXT, food TEXT, content REAL, unit TEXT)''')
    
    # Read nutrients from Indicators_brief.csv
    indicators_df = pd.read_csv('data/Indicators_brief.csv')
    nutrients = indicators_df['Indicator'].tolist()

    # Insert data for all nutrients
    data = [
        # Energy
        ('Energy', 'Brown rice (cooked)', 112, 'kcal/100g'),
        ('Energy', 'Chicken breast (cooked)', 165, 'kcal/100g'),
        ('Energy', 'Avocado', 160, 'kcal/100g'),
        ('Energy', 'Whole wheat bread', 247, 'kcal/100g'),
        ('Energy', 'Banana', 89, 'kcal/100g'),
        
        # Protein
        ('Protein', 'Chicken breast (cooked)', 31, 'g/100g'),
        ('Protein', 'Greek yogurt', 10, 'g/100g'),
        ('Protein', 'Lentils (cooked)', 9, 'g/100g'),
        ('Protein', 'Almonds', 21, 'g/100g'),
        ('Protein', 'Salmon (cooked)', 22, 'g/100g'),
        
        # Fat
        ('Fat', 'Olive oil', 100, 'g/100g'),
        ('Fat', 'Avocado', 15, 'g/100g'),
        ('Fat', 'Almonds', 49, 'g/100g'),
        ('Fat', 'Salmon (cooked)', 13, 'g/100g'),
        ('Fat', 'Chia seeds', 31, 'g/100g'),
        
        # Carbohydrate
        ('Carbohydrate (available)', 'Brown rice (cooked)', 23, 'g/100g'),
        ('Carbohydrate (available)', 'Banana', 23, 'g/100g'),
        ('Carbohydrate (available)', 'Sweet potato (cooked)', 20, 'g/100g'),
        ('Carbohydrate (available)', 'Whole wheat bread', 41, 'g/100g'),
        ('Carbohydrate (available)', 'Oatmeal (cooked)', 12, 'g/100g'),
        
        # Dietary Fibre
        ('Dietary Fibre', 'Chia seeds', 34, 'g/100g'),
        ('Dietary Fibre', 'Lentils (cooked)', 8, 'g/100g'),
        ('Dietary Fibre', 'Almonds', 12, 'g/100g'),
        ('Dietary Fibre', 'Raspberries', 7, 'g/100g'),
        ('Dietary Fibre', 'Broccoli (cooked)', 3.3, 'g/100g'),
        
        # Calcium
        ('Calcium', 'Greek yogurt', 115, 'mg/100g'),
        ('Calcium', 'Sardines (canned with bones)', 382, 'mg/100g'),
        ('Calcium', 'Kale (cooked)', 150, 'mg/100g'),
        ('Calcium', 'Tofu (firm)', 350, 'mg/100g'),
        ('Calcium', 'Almonds', 269, 'mg/100g'),
        
        # Iron
        ('Iron', 'Spinach (cooked)', 3.6, 'mg/100g'),
        ('Iron', 'Lentils (cooked)', 3.3, 'mg/100g'),
        ('Iron', 'Beef (cooked)', 2.6, 'mg/100g'),
        ('Iron', 'Pumpkin seeds', 8.8, 'mg/100g'),
        ('Iron', 'Quinoa (cooked)', 1.5, 'mg/100g'),
        
        # Zinc
        ('Zinc', 'Oysters (cooked)', 78.6, 'mg/100g'),
        ('Zinc', 'Beef (cooked)', 6.3, 'mg/100g'),
        ('Zinc', 'Pumpkin seeds', 7.8, 'mg/100g'),
        ('Zinc', 'Lentils (cooked)', 1.3, 'mg/100g'),
        ('Zinc', 'Greek yogurt', 0.7, 'mg/100g'),
        
        # Magnesium
        ('Magnesium', 'Pumpkin seeds', 592, 'mg/100g'),
        ('Magnesium', 'Spinach (cooked)', 87, 'mg/100g'),
        ('Magnesium', 'Almonds', 270, 'mg/100g'),
        ('Magnesium', 'Black beans (cooked)', 70, 'mg/100g'),
        ('Magnesium', 'Avocado', 29, 'mg/100g'),
        
        # Phosphorus
        ('Phosphorus', 'Salmon (cooked)', 280, 'mg/100g'),
        ('Phosphorus', 'Greek yogurt', 135, 'mg/100g'),
        ('Phosphorus', 'Chicken breast (cooked)', 210, 'mg/100g'),
        ('Phosphorus', 'Lentils (cooked)', 180, 'mg/100g'),
        ('Phosphorus', 'Almonds', 481, 'mg/100g'),
        
        # Potassium
        ('Potassium', 'Sweet potato (cooked)', 475, 'mg/100g'),
        ('Potassium', 'Banana', 358, 'mg/100g'),
        ('Potassium', 'Spinach (cooked)', 466, 'mg/100g'),
        ('Potassium', 'Salmon (cooked)', 360, 'mg/100g'),
        ('Potassium', 'Avocado', 485, 'mg/100g'),
        
        # Thiamin
        ('Thiamin', 'Pork (cooked)', 0.7, 'mg/100g'),
        ('Thiamin', 'Sunflower seeds', 1.5, 'mg/100g'),
        ('Thiamin', 'Black beans (cooked)', 0.2, 'mg/100g'),
        ('Thiamin', 'Brown rice (cooked)', 0.1, 'mg/100g'),
        ('Thiamin', 'Trout (cooked)', 0.1, 'mg/100g'),
        
        # Riboflavin
        ('Riboflavin', 'Almonds', 1.1, 'mg/100g'),
        ('Riboflavin', 'Beef liver (cooked)', 3.0, 'mg/100g'),
        ('Riboflavin', 'Greek yogurt', 0.3, 'mg/100g'),
        ('Riboflavin', 'Spinach (cooked)', 0.2, 'mg/100g'),
        ('Riboflavin', 'Mushrooms (cooked)', 0.3, 'mg/100g'),
        
        # Vitamin B6
        ('Vitamin B6', 'Chickpeas (cooked)', 0.2, 'mg/100g'),
        ('Vitamin B6', 'Salmon (cooked)', 0.6, 'mg/100g'),
        ('Vitamin B6', 'Banana', 0.4, 'mg/100g'),
        ('Vitamin B6', 'Potato (baked)', 0.3, 'mg/100g'),
        ('Vitamin B6', 'Chicken breast (cooked)', 0.5, 'mg/100g'),
        
        # Vitamin A (retinol equivalents)
        ('Vitamin A (retinol equivalents)', 'Sweet potato (cooked)', 961, 'μg/100g'),
        ('Vitamin A (retinol equivalents)', 'Spinach (cooked)', 524, 'μg/100g'),
        ('Vitamin A (retinol equivalents)', 'Carrots (cooked)', 852, 'μg/100g'),
        ('Vitamin A (retinol equivalents)', 'Kale (cooked)', 681, 'μg/100g'),
        ('Vitamin A (retinol equivalents)', 'Beef liver (cooked)', 9442, 'μg/100g'),
        
        # Vitamin A (retinol activity equivalents)
        ('Vitamin A (retinol activity equivalents)', 'Sweet potato (cooked)', 961, 'μg/100g'),
        ('Vitamin A (retinol activity equivalents)', 'Spinach (cooked)', 469, 'μg/100g'),
        ('Vitamin A (retinol activity equivalents)', 'Carrots (cooked)', 852, 'μg/100g'),
        ('Vitamin A (retinol activity equivalents)', 'Kale (cooked)', 681, 'μg/100g'),
        ('Vitamin A (retinol activity equivalents)', 'Beef liver (cooked)', 9442, 'μg/100g'),
        
        # Vitamin C
        ('Vitamin C', 'Red bell pepper (raw)', 128, 'mg/100g'),
        ('Vitamin C', 'Kiwi', 93, 'mg/100g'),
        ('Vitamin C', 'Broccoli (cooked)', 65, 'mg/100g'),
        ('Vitamin C', 'Strawberries', 59, 'mg/100g'),
        ('Vitamin C', 'Orange', 53, 'mg/100g'),
        
        # Vitamin B12
        ('Vitamin B12', 'Clams (cooked)', 84.1, 'μg/100g'),
        ('Vitamin B12', 'Salmon (cooked)', 2.8, 'μg/100g'),
        ('Vitamin B12', 'Beef (cooked)', 2.1, 'μg/100g'),
        ('Vitamin B12', 'Greek yogurt', 0.5, 'μg/100g'),
        ('Vitamin B12', 'Eggs', 1.1, 'μg/100g')
    ]
    
    c.executemany('INSERT INTO nutrient_sources VALUES (?,?,?,?)', data)
    
    conn.commit()
    conn.close()

def get_nutrient_sources(db_path="data/nutrient_sources.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('SELECT nutrient, food, content, unit FROM nutrient_sources')
    data = c.fetchall()
    
    nutrient_sources = {}
    for nutrient, food, content, unit in data:
        if nutrient not in nutrient_sources:
            nutrient_sources[nutrient] = {}
        nutrient_sources[nutrient][food] = (content, unit)
    
    conn.close()
    return nutrient_sources

if __name__ == "__main__":
    create_nutrient_sources_table()
