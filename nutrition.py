import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import mysql.connector as db
import emoji

# Establish Mysql Connection
connection = db.connect(
    host = "localhost",
    user = "root",
    password = "root@123",
    db = "nutrition_data"
)

# create a cursor object
cursor = connection.cursor()

st.set_page_config(page_title="Nutrition Paradox", page_icon=emoji.emojize(":pill:"), layout="wide")
st.markdown("<h1 style='color:#1E90FF;'>🥦 Nutrition Paradox</h1>", unsafe_allow_html=True)
st.divider() #adding an horizontal line.

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Nutrition Paradox",  # Menu title
        ["Obesity Query", "Malnutrition Query", "Combination of Two Query"],  # Menu options
        icons=["calendar", "calendar3"],  # Bootstrap icons
        menu_icon="cast",  # Icon for the menu title
        default_index=0
    )

if selected == "Obesity Query":

    option = st.selectbox("Select your query", ['1.Top 5 regions with the highest average obesity levels in the most recent year(2022)',
                                                '2.Top 5 countries with highest obesity estimates',
                                                '3.Obesity trend in India over the years(Mean_estimate)',
                                                '4.Average obesity by gender',
                                                '5.Country count by obesity level category and age group',
                                                '6.Top 5 countries least reliable countries(with highest CI_Width)',
                                                '7.Top 5 most consistent countries (smallest average CI_Width)',
                                                '8.Average obesity by age group',
                                                '9.Top 10 Countries with consistent low obesity (low average + low CI)over the years',
                                                '10.Countries where female obesity exceeds male by large margin (same year)',
                                                '11.Global average obesity percentage per year'])

    if option == '1.Top 5 regions with the highest average obesity levels in the most recent year(2022)':
        cursor.execute("""SELECT
                            Region, 
                            AVG(Mean_Estimate) AS AvgObesity
                        FROM 
                            obesity
                        WHERE 
                            Year = 2022 AND Region IS NOT NULL
                        GROUP BY 
                            Region
                        ORDER BY 
                            AvgObesity DESC
                        LIMIT 5;
                        """)
        
    elif option == '2.Top 5 countries with highest obesity estimates':
        cursor.execute("""SELECT 
                            Country, 
                            MAX(Mean_Estimate) AS PeakObesity
                        FROM 
                            obesity
                        GROUP BY 
                            Country
                        ORDER BY 
                            PeakObesity DESC
                        LIMIT 5;
                        """)
        
    elif option == '3.Obesity trend in India over the years(Mean_estimate)':
        cursor.execute("""SELECT 
                            Year, 
                            AVG(Mean_Estimate) AS ObesityRate
                        FROM 
                            obesity
                        WHERE 
                            Country = 'India'
                        GROUP BY 
                            Year;
                        """)

    elif option == '4.Average obesity by gender':
        cursor.execute("""SELECT
                            Gender, 
                            AVG(Mean_Estimate) AS AvgObesity
                        FROM
                            obesity
                        GROUP BY
                            Gender;
                        """)

    elif option == '5.Country count by obesity level category and age group':
        cursor.execute("""SELECT 
                            Obesity_Level,
                            Age_Group,
                            COUNT(DISTINCT Country) AS CountryCount
                        FROM
                            obesity
                        GROUP BY
                            Obesity_Level, Age_Group;
                        """)
        
    elif option == '6.Top 5 countries least reliable countries(with highest CI_Width)':
        cursor.execute("""SELECT
                            Country, 
                            AVG(CI_Width) AS AvgCI
                        FROM
                            obesity
                        GROUP BY
                            Country
                        ORDER BY
                            AvgCI DESC
                        LIMIT 5;
                        """)
        
    elif option == '7.Top 5 most consistent countries (smallest average CI_Width)':
        cursor.execute("""SELECT
                            Country, 
                            AVG(CI_Width) AS AvgCI
                        FROM
                            obesity
                        GROUP BY
                            Country
                        ORDER BY
                            AvgCI ASC
                        LIMIT 5;
                        """)

    elif option == '8.Average obesity by age group':
        cursor.execute("""SELECT
                            Age_Group,
                            AVG(Mean_Estimate) AS AvgObesity
                        FROM
                            obesity
                        GROUP BY
                            Age_Group;
                        """)

    elif option == '9.Top 10 Countries with consistent low obesity (low average + low CI)over the years':
        cursor.execute("""SELECT
                            Country,
                            AVG(Mean_Estimate) AS AvgObesity,
                            AVG(CI_Width) AS AvgCI
                        FROM
                            obesity
                        GROUP BY
                            Country
                        HAVING
                            AvgObesity < 25 AND AvgCI < 5
                        ORDER BY
                            AvgObesity
                        LIMIT 10;
                        """)

    elif option == '10.Countries where female obesity exceeds male by large margin (same year)':
        cursor.execute("""SELECT
                            o1.Country,
                            o1.Year,
                            o1.Mean_Estimate AS FemaleRate,
                            o2.Mean_Estimate AS MaleRate,
                            (o1.Mean_Estimate - o2.Mean_Estimate) AS Gap
                        FROM
                            obesity o1
                        JOIN
                            obesity o2
                        ON
                            o1.Country = o2.Country AND o1.Year = o2.Year
                        WHERE
                            o1.Gender = 'Female' AND o2.Gender = 'Male' AND (o1.Mean_Estimate - o2.Mean_Estimate) > 10
                        ORDER BY
                            Gap DESC;
                        """)

    elif option == '11.Global average obesity percentage per year':
        cursor.execute("""SELECT
                            Year,
                            AVG(Mean_Estimate) AS GlobalObesity
                        FROM
                            obesity
                        GROUP BY
                            Year;
                        """)
    
elif selected == "Malnutrition Query":

    option = st.selectbox("Select your query", ['1.Average malnutrition by age group',
                                                '2.Top 5 countries with highest malnutrition(mean_estimate)',
                                                '3.Malnutrition trend in African region over the years',
                                                '4.Gender-based average malnutrition',
                                                '5.Malnutrition level-wise (average CI_Width by age group)',
                                                '6.Yearly malnutrition change in specific countries(India, Nigeria, Brazil)',
                                                '7.Regions with lowest malnutrition averages',
                                                '8.Countries with increasing malnutrition',
                                                '9.Min/Max malnutrition levels year-wise comparison',
                                                '10.High CI_Width flags for monitoring(CI_width > 5)'])
    
    if option == '1.Average malnutrition by age group':
        cursor.execute("""SELECT
                            Age_Group,
                            AVG(Mean_Estimate) AS AvgMalnutrition
                        FROM
                            malnutrition
                        GROUP BY
                            Age_Group;
                        """)
    
    elif option == '2.Top 5 countries with highest malnutrition(mean_estimate)':
        cursor.execute("""SELECT
                            Country,
                            MAX(Mean_Estimate) AS MaxMalnutrition
                        FROM
                            malnutrition
                        GROUP BY
                            Country
                        ORDER BY
                            MaxMalnutrition DESC
                        LIMIT 5;
                        """)
    
    elif option == '3.Malnutrition trend in African region over the years':
        cursor.execute("""SELECT
                            Year,
                            AVG(Mean_Estimate) AS RegionalAvg
                        FROM
                            malnutrition
                        WHERE
                            Region = 'Africa'
                        GROUP BY
                            Year;
                        """)
    
    elif option == '4.Gender-based average malnutrition':
        cursor.execute("""SELECT
                            Gender,
                            AVG(Mean_Estimate) AS AvgMalnutrition
                        FROM
                            malnutrition
                        GROUP BY
                            Gender;
                        """)
    
    elif option == '5.Malnutrition level-wise (average CI_Width by age group)':
        cursor.execute("""SELECT
                            Region,
                            Age_Group,
                            AVG(CI_Width) AS AvgCI
                        FROM
                            malnutrition
                        GROUP BY Region, Age_Group;
                        """)
    
    elif option == '6.Yearly malnutrition change in specific countries(India, Nigeria, Brazil)':
        cursor.execute("""SELECT
                            Country,
                            Year,
                            AVG(Mean_Estimate) AS MalnutritionRate
                        FROM
                            malnutrition
                        WHERE
                            Country IN ('India', 'Nigeria', 'Brazil')
                        GROUP BY
                            Country, Year
                        ORDER BY
                            Country, Year;
                        """)
        
    elif option == '7.Regions with lowest malnutrition averages':
        cursor.execute("""SELECT
                            Region,
                            AVG(Mean_Estimate) AS AvgMalnutrition
                        FROM
                            malnutrition
                        GROUP BY
                            Region
                        ORDER BY
                            AvgMalnutrition ASC
                        LIMIT 5;
                        """)
    
    elif option == '8.Countries with increasing malnutrition':
        cursor.execute("""SELECT
                            Country,
                            MAX(Mean_Estimate) - MIN(Mean_Estimate) AS Increased_Malnutrition
                        FROM
                            malnutrition
                        GROUP BY
                            Country
                        HAVING
                            Increased_Malnutrition > 0
                        ORDER BY
                            Increased_Malnutrition DESC;
                        """)
        
    elif option == '9.Min/Max malnutrition levels year-wise comparison':
        cursor.execute("""SELECT
                            Year,
                            MIN(Mean_Estimate) AS MinMalnutrition,
                            MAX(Mean_Estimate) AS MaxMalnutrition
                        FROM
                            malnutrition
                        GROUP BY
                            Year;
                        """)
        
    elif option == '10.High CI_Width flags for monitoring(CI_width > 5)':
        cursor.execute("""SELECT
                            Country,
                            Year,
                            CI_Width
                        FROM
                            malnutrition
                        WHERE
                            CI_Width > 5
                        ORDER BY
                            CI_Width DESC;
                        """)
    
elif selected == "Combination of Two Query":

    option = st.selectbox("Select your query", ['1.Obesity vs malnutrition comparison by country(any 5 countries)',
                                                '2.Gender-based disparity in both obesity and malnutrition',
                                                '3.Region-wise avg estimates side-by-side(Africa and America)',
                                                '4.Age-wise trend analysis'])

    if option == '1.Obesity vs malnutrition comparison by country(any 5 countries)':
        cursor.execute("""SELECT
                            o.Country,
                            o.Year,
                            o.Mean_Estimate AS ObesityRate,
                            m.Mean_Estimate AS MalnutritionRate
                        FROM
                            obesity o
                        JOIN malnutrition m
                        ON
                            o.Country = m.Country AND o.Year = m.Year
                        WHERE
                            o.Country IN ('India', 'USA', 'Brazil', 'Nigeria', 'Indonesia');
                        """)
        
    elif option == '2.Gender-based disparity in both obesity and malnutrition':
        cursor.execute("""SELECT
                            o.Gender,
                            AVG(o.Mean_Estimate) AS AvgObesity,
                            AVG(m.Mean_Estimate) AS AvgMalnutrition
                        FROM
                            obesity o
                        JOIN malnutrition m
                        ON
                            o.Country = m.Country AND o.Year = m.Year AND o.Gender = m.Gender
                        GROUP BY
                            o.Gender;
                        """)
        
    elif option == '3.Region-wise avg estimates side-by-side(Africa and America)':
        cursor.execute("""SELECT
                            o.Region,
                            AVG(o.Mean_Estimate) AS ObesityAvg,
                            AVG(m.Mean_Estimate) AS MalnutritionAvg
                        FROM
                            obesity o
                        JOIN
                            malnutrition m
                        ON
                            o.Country = m.Country AND o.Year = m.Year
                        WHERE
                            o.Region IN ('Africa', 'Americas Region')
                        GROUP BY
                            o.Region;
                        """)
    
    elif option == '4.Age-wise trend analysis':
        cursor.execute("""SELECT
                            o.Year,
                            o.Age_Group,
                            AVG(o.Mean_Estimate) AS ObesityAvg,
                            AVG(m.Mean_Estimate) AS MalnutritionAvg
                        FROM
                            obesity o
                        JOIN
                            malnutrition m
                        ON
                            o.Country = m.Country AND o.Year = m.Year AND o.Age_Group = m.Age_Group
                        GROUP BY
                            o.Year, o.Age_Group
                        ORDER BY
                            o.Year;
                        """)
        
result = cursor.fetchall()

# Dynamically get column names
columns = [desc[0] for desc in cursor.description]

# Create dataframe with dynamic columns
df = pd.DataFrame(result, columns=columns)

# Display in streamlit
st.dataframe(df)