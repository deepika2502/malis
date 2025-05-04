import streamlit as st
from streamlit_image_select import image_select

# Add a placeholder image as the first option
images = ["placeholder.jpg", "img1.jpg", "img2.jpg", "img3.jpg"]

selected = image_select("Select the correct image:", images)

if selected == "placeholder.jpg":
    st.write("No image selected yet.")
else:
    st.write("You selected:", selected)

col1, col4 = st.columns([7, 1])
with col1:
    st.button('Refresh')
with col4:
    st.button('Check')
