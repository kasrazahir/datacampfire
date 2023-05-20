import streamlit as st
import requests
from bs4 import BeautifulSoup

# Initialize Google Drive API
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

st.config.set_option('theme', 'light')
# Define a list of files to display
file_list = [
    {
        "id": "1fJnsQVmHCeHI-gQysseb7ZdJroLe3g2SnzUHFE-c7NM",
        "title": "Statistical Analysis",
        "type": "document"
    },
    {
        "id": "1FcO2icLoNHoWy9rNrLXXqvOjlTG4uX_xmDSA-YVLYKM",
        "title": "Machine Learning",
        "type": "document"
    },
    {
        "id": "17ia_mo9YIzfZA73n7MD77lfY7db2w_Hjy_d9ZpqEUyA",
        "title": "Pattern Recognition",
        "type": "document"
    },
    {
        "id": "1DHoGJxjhkLpSSn7kvCoKyRb16wLX9xeB45E8TXhmR6s",
        "title": "Time Series & Forecasting",
        "type": "document"
    }
]

# Function to get the HTML content of the Google Doc
def get_google_doc_html(file_id):
    url = f"https://docs.google.com/document/d/{file_id}/export?format=html"
    response = requests.get(url)
    return response.text

# Define the welcome message
welcome_message = """
# Welcome

On this site you will find a collection of my notes and insights gathered throughout my journey of learning  
data science and machine learning. This field has been a passion of mine for years and I am committed to continuously updating and expanding these notes.

Feel free to explore the **topics listed on the left-hand side** of the page. Each section is dedicated to a specific aspect of the data science craft.

I hope that this website becomes a valuable resource on your  data science journey. If you have any 
questions or feedback, please don't hesitate to reach out. 

Wishing you a fulfilling and rewarding learning adventure!
"""

# Retrieve or initialize the button states from the session state
button_states = st.session_state.setdefault("button_states", {})

# Display the button list in the sidebar
selected_page = None

for file in file_list:
    if button_states.get(file["title"], False):
        button_clicked = st.sidebar.button(file["title"], key=file["title"])
    else:
        button_clicked = st.sidebar.button(file["title"], key=file["title"])
    if button_clicked:
        selected_page = file
        button_states[file["title"]] = True
    else:
        button_states[file["title"]] = False

# Apply CSS styling to the buttons to set equal width
button_style = """
.stButton>button {
    background-color: transparent;
    border: none;
    cursor: pointer;
}

.stButton>button:hover {
    background-color: transparent;
}
"""
st.sidebar.markdown(
    """
    <style>
    {}
    </style>
    """.format(button_style),
    unsafe_allow_html=True
)

# Function to process images within the HTML content
def process_images(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    images = soup.find_all("img")
    for image in images:
        image_url = image["src"]
        # st.image(image_url, use_column_width=True)
    return str(soup)

# Display the selected file content or the welcome message
if selected_page is None:
    st.markdown(welcome_message)
else:
    content = get_google_doc_html(selected_page["id"])
    processed_content = process_images(content)
    st.markdown(processed_content, unsafe_allow_html=True)
