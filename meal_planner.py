from langchain_ollama import ChatOllama
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

meal_planner_model = ChatOllama(model="llama3.2", base_url="http://localhost:11434/", temperature=0.2)

meal_planner_system_message = SystemMessagePromptTemplate.from_template("""You are a nutritionist and meal planner. 
Given a detailed analysis of a person's nutrient intake, you will create a meal plan for a week with 3 meals per day. 
Focus on addressing any nutrient deficiencies and maintaining a balanced diet. 
Provide a brief explanation for each day's meals and how they address the nutritional needs.""")

def generate_meal_plan(analysis_results, country):
    try:
        formatted_results = "\n".join([f"{row['Nutrient']}: Intake {row['Intake']:.2f}, Reference {row['Reference']:.2f}, Status {row['Status']}" for _, row in analysis_results.iterrows()])
        
        prompt = HumanMessagePromptTemplate.from_template(f"Based on this nutrient analysis:\n\n{formatted_results}\n\nCreate a meal plan for a week with 3 meals per day for someone living in {country}. Consider local cuisine and available ingredients.")
        chat_history = [meal_planner_system_message, prompt]
        chat_template = ChatPromptTemplate.from_messages(chat_history)
        chain = chat_template | meal_planner_model | StrOutputParser()
        response = chain.invoke({})
        return response
    except Exception as e:
        return f"Error generating meal plan: {str(e)}"
