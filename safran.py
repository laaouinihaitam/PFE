import streamlit as st
import pandas as pd 
import plotly.express as px 
import base64  
from io import StringIO, BytesIO  
import pickle
from pathlib import Path 
import streamlit_authenticator as stauth



def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Tpt_report.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title='Safran APP',page_icon="✈️")
#---user authentification---
image_url = "https://formation-cfr.fr/wp-content/uploads/2016/04/logo-safran.png"
st.write("<style>div.Widget.row-widget.stHorizontal {flex-direction: row-reverse;}</style>", unsafe_allow_html=True)
st.image(image_url, width=1000, use_column_width=False, caption='', clamp=False, channels='RGB', output_format='auto')
#---user authentification---
names=["Mohammed Rahmouni","Mourad Bouchnaf", "Haitam Laaouini"]
usernames =["rahmouni","bouchnaf","laaouini"]

# load hashed passwords
file_path = Path(__file__).parent /"hashed_pw.pkl"
with file_path.open("rb") as file :
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"excel_plotter","abcdef",0)

name,authentification_status,username =authenticator.login("Login","main")
if authentification_status==False:
    st.error("Username/password is incorrect")
if authentification_status==None:
    st.warning("Please enter your username and password")
if authentification_status:
    st.title('Excel Plotter ')
    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.success("Select a page above")
    st.subheader('Feed me with your Excel file !🧟‍♂️')
    uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
    if uploaded_file:
       st.markdown('---')
       df = pd.read_excel(uploaded_file, engine='openpyxl')
       st.dataframe(df)
       groupby_column = st.selectbox(
        'What would you like to analyse?',
        ('Test ID', 'Test Date', 'Tester Name', 'Module_RQ','Team','State'),
        )
       output_columns = ['Coverage', 'Taux']
       df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

       fig1 = px.bar(
         df_grouped,
         x=groupby_column,
         y='Coverage',
         color='Taux',
         color_continuous_scale=['red', 'yellow', 'green'],
         template='plotly_white',
         title=f'Coverage & Taux by {groupby_column}'
        )
       
         


       fig = px.scatter(
          df_grouped,
          x=groupby_column,
          y='Coverage',
          color='Taux',
          color_continuous_scale=['red', 'yellow', 'green'],
          template='plotly_white',
          title=f'<b>Sales & Taux by {groupby_column}</b>'
        )
       
       fig2 = px.line(
        df_grouped,
        x=groupby_column,
        y='Coverage',
        color='Taux',
        line_shape='hv',  # 'hv' to create filled areas
        template='plotly_white',
        title=f'Coverage & Taux by {groupby_column}'
       )

# Manually set colors for each line segment based on the 'Profit' values
       for i, trace in enumerate(fig.data):
        if i > 0:  # Skip the first trace (i.e., the x-axis)
          trace.fill = 'tozeroy'  # Fill to the x-axis
          trace.line.color = fig.data[i-1].line.color  # Use the previous trace's color






       st.plotly_chart(fig)
       st.plotly_chart(fig1)
       st.plotly_chart(fig2)

       st.subheader('Downloads:')
       generate_excel_download_link(df_grouped)
       generate_html_download_link(fig)
       generate_html_download_link(fig1)
       generate_html_download_link(fig2)
image_url = "https://formation-cfr.fr/wp-content/uploads/2016/04/logo-safran.png"

# Center the image horizontally with equal margins and add a caption
st.write("<style>.stImage {white-space: nowrap;}</style>", unsafe_allow_html=True)
st.image(image_url, width=100, use_column_width=False, caption='© 2024 SES Rabat-Morocco', clamp=False, channels='RGB', output_format='auto')

