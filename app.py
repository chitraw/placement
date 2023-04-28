import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Survey Placement')
st.header('Survey Results ')
st.subheader('Prediction')

### --- LOAD DATAFRAME
excel_file = "placement.xlsx"
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='A:I',
                   header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='E:G',
                                header=3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
department = df['Companies'].unique().tolist()
Salary = df['Salary'].unique().tolist()

age_selection = st.slider('Salary:',
                        min_value= min(Salary),
                        max_value= max(Salary),
                        value=(min(Salary),max(Salary)))

department_selection = st.multiselect('Companies:',
                                    department,
                                    default=department)




# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Salary'].between(*age_selection)) & (df['Companies'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

Name = df['NAME'].unique().tolist()
Skills = df['Skills'].unique().tolist()
department_selection = st.multiselect('Skills:',
                                Skills,
                                    )
# selected_skill = input('Enter the selected skill: ')


# filtered_df = df[df['Skills'] == selected_skill]
# for index, row in filtered_df.iterrows():
#     print(row['NAME'])

# Display the names of people who have the selected skill

# filtered_df = df[df["Skills"] == department_selection]
# for index, row in filtered_df.iterrows():
#     print(row['NAME'])

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Role']).count()[['Placed']]
df_grouped = df_grouped.rename(columns={'Placed': 'Companies'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Role',
                   y='Companies',
                   text='Companies',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('images/survey.jpg')
col1.image(image,
        caption='Designed by slidesgo / Freepik',
        use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Total No. of Participants',
                values='Participants',
                names='Companiess')

st.plotly_chart(pie_chart)
