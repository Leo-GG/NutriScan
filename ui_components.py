import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from nutrient_analysis import get_food_recommendations

def display_results(df_results, reference_df):
    """
    Display the analysis results using a bar chart and detailed table
    
    Args:
        df_results: DataFrame containing analysis results
        reference_df: DataFrame containing reference values and units
    """
    # Display section title
    st.markdown("<h2 style='text-align: center;'>Diet Overview</h2>", unsafe_allow_html=True)
    
    # Define color scheme for different nutrient statuses
    color_map = {
        'green': '#2ecc71',   # Adequate
        'yellow': '#f1c40f',  # Borderline
        'red': '#e74c3c',     # Deficient
        'orange': '#e67e22',  # High
        'purple': '#9b59b6'   # Excess
    }
    
    # Create bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_results['Nutrient'],
        y=df_results['Percentage'],
        marker_color=[color_map[color] for color in df_results['Color']],
        text=df_results['Percentage'].round(1).astype(str) + '%',
        textposition='outside'
    ))

    # Configure chart layout with responsive sizing
    fig.update_layout(
        title={
            'text': 'Nutrient Intake as Percentage of Reference Values',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis_title='Percentage of Reference Value',
        yaxis_range=[0, max(df_results['Percentage'].max() * 1.2, 120)],
        xaxis_tickangle=-45,
        height=500,  # Reduced height
        margin=dict(t=100, b=50, l=50, r=100),  # Increased bottom margin for labels
        autosize=True,  # Enable responsive sizing
        # Make the plot fit in the container width
        width=1000,
        showlegend=False
    )

    # Add reference line at 100%
    fig.add_hline(y=100, line_dash="dash", line_color="gray")
    
    # Display the plot with container width constraint and hide modebar
    st.plotly_chart(
        fig, 
        use_container_width=False, 
        config={
            'displayModeBar': True,  # Hide the modebar completely
            'responsive': True
        }
    )

    # Create detailed analysis table
    st.markdown("<h2 style='text-align: center;'>Detailed Analysis</h2>", unsafe_allow_html=True)

    # Prepare detailed results DataFrame
    detailed_results = pd.DataFrame({
        'Intake': [f"{val:.2f} {unit}" for val, unit in zip(df_results['Intake'].values, reference_df['Unit'].values)],
        'Reference': [f"{val:.2f} {unit}" for val, unit in zip(df_results['Reference'].values, reference_df['Unit'].values)],
        'Percentage': [f"{val:.2f}%" for val in df_results['Percentage'].values],
        'Status': df_results['Status'].values
    }, index=df_results['Nutrient'])
    
    # Function to color-code status cells
    def color_status(val):
        if val == 'Adequate':
            return 'background-color: #2ecc71'
        elif val == 'Borderline':
            return 'background-color: #f1c40f'
        elif val == 'High':
            return 'background-color: #e67e22'
        elif val == 'Excess':
            return 'background-color: #9b59b6'
        else:  # Deficient
            return 'background-color: #e74c3c'

    # Apply styling and display table
    styled_results = detailed_results.style.applymap(color_status, subset=['Status'])
    table_html = styled_results.to_html(escape=False)
    
    # Center the table
    centered_table_html = f"""
    <div style="display: flex; justify-content: center; width: 100%;">
        <div style="width: 80%;">
            {table_html}
    """
    
    st.markdown(centered_table_html, unsafe_allow_html=True)

def display_recommendations(df_results, nutrient_sources):
    """
    Display dietary recommendations based on analysis results
    
    Args:
        df_results: DataFrame containing analysis results
        nutrient_sources: Dictionary containing food sources for each nutrient
    """
    # Get nutrients that need adjustment
    deficient_nutrients = df_results[df_results['Status'].isin(['Deficient', 'High', 'Excess'])]
    
    if not deficient_nutrients.empty:
        st.warning("Your diet needs adjustment for the following nutrients:")
        
        # Process each nutrient that needs adjustment
        for _, row in deficient_nutrients.iterrows():
            nutrient = row['Nutrient']
            current = row['Intake']
            reference = row['Reference']
            difference = reference - current
            status = row['Status']
            
            # Determine action and color based on status
            if status in ['High', 'Excess']:
                action_color = 'orange'
                action_text = 'reduce'
            else:  # Deficient
                action_color = 'red'
                action_text = 'increase'
            
            # Display nutrient status and recommended action
            st.subheader(f"🔍 {nutrient}")
            st.markdown(f"""
                <h3>Current intake: <span style='color: {action_color}; font-weight: bold;'>{current:.1f}</span> | 
                Recommended action: <span style='color: {action_color}; font-weight: bold;'>{action_text} by {abs(difference):.1f}</span></h3>
                """, unsafe_allow_html=True)
            
            # Get and display food recommendations
            recommendations = get_food_recommendations(nutrient, current, reference, nutrient_sources)
            
            if recommendations:
                st.write("Suggested food modifications:")
                # Create recommendations DataFrame
                rec_df = pd.DataFrame(
                    [(f"{amount:.1f}g", f"{content:.1f}{unit}", action.capitalize()) 
                     for food, (amount, unit, content, action) in recommendations.items()],
                    index=[food for food in recommendations.keys()],
                    columns=['Amount', 'Nutrient content', 'Action']
                )
                st.table(rec_df)
                
                # Display nutrient-specific tips
                if nutrient.startswith('Vitamin'):
                    st.write("💡 Tips:")
                    st.write("- Consider taking supplements after consulting with a healthcare provider")
                    st.write("- Try to incorporate these foods into your daily meals")
                elif nutrient.startswith('Iron'):
                    st.write("💡 Tips:")
                    st.write("- Combine iron-rich foods with vitamin C sources to improve absorption")
                    st.write("- Avoid consuming iron-rich foods with calcium-rich foods")
                elif nutrient.startswith('Calcium'):
                    st.write("💡 Tips:")
                    st.write("- Spread calcium intake throughout the day for better absorption")
                    st.write("- Ensure adequate vitamin D intake for optimal calcium absorption")
            st.write("---")
    else:
        st.success("Your nutrient intake appears to be adequate for all measured parameters!")
