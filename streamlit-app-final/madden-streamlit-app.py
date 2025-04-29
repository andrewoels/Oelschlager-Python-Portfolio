import streamlit as st
import pandas as pd
import re
import plotly.express as px


#Importing and cleaning data

#@st.cache_data
def load_data():
    df = pd.read_csv("data/madden_25_ratings.csv")

    # Step 1: Combine first and last names
    df["Name"] = df["firstName"] + " " + df["lastName"]

    # Step 2: Drop original firstName and lastName
    df = df.drop(columns=["firstName", "lastName"])

    # Step 3: Drop columns ending with "/diff"
    diff_cols = [col for col in df.columns if col.endswith("/diff")]
    df = df.drop(columns=diff_cols)

    # Step 4: Drop "stats/overall/value" manually to avoid duplicate
    if "stats/overall/value" in df.columns:
        df = df.drop(columns=["stats/overall/value"])

    # Step 5: Rename "stats/X/value" columns cleanly
    rename_map = {}
    for col in df.columns:
        if col.startswith("stats/") and col.endswith("/value"):
            raw_name = col.split("/")[1]

            # Insert space before capital letters (except first letter)
            pretty_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', raw_name)

            # Title case every word properly
            pretty_name = pretty_name.title()

            rename_map[col] = pretty_name

    df = df.rename(columns=rename_map)

    # Step 6: Move "Name", "Team", "Position", "Overall" to the front
    front_cols = ["Name", "Team", "Position", "Overall"]
    other_cols = [col for col in df.columns if col not in front_cols]
    df = df[front_cols + other_cols]

    return df



# Load cleaned data
df = load_data()

#Formatting – creating a section divider and a line break so the app looks nice
def section_divider():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

def line_break():
    st.markdown("<br>", unsafe_allow_html=True)

#Image header Madden Cover
st.image("images/MaddenCover.jpg")

#App Title
st.markdown("<h1 style='text-align: center;'>Madden NFL 25 Scouting App</h1>", unsafe_allow_html=True)

#Find a Player to Fit Your Scheme
st.markdown("<h3 style='text-align: center;'>Compare players and find the perfect fit for your scheme!</h3>", unsafe_allow_html=True)

line_break()

st.markdown(
    "<div style='text-align: left;'>This app is designed to help Madden NFL franchise mode players scout, compare, and build the perfect team for their unique scheme. First, users can search for players by specific archetypes that align with the roles they need to fill, narrowing down the pool to the athletes who best fit their strategy. Once players are identified, users can dive deeper into a visual comparison of their exact attributes using customizable spider and bar charts, making it easy to spot strengths and weaknesses at a glance. Finally, users can save their customized list of prospects for future reference as they manage their franchise. By helping users find players who are highly skilled yet possibly undervalued, the app empowers franchise GMs to build smarter, more scheme-specific rosters — just like a real NFL front office..</div>",
    unsafe_allow_html=True)

section_divider()

st.markdown("<h3 style='text-align: center;'>🎯 Identify Players by Archetype</h3>", unsafe_allow_html=True)
line_break()

# Step 1: Custom position group map - do this because archetypes have broader applications beyond each specific position
position_group_map = {
    "QB": ["QB"],
    "HB": ["HB"],
    "FB": ["FB"],
    "WR": ["WR"],
    "TE": ["TE"],
    "OT": ["LT", "RT"],
    "G": ["LG", "RG"],
    "C": ["C"],
    "DE": ["LE", "RE"],
    "DT": ["DT"],
    "LB": ["LOLB", "MLB", "ROLB"],
    "CB": ["CB"],
    "S": ["FS", "SS"],
    "K": ["K"],
    "P": ["P"]
}

# Step 2: Build archetype list based on logical order
ordered_archetypes = []
for group in position_group_map.keys():
    group_positions = position_group_map[group]
    group_archetypes = df[df["Position"].isin(group_positions)]["Archetype"].dropna().unique()
    for archetype in sorted(group_archetypes):
        if archetype not in ordered_archetypes:
            ordered_archetypes.append(archetype)

# Step 3: Archetype selector
selected_archetype = st.selectbox(
    "First, select an archetype to scout. This is based on Madden's predefined archetypes for each position.",
    ordered_archetypes
)

# Step 4: Filter and Display
if selected_archetype:
    filtered_archetype_df = df[df["Archetype"] == selected_archetype]

    if not filtered_archetype_df.empty:
        st.markdown(f"Top players for **{selected_archetype}** archetype. Click on a column header to sort the table by that attribute in ascending or descending order.")

        top_players = filtered_archetype_df.sort_values(by="Overall", ascending=False)

        # Step 5: Clean up columns

# Always start with these basic columns if they exist
        base_columns = ["Name", "Team", "Position", "Overall"]
        optional_columns = ["Height (Inches)", "Weight"]

        columns_to_keep = []

        # Add base columns if they exist
        for col in base_columns:
            if col in top_players.columns:
                columns_to_keep.append(col)

        # Add height and weight if they exist
        for col in optional_columns:
            if col in top_players.columns:
                columns_to_keep.append(col)

        # Now handle performance attributes dynamically
        all_columns = list(df.columns)
        if "Acceleration" in all_columns:
            accel_idx = all_columns.index("Acceleration")
            performance_attrs = all_columns[accel_idx:]
        else:
            performance_attrs = [col for col in all_columns if col not in ["Name", "Team", "Position", "Overall"]]

        for attr in performance_attrs:
            if attr in top_players.columns:
                attr_values = pd.to_numeric(top_players[attr], errors='coerce')
                if (attr_values < 40).any():
                    continue  # Skip attributes with any player under 40 because these are going to be attributes that aren't important for the position
                else:
                    columns_to_keep.append(attr)

        # Remove "Running Style" manually if it somehow exists because this doesn't affect gameplay performance
        if "Running Style" in columns_to_keep:
            columns_to_keep.remove("Running Style")

        #Finalize: Static base columns + dynamic stat columns sorted alphabetically
        static_columns = [col for col in ["Name", "Team", "Position", "Overall", "Height (Inches)", "Weight"] if col in columns_to_keep]
        dynamic_columns = sorted([col for col in columns_to_keep if col not in static_columns])
        final_columns = static_columns + dynamic_columns

        # Display the final cleaned table
        display_df = top_players[final_columns]
        st.dataframe(display_df, use_container_width=True)

    else:
        st.warning("No players found for this archetype.")



section_divider()

#Radar/Spider Chart Section
st.markdown("<h3 style='text-align: center;'>📈 Visually Compare Player Attributes</h3>", unsafe_allow_html=True)
line_break()
#st.subheader("📈 Compare Player Attributes (Spider Chart or Bar Chart)")

# Step 1: Custom position order
position_order = ["QB", "HB", "FB", "WR", "TE",
                  "LT", "LG", "C", "RG", "RT",
                  "LE", "DT", "RE",
                  "LOLB", "MLB", "ROLB",
                  "CB", "S",
                  "K", "P"]

available_positions = [pos for pos in position_order if pos in df["Position"].unique()]

# Step 2: Search Filters
st.markdown("#### 🔎 Filter Options")
col1, col2 = st.columns(2)

#position filter
with col1:
    selected_positions = st.multiselect(
        "Filter by Position",
        options=available_positions
    )

#team filter
with col2:
    selected_teams = st.multiselect(
        "Filter by Team",
        options=sorted(df["Team"].dropna().unique())
    )


# Step 3: Apply Filters
filtered_df = df.copy()

if selected_positions:
    filtered_df = filtered_df[filtered_df["Position"].isin(selected_positions)]
if selected_teams:
    filtered_df = filtered_df[filtered_df["Team"].isin(selected_teams)]


# Step 4: Player Selection
players_selected = st.multiselect(
    "Choose players from filtered list:",
    options=filtered_df["Name"].unique(),
    key="player_selector"
)

# Step 5: Chart Type Toggle
if players_selected:
    chart_type = st.radio(
        "Select Chart Type:",
        ["Spider Chart", "Bar Chart"],
        index=0,
        horizontal=True,
        key="chart_type_selector"
    )

    # Step 6: Spider Chart / Bar Chart logic
    first_player = players_selected[0]
    player_position = df[df["Name"] == first_player]["Position"].values[0]

    position_attribute_defaults = {
        "QB": ["Throw Power", "Throw Accuracy Short", "Throw Accuracy Mid", "Throw Accuracy Deep", "Awareness", "Speed", "Agility", "Strength"],
        "HB": ["Speed", "Acceleration", "Agility", "Carrying", "Break Tackle", "Trucking", "Juke"],
        "FB": ["Strength", "Carrying", "Run Block", "Awareness"],
        "WR": ["Speed", "Acceleration", "Catching", "Short Route Running", "Medium Route Running", "Deep Route Running", "Catch In Traffic"],
        "TE": ["Catching", "Run Block", "Strength", "Speed", "Awareness"],
        "LT": ["Strength", "Pass Block", "Pass Block Power", "Run Block", "Run Block Power", "Awareness"],
        "LG": ["Strength", "Pass Block", "Pass Block Power", "Run Block", "Run Block Power", "Awareness"],
        "C":  ["Strength", "Pass Block", "Pass Block Power", "Run Block", "Run Block Power", "Awareness"],
        "RG": ["Strength", "Pass Block", "Pass Block Power", "Run Block", "Run Block Power", "Awareness"],
        "RT": ["Strength", "Pass Block", "Pass Block Power", "Run Block", "Run Block Power", "Awareness"],
        "LE": ["Strength", "Power Moves", "Finesse Moves", "Block Shedding", "Awareness"],
        "DT": ["Strength", "Power Moves", "Block Shedding", "Awareness"],
        "RE": ["Strength", "Power Moves", "Finesse Moves", "Block Shedding", "Awareness"],
        "LOLB": ["Speed", "Tackle", "Hit Power", "Block Shedding", "Zone Coverage", "Man Coverage"],
        "MLB":  ["Speed", "Tackle", "Hit Power", "Block Shedding", "Zone Coverage", "Man Coverage"],
        "ROLB": ["Speed", "Tackle", "Hit Power", "Block Shedding", "Zone Coverage", "Man Coverage"],
        "CB": ["Speed", "Man Coverage", "Zone Coverage", "Awareness", "Acceleration", "Agility"],
        "S": ["Speed", "Zone Coverage", "Hit Power", "Awareness", "Acceleration"],
        "K": ["Kick Power", "Kick Accuracy"],
        "P": ["Kick Power", "Kick Accuracy"],
    }

    default_attrs = position_attribute_defaults.get(player_position, ["Speed", "Strength", "Agility", "Awareness"])

    all_columns = list(df.columns)
    if "Acceleration" in all_columns:
        accel_idx = all_columns.index("Acceleration")
        performance_attrs = all_columns[accel_idx:]
    else:
        performance_attrs = [col for col in all_columns if col not in ["Name", "Team", "Position", "Overall"]]

    default_attrs_filtered = [attr for attr in default_attrs if attr in performance_attrs]

    attributes_to_plot = st.multiselect(
        "Select Attributes to Compare",
        options=performance_attrs,
        default=default_attrs_filtered,
        key="attribute_selector"
    )

    if attributes_to_plot:
        compare_df = df[df["Name"].isin(players_selected)]
        melted = compare_df.melt(id_vars=["Name"], value_vars=attributes_to_plot,
                                 var_name="Attribute", value_name="Rating")

        if chart_type == "Spider Chart":
            fig = px.line_polar(
                melted,
                r="Rating",
                theta="Attribute",
                color="Name",
                line_close=True
            )
            fig.update_traces(fill='toself')
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[60, 100],
                        showline=True,
                        showticklabels=True,
                        ticks='outside',
                        gridcolor="lightgray"
                    ),
                    angularaxis=dict(
                        gridcolor="lightgray"
                    )
                ),
                showlegend=True
            )
        else:
            fig = px.bar(
                melted,
                x="Attribute",
                y="Rating",
                color="Name",
                barmode="group"
            )
            fig.update_layout(
                yaxis=dict(range=[60, 100])
            )

        st.plotly_chart(fig, use_container_width=True)

        # Step 7: Download Button
        st.markdown("### 📥 Download Selected Players")
        download_df = compare_df[["Name", "Team", "Position", "Overall"] + attributes_to_plot]
        csv = download_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='selected_players.csv',
            mime='text/csv'
        )

    else:
        st.info("Please select at least one attribute to plot.")
else:
    st.info("Please select players above to start comparing their attributes.")






