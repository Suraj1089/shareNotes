import streamlit as st
import base64
from annotated_text import annotated_text
import requests
import os

BASE_URL = st.secrets['BASE_URL']

# BASE_URL = 'http://localhost:8000'
def displayPDF(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

    
def App():

    st.markdown("""
        Resume Analyser
        ---------------
        """)
    with st.sidebar:
        st.markdown("""
            ## Result Analyser

            <a href="https://github.com/Suraj1089/shareNotes/network/members"><img src="https://img.shields.io/github/forks/Suraj1089/shareNotes" alt="Forks Badge"/></a>
            <a href="https://github.com/Suraj1089/shareNotes/pulls"><img src="https://img.shields.io/github/issues-pr/Suraj1089/shareNotes" alt="Pull Requests Badge"/></a>
            <a href="https://github.com/Suraj1089/shareNotes/issues"><img src="https://img.shields.io/github/issues/Suraj1089/shareNotes" alt="Issues Badge"/></a>
            <a href="https://github.com/Suraj1089/shareNotes/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/Suraj1089/shareNotes?color=2b9348"></a>
            [![GitHub license](https://img.shields.io/github/license/Suraj1089/shareNotes?color=orange)](https://github.com/Suraj1089/shareNotes/blob/dev/LICENSE)
            [![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Suraj1089/shareNotes)](https://github.com/Suraj1089/shareNotes/graphs/commit-activity)
            [![GitHub issues](https://img.shields.io/github/issues/Suraj1089/shareNotes?color=blue)](https://github.com/Suraj1089/shareNotes/issues)
            [![GitHub stars](https://img.shields.io/github/stars/Suraj1089/shareNotes)](https://github.com/Suraj1089/shareNotes/stargazers)

        """, unsafe_allow_html=True)

                            
    pdf_file = st.file_uploader(label="Upload Pdf File", type="pdf")
    if pdf_file:
        with st.spinner("Uploading ..."):
            response = requests.post(
                url=f'{BASE_URL}/upload',
                files={'file': pdf_file},
            )

        
        if response.status_code == 201:
            st.success("File Uploaded Successfully")
            Analyse = st.button("Analyse")
            import time
            if Analyse:
                path = response.json()['path']
                data = requests.post(
                    url=f'{BASE_URL}/analyse?path={path}',
                )

                # data = requests.post()
                my_bar = st.progress(0, text='Analyzing...')

                for percent_complete in range(0,100):
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1, text='Analyzing...')
                my_bar.empty()
                st.success("Analysis Completed")

                if data.status_code == 200:
                    st.write(data.json())
    
        else:
            st.error("Error in uploading file")

                
if __name__ == "__main__":
    
    # set page title and icon
    try:
        st.set_page_config(
            page_title='Resume Analysis',
            page_icon='📃',
        )
        with st.sidebar:
            st.header('Our Contributors')

            import streamlit as st

            st.markdown(
                """
                <style>
                    /* Add CSS styles here */
                    .avatar-container {
                        display: inline-block;
                        margin-right: 20px; /* Adjust the margin to your desired spacing */
                    }
                </style>

                <div class="avatar-container">
                    <a href="https://github.com/Suraj1089/shareNotes/graphs/contributors">
                        <img src="https://contrib.rocks/image?max=50&repo=Suraj1089/shareNotes" />
                    </a>
                </div>

        
                """,
                unsafe_allow_html=True
            )


    except Exception as e:
        pass

    App()