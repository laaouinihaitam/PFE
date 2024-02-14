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
  def run_tests(file1, test_file1):
    # Run pytest with coverage options separately
    coverage_command = f'coverage run -m pytest {test_file1}'
    coverage_process = subprocess.Popen(coverage_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout_output, stderr_output = coverage_process.communicate()

    # Generate coverage report
    subprocess.run(['coverage', 'html'])

    # Print captured output for debugging
    print("pytest output:", stdout_output)
    print("pytest error:", stderr_output)

    # Check if tests ran successfully
    if coverage_process.returncode == 0:
        st.success("Tests ran successfully!")
        # Get coverage report directory
        cov_dir = os.path.join(os.getcwd(), 'htmlcov')
        st.write(f"Coverage report generated at: {cov_dir}")
        # Provide a download link for the coverage report
        st.markdown(f"## [Download Coverage Report]({cov_dir}/index.html)")
    else:
        st.error("Tests failed. Please check your files and try again.")
        cov_dir = os.path.join(os.getcwd(), 'htmlcov')
        st.write(f"Coverage report generated at: {cov_dir}")
        # Provide a download link for the coverage report
        st.markdown(f"## [Download Coverage Report]({cov_dir}/index.html)")

  def main():
    st.title("Python File Testing with Pytest and Coverage")

    st.write("Upload your Python files:")
    uploaded_files = st.file_uploader("Upload file1.py", type="py", key="file1")
    test_uploaded_files = st.file_uploader("Upload test_file1.py", type="py", key="test_file1")

    if st.button("Run Tests"):
        if uploaded_files is not None and test_uploaded_files is not None:
            # Save the uploaded files to the current directory
            with open("file1.py", "wb") as f1, open("test_file1.py", "wb") as tf1:
                f1.write(uploaded_files.read())
                tf1.write(test_uploaded_files.read())
            
            run_tests("file1.py", "test_file1.py")
        else:
            st.error("Please upload both files before running tests.")

  if __name__ == "__main__":
    main()



image_url = "https://formation-cfr.fr/wp-content/uploads/2016/04/logo-safran.png"

# Center the image horizontally with equal margins and add a caption
st.write("<style>.stImage {white-space: nowrap;}</style>", unsafe_allow_html=True)
st.image(image_url, width=100, use_column_width=False, caption='© 2024 SES Rabat-Morocco', clamp=False, channels='RGB', output_format='auto')