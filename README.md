# NutriScan: AI-Powered Dietary Analysis App

NutriScan is an interactive web application developed in Python using the Streamlit framework. It helps users analyze their dietary nutrient intake and provides personalized recommendations for a balanced diet. The app leverages Large Language Models through the Groq API for diet analysis and meal planning. 

<div align="center">
    <h1>
        <a href="https://nutriscanapp.streamlit.app/">🚀 Try the app here! 🚀</a>
    </h1>
</div>


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

## Installation

### Prerequisites
- Python 3.8 or higher
- Git
- A Groq API key (get one at https://console.groq.com)
- pip (Python package installer)
- For voice input: Working microphone and appropriate audio drivers

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/leo-gg/nutriscan.git
cd nutriscan
```

2. Create and activate a virtual environment (optional but recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install required packages:

```bash
# Update pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

Note: For voice input functionality, you might need additional system-level packages:

```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# MacOS (using Homebrew)
brew install portaudio
pip install pyaudio

# Windows
# If PyAudio installation fails, try:
pip install pipwin
pipwin install pyaudio
```

4. Create a `.env` file in the project root directory and add your Groq API key:

```bash
# Create .env file and add your API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

Replace `your_groq_api_key_here` with your actual Groq API key.

5. Run the application:

```bash
streamlit run main.py
```

The app should now be running on http://localhost:8501

### Troubleshooting

If you encounter issues during installation:

1. **PyAudio installation fails**:
   - Windows: Try using pipwin as shown above
   - Linux: Make sure you have portaudio19-dev installed
   - MacOS: Install portaudio via Homebrew first

2. **Package conflicts**:
   - Try installing in a fresh virtual environment
   - Make sure you're using Python 3.8 or higher
   - Update all packages to their latest versions

3. **Streamlit issues**:
   - Check if port 8501 is available
   - Try clearing the Streamlit cache: `streamlit cache clear`
   - Ensure all dependencies are correctly installed

### Important Notes

- Keep your `.env` file private and never commit it to version control
- Voice input requires a working microphone and appropriate audio drivers
- Some features require an active internet connection
- The application has been tested on Python 3.8-3.11
- You need a valid Groq API key to use the AI features

## Authors

- [Leonardo Garma](https://www.linkedin.com/in/lgarma) 
- [Nuria Moreno](https://www.linkedin.com/in/nuria-moreno-marín-28aa52190)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Data4Sustainability challenge 2024
- FAOSTAT for providing dietary data
- Groq for AI capabilities
