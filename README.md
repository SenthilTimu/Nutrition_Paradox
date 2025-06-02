🥦 Nutrition Paradox Dashboard

A Streamlit-based interactive data analysis tool to explore global trends in obesity and malnutrition using SQL queries. This dashboard helps visualize health disparities, compare metrics across countries, and analyze gender- and age-based differences.

🌐 Features
  📊 Obesity Queries:
  
  Top 5 regions/countries with highest obesity rates
  
  Gender and age group breakdowns
  
  Country-wise and global obesity trends
  
  Consistency and reliability checks using confidence intervals (CI)
  
  🍽️ Malnutrition Queries:
  
  Top 5 countries by malnutrition
  
  Region and gender comparisons
  
  Time-series analysis by country and age group
  
  High CI width alert flags for monitoring
  
  🔀 Combined Queries:
  
  Obesity vs malnutrition comparisons
  
  Gender and region-wise disparities
  
  Age-wise trends over time

🧰 Tech Stack
  Frontend: Streamlit
  
  Backend: Python + MySQL
  
  UI Enhancements: streamlit_option_menu, emoji
  
  Database: MySQL with two tables: obesity and malnutrition

🏗️ Setup Instructions
1. Clone this repository: git clone https://github.com/SenthilTimu/Nutrition_Paradox
2. cd nutrition-paradox-dashboard

📌 Requirements
* Python 3.7+

MySQL Server

Required Python libraries:

streamlit

pandas

streamlit-option-menu

mysql-connector-python

emoji
