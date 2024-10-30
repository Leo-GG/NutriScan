# NutriScan: AI-Powered Dietary Analysis App

NutriScan is an interactive web application developed in Python using the Streamlit framework. It helps users analyze their dietary nutrient intake and provides personalized recommendations for a balanced diet. The app leverages Large Language Models through the Groq API for diet analysis and meal planning. 

This project was developed by Leonardo Garma and Nuria Moreno as an entry for the [Data4Sustainability challenge 2024](https://www.datais.es/dataton-sostenibilidad).

## Features

### 1. Diet Input & Estimation
- **FAOSTAT Data Profiles**: Load and customize dietary profiles from the FAOSTAT data used in the challenge
- **LLM Estimation**: Use AI to estimate nutrient content from text descriptions of meals
- **Voice Input**: Describe your diet using voice input
- **Manual Input**: Enter nutrient values manually

### 2. Diet Analysis
- Visual representation of nutrient intake compared to reference values
- Color-coded status indicators (Deficient, Borderline, Adequate, High, Excess)
- Detailed analysis table with specific values and percentages

### 3. Recommendations
- Personalized dietary recommendations based on analysis results
- Specific food suggestions to address deficiencies or excesses
- Nutrient-specific tips for better absorption and intake
- AI-generated weekly meal plans tailored to your country of residence

## Resources

- **Frontend & Backend**: Python with Streamlit
- **Data Analysis**: Pandas, Plotly
- **AI Integration**: Groq API with LangChain
- **Data Sources**: FAOSTAT, custom nutrient databases

