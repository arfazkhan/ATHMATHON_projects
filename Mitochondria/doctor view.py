import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from the USERDATA worksheet
data = conn.read(worksheet="USERDATA")
data_filtered = data.dropna(subset=["PATIENT_NAME"])

# Display the original data
sql = '''
    SELECT
        "TOKEN_NO",
        "CURR_DATE",
        "PATIENT_NAME",
        "CURR_CONDITION",
        "AI_RESPONSE",
        "STATUS",
        "Remarks"
    FROM USERDATA
    WHERE "TOKEN_NO" IS NOT NULL
    AND "CURR_DATE" = CURRENT_DATE
'''
df_user_data = conn.query(sql=sql)
st.dataframe(df_user_data)



# Get user input for selecting a user
selected_user = st.selectbox("Select user:", data_filtered["PATIENT_NAME"])

# Get user input for new status
status_options = ["Cancel", "Add"]  # Add more options as needed
new_status = st.selectbox("Select new status:", status_options)

# Get user input for new remarks
new_remarks = st.text_area("Enter new remarks (optional):")

# Button to trigger the insertion
if st.button("Insert"):
    if not new_status:
        st.warning("Please select a status.")
    else:
        # Update the DataFrame locally
        data.loc[data["PATIENT_NAME"] == selected_user, "STATUS"] = new_status
        data.loc[data["PATIENT_NAME"] == selected_user, "Remarks"] = new_remarks

        # Write the updated data back to Google Sheets
        conn.write(data, worksheet="USERDATA")

        # Display success message
        st.success("Data inserted successfully!")

        # Display updated data
        st.write("Updated Data:")
        st.dataframe(data)

