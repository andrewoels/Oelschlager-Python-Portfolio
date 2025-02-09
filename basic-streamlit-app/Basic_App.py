import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv("Data/penguins.csv")

# Streamlit app title and description
st.title("Penguin Data Explorer")
st.write("This app allows users to explore the Palmer Penguins dataset with interactive filters.")

# Sidebar filters
species_options = df['species'].unique()
selected_species = st.sidebar.multiselect("Select Species:", species_options, default=species_options)

island_options = df['island'].unique()
selected_island = st.sidebar.multiselect("Select Island:", island_options, default=island_options)

body_mass_min, body_mass_max = int(df['body_mass_g'].min()), int(df['body_mass_g'].max())
selected_body_mass = st.sidebar.slider("Select Body Mass Range:", body_mass_min, body_mass_max, (body_mass_min, body_mass_max))

# Apply filters
filtered_df = df[(df['species'].isin(selected_species)) &
                 (df['island'].isin(selected_island)) &
                 (df['body_mass_g'].between(selected_body_mass[0], selected_body_mass[1]))]

# Display filtered data
st.write("### Filtered Penguin Data")
st.dataframe(filtered_df)

# Instructions on how to run the app


# How to Run the Streamlit App
#1. Ensure you have Python installed
#2. Install Streamlit if you haven't already by running:
#3. Navigate to the directory containing this script in the terminal or command prompt.
#4. Run the Streamlit app using the following command: streamlit run Basic_App.py
#5. The app should open in your web browser automatically.
