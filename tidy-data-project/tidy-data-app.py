#%%
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("data/olympics_08_medalists.csv")

# Convert wide data format to tidy format
melted_df = pd.melt(df, id_vars = ["medalist_name"],
                    value_vars = ["male_archery","female_archery","male_athletics","female_athletics","male_badminton","female_badminton","male_baseball","male_basketball","female_basketball","male_boxing","male_canoeing and kayaking","female_canoeing and kayaking","male_road bicycle racing","female_road bicycle racing","male_track cycling","female_track cycling","male_mountain biking","female_mountain biking","male_bmx","female_bmx","male_diving","female_diving","female_equestrian sport","male_equestrian sport","male_fencing","female_fencing","male_field hockey","female_field hockey","male_association football","female_association football","male_artistic gymnastics","female_artistic gymnastics","female_rhythmic gymnastics","male_trampoline gymnastics","female_trampoline gymnastics","male_handball","female_handball","male_judo","female_judo","male_modern pentathlon","female_modern pentathlon","male_rowing","female_rowing","male_sailing","female_sailing","male_shooting sport","female_shooting sport","female_softball","male_swimming","female_swimming","female_synchronized swimming","male_table tennis","female_table tennis","male_taekwondo","female_taekwondo","male_tennis","female_tennis","male_triathlon","female_triathlon","male_beach volleyball","female_beach volleyball","male_volleyball","female_volleyball","male_water polo","female_water polo","male_weightlifting","female_weightlifting","male_freestyle wrestling","female_freestyle wrestling","male_greco-roman wrestling"],
                    var_name = "Event",
                    value_name = "Medal Type")

#Drop unnecessary rows
melted_df = melted_df.dropna().reset_index(drop=True)

# Format event names
melted_df["Event"] = melted_df["Event"].str.replace("_", " ").str.title()

# Rename columns
melted_df.rename(columns={"medalist_name": "Medalist Name"}, inplace=True)

# Capitalize medal types
melted_df["Medal Type"] = melted_df["Medal Type"].str.title()

# Streamlit App
st.title("Olympic Medalists Data")
st.markdown("""
This interactive dashboard allows users to explore and filter Olympic medalist data from the 2008 games. 
Use the provided filters to narrow down medalists by name, event, or medal type.
""")

# Sidebar Navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("[Medal Summary](#olympic-medalists-data)")
st.sidebar.markdown("[Visualizations](#total-medals-by-event)")


# Filtering options
col1, col2, col3 = st.columns(3)
with col1:
    medalist_filter = st.text_input("Search Medalist Name")
with col2:
    event_filter = st.selectbox("Select an Event", ["All"] + sorted(melted_df["Event"].unique()))
with col3:
    medal_order = ["Gold", "Silver", "Bronze"]
    medal_filter = st.selectbox("Select Medal Type", ["All"] + medal_order)

# Apply filters
filtered_df = melted_df.copy()
if medalist_filter:
    filtered_df = filtered_df[filtered_df["Medalist Name"].str.contains(medalist_filter, case=False, na=False)]
if event_filter != "All":
    filtered_df = filtered_df[filtered_df["Event"] == event_filter]
if medal_filter != "All":
    filtered_df = filtered_df[filtered_df["Medal Type"] == medal_filter]

# Display DataFrame
st.subheader("Filtered Medalist Data")
st.caption("Use the filters above to refine the dataset.")
st.dataframe(filtered_df, hide_index=True)

# Pivot Table Summary
st.subheader("Medal Summary by Event and Type")
st.caption("Aggregated count of medals awarded for each event and type.")
pivot_df = melted_df.pivot_table(index="Event", columns="Medal Type", aggfunc="size", fill_value=0)[["Gold", "Silver", "Bronze"]]
st.dataframe(pivot_df)

# Visualization 1: Total Medals by Event
st.subheader("Total Medals by Event")
st.caption("A bar chart showing the total medals awarded in each event.")
fig, ax = plt.subplots(figsize=(12, 12))
event_counts = melted_df["Event"].value_counts()
sns.barplot(x=event_counts.values, y=event_counts.index, palette="viridis")
plt.xlabel("Total Medals")
plt.ylabel("Event")
plt.yticks(fontsize=9)
st.pyplot(fig)

# Visualization 2: Medal Distribution
st.subheader("Medal Distribution by Type")
st.caption("A count plot showing the distribution of gold, silver, and bronze medals.")
fig, ax = plt.subplots()
sns.countplot(data=melted_df, x="Medal Type", order=medal_order, palette=["gold", "silver", "#cd7f32"])
plt.xlabel("Medal Type")
plt.ylabel("Count")
st.pyplot(fig)

#%%
