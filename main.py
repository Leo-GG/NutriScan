# Import required libraries
import streamlit as st  # Web app framework
import pandas as pd  # Data manipulation
import pycountry  # Country data and operations
from langchain_groq import ChatGroq  # Groq LLM integration
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate  # LLM prompt templates
from langchain_core.output_parsers import StrOutputParser  # Parse LLM output
# Import custom modules
from diet_database import get_nutrient_sources  # Database operations
from data_loader import load_reference_values, load_faostat_data, get_faostat_profile  # Data loading utilities
from nutrient_analysis import calculate_results, get_food_recommendations  # Analysis functions
from ui_components import display_results, display_recommendations  # UI components
from meal_planner import generate_meal_plan  # Meal planning functionality
from voice_input import get_voice_input  # Voice input processing
from streamlit_extras.stylable_container import stylable_container  # Styled containers
from dotenv import load_dotenv  # Environment variable management
import os
# Import required for image handling
from PIL import Image

# Define common container style
CONTAINER_STYLE = """
    {    
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
    }
"""

# Extended container style for input section
CONTAINER_STYLE_WITH_CHILDREN = CONTAINER_STYLE + """
    /* Make sure all children also respect container width */
    div {
        max-width: 100%;
        word-wrap: break-word;
    }
    
    /* Handle tables specifically if you have any */
    table {
        width: 100%;
        table-layout: fixed;
    }
"""

# Define data directory path
DATA_DIR = "data"

# Function to load custom CSS
def local_css(file_name):
    with open(os.path.join("data", file_name), "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load necessary data at startup
reference_values, reference_df = load_reference_values()  # Load nutrient reference values
faostat_df = load_faostat_data()  # Load FAOSTAT dietary data

# Initialize database
#create_nutrient_sources_table(os.path.join(DATA_DIR, "nutrient_sources.db"))  # Pass the new path
nutrient_sources = get_nutrient_sources(os.path.join(DATA_DIR, "nutrient_sources.db"))  # Pass the new path

# Load environment variables
load_dotenv()

# Initialize the LLM model
model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name='llama-3.2-90b-text-preview',
    temperature=0.0  # Set to 0 for deterministic outputs
)

# Define system message template for the LLM
system_message = SystemMessagePromptTemplate.from_template(f"""You are given a list of food items or meals and you need to estimate 
                                                           the total nutrient content of the diet. The nutrients that you have to 
                                                           consider are: {', '.join(reference_values.keys())}.
                                                           Write the estimated amount of each nutrient separated by semicolons, with 
                                                           the format "Nutrient name: value;". Answer always in English, use the nutrient
                                                           names exactly as they are in the list above.
                                                           Only provide estimates for the nutrients listed above.
                                                           You are brief. You do not comment on the results.
                                                           If you don't know the nutrient content of a food item or meal, you say 'unknown'.
                                                           If you don't recognize a food item, you can ask for clarification or you can make an estimation based on the context.
                                                           """)

# Get list of all countries from pycountry
all_countries = [country.name for country in pycountry.countries]

# Function to generate LLM response
def generate_response(chat_history):
    chat_template = ChatPromptTemplate.from_messages(chat_history)
    chain = chat_template | model | StrOutputParser()
    response = chain.invoke({})
    return response

# Function to parse LLM response into structured data
def parse_response(response):
    try:
        # Skip lines until we find one containing a colon
        lines = response.split('\n')
        while lines and ':' not in lines[0]:
            lines.pop(0)
        
        data = {}
        estimates = lines[0].split(';')
        
        # Process each nutrient estimate
        for line in estimates: 
            parts = line.split(':')
            if len(parts) == 2:
                nutrient = parts[0].strip()
                value = parts[1].strip()
                
                # Only process nutrients that are in our reference list
                if nutrient in reference_values:
                    import re
                    # Handle decimal numbers with commas
                    value = value.replace(',', '.')
                    match = re.match(r'(\d+(?:\.\d+)?)\s*(\w+)', value)
                    if match:
                        numeric_value, unit = match.groups()
                        data[nutrient] = float(numeric_value)
                    else:
                        data[nutrient] = 0.0  # Default to 0 if parsing fails
        
        return data
    except Exception as e:
        st.error(f"Failed to parse the response into a table: {str(e)}")
        return None

# Main application function
def main():
    # Configure the page
    st.set_page_config(layout="wide", page_title="NutriScan", page_icon="🍽️")
    local_css("style.css")

    # Display app introduction and description
    st.markdown("""
                
                <h2 style='text-align: center;'>Hi! We are <a href=https://www.linkedin.com/in/nuria-moreno-marín-28aa52190">Nuria</a> and 
                <a href=https://www.linkedin.com/in/lgarma">Leo</a> and this is our entry for the
                <a href=https://www.datais.es/dataton-sostenibilidad">Data4Sustainability challenge 2024</a> from <a href=https://www.datais.es>Datais</a>! 
                </h2>
                <br>
                <br>
""", unsafe_allow_html=True)
    
    col1, col_photo1,col3, col_photo2, col5 = st.columns(5)

    with col_photo1:
        try:
            image = Image.open('data/Nuria.png')
            st.image(image, width=200, use_column_width=True, caption="Nuria Moreno")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load image: {e}")

    with col_photo2:
        try:
            image = Image.open('data/Leo.png')
            st.image(image, width=200, use_column_width=True, caption="Leonardo Garma")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load image: {e}")

    st.markdown("""
                <h3 style='text-align: justify;'>We are a team of 2 spanish scientists passionate 
                about using data to make a positive impact. We decided to join forces to tackle challenge #3
                by developing <b>NutriScan</b>, an AI-powered app that estimates and analyzes nutrient intakes and makes personalized 
                recommendations for a balanced diet.</h3>
                <br>
                <br>
                <h2 style='text-align: center;'>Our app consists of 3 main parts</h2>
                <br>
                <br>
                """, unsafe_allow_html=True)

    # Create three columns for app features description
    col_left, col_middle, col_right = st.columns([0.3,0.3, 0.3])
    
    # Display feature descriptions in columns
    with col_left:
        with stylable_container(
                key="container_with_border",
                css_styles=CONTAINER_STYLE
            ):
            st.markdown("""
                <h2 style='text-align: center;'>Diet Estimation</h2>
                <h4 style='text-align: justify;'>You can use our app to estimate the nutrient content of a diet
                by either using FAOSTAT data or describing your diet using text or voice input to an LLM.</h4>
                <br>
                <h4 style='text-align: justify;'>And of course you can input or modify any of the values manually.</h4>
                <br>
                <br>
            """, unsafe_allow_html=True)
    with col_middle:
        with stylable_container(
                key="container_with_border",
                css_styles=CONTAINER_STYLE
            ):
            st.markdown("""
                <h2 style='text-align: center;'>Diet Analysis</h2>
                <h4 style='text-align: justify;'>Once you have estimated the nutrient content of your diet, you can 
                analyze it by comparing it to recommended values to detect any deficiencies or excesses.</h4>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
            """, unsafe_allow_html=True)

    with col_right:
        with stylable_container(
                key="container_with_border",
                css_styles=CONTAINER_STYLE
            ):
            st.markdown("""
                <h2 style='text-align: center;'>Recommendations</h2>
                <h4 style='text-align: justify;'>After the analysis, you can get personalized recommendations 
                to balance your diet.</h4>
                <br>
                <h4 style='text-align: justify;'>You can generate a weekly meal plan, which addresses the deficiencies 
                and excesses detected and takes into account the country you live in.</h4>
                <br>
                <br>
            """, unsafe_allow_html=True)

    st.markdown("""
                <br>
                <br>
                <h2 style='text-align: center;'>Have fun testing it!</h2>
                <br>
                <br>
                """, unsafe_allow_html=True)
    
    with stylable_container(
        key="app-title",
        css_styles="""
            {    
                background-color: #4CAF50;
                color: white;
                padding: 2rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                text-align: center;
            }
            """,
    ):  # Use stylable_container for the app header
        st.markdown("""
            <h1>🍽️ NutriScan App</h1>
            <p>Analyze your diet and get personalized recommendations</p>
        """, unsafe_allow_html=True)
    
    # Initialize session state variables if they don't exist
    if 'show_meal_plan' not in st.session_state:
        st.session_state.show_meal_plan = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'estimated_intakes' not in st.session_state:
        st.session_state.estimated_intakes = None
    if 'meal_plan' not in st.session_state:
        st.session_state.meal_plan = None
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = None

    # Create main layout columns
    col_input, col_results = st.columns([0.4, 0.6])
    
    submitted = False
    intakes = {}

    # Input section
    with col_input:
        with stylable_container(
        key="container_with_border",
        css_styles=CONTAINER_STYLE_WITH_CHILDREN
        ):  # Use stylable_container for the input section
            st.subheader("Diet Input")
            
            input_method = st.radio("Choose input method:", ("FAOSTAT Data Profiles", "LLM Estimation", "Manual"), horizontal=True)
            
            if input_method == "FAOSTAT Data Profiles":
                countries = faostat_df['Survey'].unique()
                selected_country = st.selectbox("Select a country:", countries)
                st.session_state.selected_country = selected_country
                
                subpopulations = faostat_df[faostat_df['Survey'] == selected_country]['Geographic Level'].unique()
                selected_subpopulation = st.selectbox("Select a subpopulation:", subpopulations)
                
                if st.button("Load FAOSTAT Profile"):
                    faostat_intakes = get_faostat_profile(faostat_df, selected_country, selected_subpopulation, reference_values)
                    if faostat_intakes:
                        st.session_state.estimated_intakes = faostat_intakes
                        st.success(f"Loaded dietary profile for {selected_country} - {selected_subpopulation}")
                        # Debug output
                        #st.write("Loaded profile:", faostat_intakes)
                    else:
                        st.error("No matching data found for the selected country and subpopulation.")
                
                if st.session_state.estimated_intakes:
                    st.subheader("FAOSTAT Profile - Adjust if needed")
                    adjusted_intakes = {}
                    with st.form("adjust_faostat_profile"):
                        for nutrient, intake in st.session_state.estimated_intakes.items():
                            if nutrient in reference_values:
                                adjusted_intakes[nutrient] = st.number_input(
                                    f"{nutrient} ({reference_df.loc[reference_df['Indicator'] == nutrient, 'Unit'].values[0]})",
                                    value=float(intake),
                                    help=f"FAOSTAT value: {intake}, Reference: {reference_values.get(nutrient, 'N/A')}"
                                )
                        submitted = st.form_submit_button("Analyze Adjusted FAOSTAT Profile")
                    
                    if submitted:
                        intakes = adjusted_intakes
            else:
                st.session_state.selected_country = st.selectbox("Select your country of residence:", all_countries, index=all_countries.index("United States"))
            
            if input_method == "Manual":
                with st.form("nutrient_form"):
                    for nutrient, reference in reference_values.items():
                        intakes[nutrient] = st.number_input(
                            f"{nutrient} ({reference_df.loc[reference_df['Indicator'] == nutrient, 'Unit'].values[0]})",
                            value=0.0,
                            help=f"Reference value: {reference}"
                        )
                    submitted = st.form_submit_button("Analyze Diet")
            elif input_method == "LLM Estimation":
                with st.form("llm_form"):
                    text = st.text_area("Describe your diet:")
                    use_voice = st.checkbox("Use voice input")
                    estimate_submitted = st.form_submit_button("Estimate Nutrient Content")
                
                if estimate_submitted:
                    if use_voice:
                        text = get_voice_input()
                    if text:
                        with st.spinner("Estimating nutrient content..."):
                            prompt = HumanMessagePromptTemplate.from_template(text)
                            chat_history = [system_message, prompt]
                            response = generate_response(chat_history)
                            st.session_state.chat_history.append({'user': text, 'assistant': response})
                            # Debug output
                            # st.write(response)
                            intakes = parse_response(response)
                            if intakes:
                                st.session_state.estimated_intakes = intakes
                                st.success("Nutrient content estimated successfully!")

                                # Debug output
                                #st.write("Estimated intakes:", intakes)
                            else:
                                st.error("Failed to estimate nutrient content. Please try again.")
                                return
                
                if st.session_state.estimated_intakes:
                    st.subheader("Estimated Nutrient Intakes")
                    st.write("You can adjust these values if needed:")
                    
                    adjusted_intakes = {}
                    with st.form("adjust_estimates"):
                        for nutrient, intake in st.session_state.estimated_intakes.items():
                            adjusted_intakes[nutrient] = st.number_input(
                                f"{nutrient} ({reference_df.loc[reference_df['Indicator'] == nutrient, 'Unit'].values[0]})",
                                value=float(intake),
                                help=f"Estimated: {intake}, Reference: {reference_values.get(nutrient, 'N/A')}"
                            )
                        submitted = st.form_submit_button("Analyze Adjusted Diet")
                    
                    if submitted:
                        intakes = adjusted_intakes

            st.markdown('</div>', unsafe_allow_html=True)

    # Results section
    if submitted and intakes:
        st.session_state.results = calculate_results(intakes, reference_values)
        
    if 'results' in st.session_state:
        with col_results:
            with stylable_container(
                key="container_with_border",
                css_styles=CONTAINER_STYLE
            ):  # Use stylable_container for results
                #st.markdown("<h2 style='text-align: center;'>Analysis Results and Recommendations</h2>", unsafe_allow_html=True)
                display_results(st.session_state.results, reference_df)
                st.markdown('</div>', unsafe_allow_html=True)
        
        col_recommendations, col_meal_plan = st.columns(2)
        
        with col_recommendations:
            with stylable_container(
                key="container_with_border",
                css_styles=CONTAINER_STYLE
            ):  # Use stylable_container for recommendations
                st.subheader("Dietary Recommendations")
                display_recommendations(st.session_state.results, nutrient_sources)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col_meal_plan:
            with stylable_container(
                key="container_with_border",
                css_styles=CONTAINER_STYLE
            ):  # Use stylable_container for meal plan
                st.subheader("Meal Planner")
                if st.button("Generate Meal Plan", key="generate_meal_plan"):
                    with st.spinner("Generating meal plan..."):
                        st.session_state.meal_plan = generate_meal_plan(st.session_state.results, st.session_state.selected_country)
                    st.session_state.show_meal_plan = True
            
                if st.session_state.show_meal_plan and st.session_state.meal_plan:
                    st.markdown(f"<h4>Weekly Meal Plan for {st.session_state.selected_country}</h4>", unsafe_allow_html=True)
                    st.markdown(st.session_state.meal_plan)
                elif st.session_state.show_meal_plan:
                    st.error("Failed to generate meal plan. Please try again.")
                st.markdown('</div>', unsafe_allow_html=True)

# Entry point
if __name__ == "__main__":
    main()
