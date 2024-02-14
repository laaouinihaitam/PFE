import streamlit as st
import os
import subprocess
import io
import sys

import pandas as pd 
import plotly.express as px 
import base64  
from io import StringIO, BytesIO  
import pickle
from pathlib import Path 
import streamlit_authenticator as stauth
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import os
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime
from reportlab.platypus import Table, TableStyle

from reportlab.lib.colors import red




st.set_page_config(page_title='Safran APP',page_icon="✈️")
#---user authentification---
image_url = "https://formation-cfr.fr/wp-content/uploads/2016/04/logo-safran.png"
st.write("<style>div.Widget.row-widget.stHorizontal {flex-direction: row-reverse;}</style>", unsafe_allow_html=True)
st.image(image_url, width=1000, use_column_width=False, caption='', clamp=False, channels='RGB', output_format='auto')
names=["Mohammed Rahmouni","Mourad Bouchnaf","Haitam Laaouini"]
usernames =["rahmouni","bouchnaf","laaouini"]

# load hashed passwords
file_path = Path("C:/Users/LOGION/Desktop/haiiitam/hashed_pw.pkl")
with file_path.open("rb") as file :
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"excel_plotter","abcdef",0)

name,authentification_status,username =authenticator.login("Login","main")
if authentification_status==False:
    st.error("Username/password is incorrect")
if authentification_status==None:
    st.warning("Please enter your username and password")
if authentification_status:
  authenticator.logout("Logout","sidebar")
  st.sidebar.title(f"Welcome {name}")
  st.sidebar.success("Select a page above")
  def scrape_and_convert_to_excel(html_file, output_excel):
    # Read the HTML content from the UploadedFile object
    html_content = html_file.getvalue().decode('utf-8')
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the first table in the HTML
    first_table = soup.find('table')

    if first_table:
        # Extract data from the table
        rows = []
        for row in first_table.find_all('tr'):
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            rows.append(row_data)

        # Convert data to a pandas DataFrame
        df = pd.DataFrame(rows)

        # Write data to Excel file
        df.to_excel(output_excel, index=False, header=False)

        st.success(f'Successfully scraped and saved the first table from uploaded HTML file to {output_excel}')
    else:
        st.warning('No table found in the uploaded HTML file.')


  def adjust_column_widths(excel_file):
    # Load the Excel workbook
    workbook = openpyxl.load_workbook(excel_file)

    # Select the first (and only) sheet in the workbook
    sheet = workbook.active

    # Iterate through all columns and adjust width based on the maximum content length
    for column in sheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                cell_value = str(cell.value) if cell.value is not None else ''
                if len(cell_value) > max_length:
                    max_length = len(cell_value)
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[openpyxl.utils.get_column_letter(cell.column)].width = adjusted_width

    # Save the modified workbook
    workbook.save(excel_file)
    st.info(f'Column widths adjusted for {excel_file}')

# Function to show file description
  def show_file_description(excel_file):
    # Load the Excel file
    df = pd.read_excel(excel_file)

    # Display file description
    st.subheader("Excel File Description")
    st.markdown(f"**Number of Rows:** {df.shape[0]}")
    st.markdown(f"**Number of Columns:** {df.shape[1]}")
    st.write("")

    st.subheader("Sample Data")
    st.write(df.head(5))  # Display first 5 rows as sample data

    return df

# Function to plot data
  def plot_data(df):
    st.subheader("Data Visualization")

    # Countplot for the first column
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x="Assesslet Name", hue="Failed", ax=ax)
    ax.set_title("Failed test cases")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)


    # Count the number of Assesslet Name entries where Failed equals 1
    num_failed_1 = df[df['Failed'] == 1]['Assesslet Name'].nunique()

    # Calculate coverage as a percentage
    coverage_percentage = (1 - (num_failed_1 / 13)) * 100
    st.write(f"Coverage: {coverage_percentage:.2f}%")

    # Plot coverage in a pie chart
    labels = ['Coverage', 'Remaining']
    sizes = [coverage_percentage, 100 - coverage_percentage]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)  # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    plt.title('Coverage')
    st.pyplot(plt)

# Function to generate PDF report
  def generate_pdf_report(df, coverage_percentage):
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    # Create a PDF document
    pdf_file_name = f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    pdf = SimpleDocTemplate(pdf_file_name, pagesize=letter)
    elements = []

    # Add table to PDF
    table_data = [df.columns.tolist()] + df.values.tolist()
    table = Table(table_data)
    style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), 'blue'),  # Header background color
    ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Header text color
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
    ('GRID', (0, 0), (-1, -1), 1, 'BLACK'),  # Add grid lines to all cells
    ])
    


    table.setStyle(style)
    elements.append(table)

    # Add spacing
    elements.append(Spacer(1, 12))

    # Add review paragraph
    styles = getSampleStyleSheet()
    review_paragraph = f"Review: The table above displays the data extracted from the uploaded HTML file. " \
                       f"The count plot shows the distribution of failed test cases among the assesslet names. " \
                       f"The pie chart illustrates the coverage percentage based on the failed test cases. " \
                       f"The coverage percentage is <font color='red'>{coverage_percentage:.2f}%</font>."
    review = Paragraph(review_paragraph, styles["Normal"])
    elements.append(review)

    # Add date and time of download
    download_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    download_text = f"Downloaded on: {download_datetime}"
    download = Paragraph(download_text, styles["Normal"])
    elements.append(download)

    # Build PDF document
    pdf.build(elements)

    return pdf_file_name

# Streamlit UI
  st.title("HTML to Excel Converter")

  html_file = st.file_uploader("Upload HTML file", type=['html'])

  if html_file is not None:
    if st.button("Convert to Excel and Generate Report"):
        with st.spinner("Converting..."):
            excel_file_name = f"{html_file.name.split('.')[0]}.xlsx"
            scrape_and_convert_to_excel(html_file, excel_file_name)
            adjust_column_widths(excel_file_name)
            st.write("Conversion completed.")

        # Show file description
        df = show_file_description(excel_file_name)

        # Plot data
        plot_data(df)

        # Generate PDF report
        num_failed_1 = df[df['Failed'] == 1]['Assesslet Name'].nunique()
        coverage_percentage = (1 - (num_failed_1 / 13)) * 100
        pdf_file_name = generate_pdf_report(df, coverage_percentage)

        # Add a download button for the generated PDF report
        st.download_button(
            label="Download PDF Report",
            data=open(pdf_file_name, 'rb').read(),
            file_name=pdf_file_name,
            mime='application/pdf'
        )


image_url = "https://formation-cfr.fr/wp-content/uploads/2016/04/logo-safran.png"

# Center the image horizontally with equal margins and add a caption
st.write("<style>.stImage {white-space: nowrap;}</style>", unsafe_allow_html=True)
st.image(image_url, width=100, use_column_width=False, caption='© 2024 SES Rabat-Morocco', clamp=False, channels='RGB', output_format='auto')