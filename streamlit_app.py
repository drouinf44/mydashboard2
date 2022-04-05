import streamlit as st
from streamlit_autorefresh import st_autorefresh

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt
import platform

# update every 1 min
st_autorefresh(interval=1 * 60 * 1000, key="dataframerefresh")

st.title("Hello on streamlit 1")

if(platform.processor() == ""):
    cloudExecution = True
else:
    cloudExecution = False

#################### Google Sheet Credentials Logic ##################################

# Récupérer des credentials
if(cloudExecution):
    # pour streamlit cloud : récupération depuis les secrets
    scope = [   'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
    )
else:
    # en local : récupération depuis le fichier client_secret.json
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\px9\PycharmProjects\Alimentor\client_secret.json', scope)

# use creds to create a client to interact with the Google Drive API
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("SAP_PERF").sheet1

# Extract and print all of the values
# df = pd.DataFrame(sheet.get_all_records())
# sm12_fig = plt.figure(figsize=(6,4))
# sm12_ax = sm12_fig.add_subplot(111)
# df.plot.bar(alpha=0.5, ax=sm12_ax, title="SM12");

# Récupérer le numéro de la première ligne vide et la valeur de la dernière date renseignée
last_row = len(list(filter(None, sheet.col_values(1))))
sm12_int = int(sheet.cell(last_row, 2).value)
sm12_str = str(sheet.cell(last_row, 2).value)

##################### Layout Application ##################
if sm12_int < 500:
    st.success("SM12 : " + sm12_str)
elif sm12_int <5000:
    st.warning("SM12 : " + sm12_str)
else:
    st.error("SM12 : " + sm12_str)

# container1 = st.container()
# col1, col2, col3, col4, col5  = st.columns(5)
#
# with container1:
#     with col1:
#         st.markdown("<h6 style='text-align: center; vertical-align: middle; color: black;'>BOM SAP/ouvrage</h6>", unsafe_allow_html=True)
#     with col2:
#         st.warning("L34")
#     with col3:
#         st.error("W34")
#     with col4:
#         st.success("T34")
#     with col5:
#         st.success("T34")

# with st.expander("Details BOM/étape..."):
#     sm12_fig