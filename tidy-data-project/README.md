# 🏅 Olympic Medalists Dashboard

Welcome to the **Olympic Medalists Data Dashboard**! 🎉  
This interactive Streamlit app allows users to explore and filter Olympic medalist data from the 2008 games. 

## 📌 Features 
- 🎯 **Filter** by name, event,and medal type
- 📑 **Aggregated pivot table** for an easy-to-digest summary    
- 📊 **Visualizations** to better understand the distribution of medals by event


## 🛠️ Data Preprocessing
The dataset originally contained Olympic medalist data in a wide format, unideal for analysis and visualizations. To make the data more usable for analysis and visualization, it was transformed into a tidy format using the following steps:

1. Loading Data: Read the CSV file using pandas.
2. Reshaping Data: Converted from wide format to tidy format using pd.melt(), ensuring each row represents a single observation (medalist-event-medal type).
3. Cleaning Data: Removed empty rows using dropna(), standardized column names, and ensured consistency in medal types (Gold, Silver, Bronze).
4. Filtering & Display: Added interactive filters to dynamically display and sort data.
5. Aggregation: Created a pivot table summarizing medal counts for each event.


## 📊 Tidy Data Principles
This project follows Tidy Data principles as outlined by Hadley Wickham:
- Each variable forms a column (e.g., Medalist Name, Event, Medal Type).
- Each observation forms a row (each row contains one medalist's achievement).
- Each value is in a single cell (no merged or nested data structures).

This structure allows for efficient filtering, aggregation, and visualization, making it easier to analyze Olympic medalist data. 


## 🚀 Installation
1. Clone this repository
2. Install dependencies
3. Run the Streamlit app


## 📦 Dependencies
Ensure you have the following Python libraries installed:

- Pandas
- Streamlit
- Matplotlib
- Seaborn


## 🖥️ Usage
Once the app is running, you can:

- Use the filters at the top to refine the dataset
- View the summary table to see aggregated medal counts
- Explore visualizations
