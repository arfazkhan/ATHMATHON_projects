import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from the USERDATA worksheet
data = conn.read(worksheet="USERDATA")

# Display the original data
sql=''' select 
              "TOKEN_NO",
              "CURR_DATE",
              "PATIENT_NAME",
              "CURR_CONDITION",
              "AI_RESPONSE",
              "STATUS"
               "Remarks" from USERDATA where "TOKEN_NO" not null and "CURR_DATE"= CURRENT_DATE
    '''

df_user_data= conn.query(sql=sql)
st.dataframe(df_user_data)

# Get user input for selecting a user
selected_user = st.selectbox("Select user:", data["PATIENT_NAME"])

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
        # Create a new DataFrame with the new data
        new_data = pd.DataFrame({
            "TOKEN_NO": [None],
            "CURR_DATE": [pd.to_datetime("today").date()],
            "PATIENT_NAME": [selected_user],
            "CURR_CONDITION": [None],
            "AI_RESPONSE": [None],
            "STATUS": [new_status],
            "Remarks": [new_remarks]
        })

        # Append the new data to the original data
        updated_data = pd.concat([data, new_data], ignore_index=True)

        # Write the updated data back to Google Sheets
        conn.session.write(updated_data, worksheet="USERDATA")

        # Display updated data
        st.success("Data inserted successfully!")
        st.write("Updated Data:")
        st.dataframe(updated_data)
