import streamlit as st
import requests
import os

FLASK_URL = os.getenv("FLASK_URL", "https://journal-mx-1.onrender.com")

def get_entries():
    response = requests.get(f"{FLASK_URL}/entries")
    return response.json() if response.status_code == 200 else []

st.title('📖 My Journal App')
st.write('Write, View and Manage your journal entries.')

# Display Entries
entries = get_entries()
for entry in entries:
    st.subheader(entry['title'])
    st.write(entry['content'])
    st.caption(f'🕒 Created on {entry["date"]}')

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🗑️ Delete", key=f"del-{entry['id']}"):
            response = requests.delete(f"{FLASK_URL}/delete/{entry['id']}")
            if response.status_code == 200:
                st.success("Entry deleted successfully!")
                st.rerun()
            else:
                st.error("Failed to delete entry.")

    st.markdown("---")

# Create Entry
st.subheader("➕ Add New Entry")
title = st.text_input('Title')
content = st.text_area('Content')

if st.button('📌 Add Entry'):
    if title and content:
        response = requests.post(f"{FLASK_URL}/create", json={"title": title, "content": content})
        if response.status_code == 201:
            st.success("Entry added successfully!")
            st.experimental_rerun()
        else:
            st.error("Failed to add entry.")
    else:
        st.error("Title and content are required.")

# Update Entry
st.subheader("✏️ Edit Journal Entry")
entry_id = st.number_input("Entry ID to Edit", min_value=1, step=1)
new_title = st.text_input("New Title")
new_content = st.text_area("New Content")

if st.button("✅ Update Entry"):
    if new_title and new_content:
        response = requests.put(f"{FLASK_URL}/update/{entry_id}", json={"title": new_title, "content": new_content})
        if response.status_code == 200:
            st.success("Entry updated successfully!")
            st.experimental_rerun()
        else:
            st.error("Failed to update entry.")
    else:
        st.error("New title and content are required.")
