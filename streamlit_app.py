from database import Database
import streamlit as st
import requests
from app import fetch_entries, create_entry, delete_entry


FLASK_URL = "https://journal-mx-1.onrender.com"


def get_entries():
    response = requests.get(f'{FLASK_URL}/entries')
    return response.json() if response.status_code == 200 else []



st.title('My Journal app')
st.write('Write, View and Delete your journal entries.')

# Show all Entries
entries = get_entries()
for entry in entries:
    st.subheader(entry['title'])
    st.write(entry['content'])
    st.caption(f'Created on {entry['date']}')
    if st.button(f"🗑️  Delete", key=entry["id"]):
        response = requests.delete(f"{FLASK_URL}/delete/{entry['id']}")
        if response.status_code == 200:
            st.success("Entry deleted successfully!")


    st.write('---')

    # st.success('Streamlit frontend working properly')

# Create new entry
st.subheader('Add new entry')
title = st.text_input('Title')
content = st.text_area('Content')

if st.button('Add ENTRY'):
    if title and content:
        new_entry={'title': title, 'content': content}
        response = requests.post(f'{FLASK_URL}/create', json=new_entry)
        if response.status_code == 200:
            st.success('ENTRY added succesfully')
    else:
        st.error('both Title and Content are required...')


st.header("Edit Journal Entry")
entry_id = st.number_input("Entry ID to Edit", min_value=1, step=1)
title = st.text_input("New Title")
content = st.text_area("New Content")

if st.button("Update Entry"):
    update_data = {"title": title, "content": content}
    response = requests.put(f"{FLASK_URL}/update/{entry_id}", json=update_data)
    
    if response.status_code == 200:
        st.success("Entry updated successfully!")
        # st.experimental_rerun()
    else:
        st.error("Failed to update entry.")




