import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ATP Race Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data(filepath):

    df = pd.read_csv(filepath)

    df["tourney_date"] = pd.to_datetime(
        df["tourney_date"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    df["year"] = df["tourney_date"].dt.year

    return df


filepath = "data/ATP 2026.csv"
df = load_data(filepath)

# --------------------------------------------------
# ATP POINTS TABLES
# --------------------------------------------------

POINT_TABLES = {

    "G": {   # Grand Slam
        "W": 2000,
        "F": 1300,
        "SF": 800,
        "QF": 400,
        "R16": 200,
        "R32": 100,
        "R64": 50,
        "R128": 10
    },

    "M": {   # Masters 1000
        "W": 1000,
        "F": 650,
        "SF": 400,
        "QF": 200,
        "R16": 100,
        "R32": 50,
        "R64": 30
    },

    "500": {
        "W": 500,
        "F": 330,
        "SF": 200,
        "QF": 100,
        "R16": 50,
        "R32": 25
    },

    "250": {
        "W": 250,
        "F": 165,
        "SF": 100,
        "QF": 50,
        "R16": 25,
        "R32": 13
    }
}

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("ATP Filtered Race Rankings")

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox(
    "Year",
    sorted(df["year"].dropna().unique())
)

filtered_df = df[df["year"] == selected_year]

selected_tournaments = st.sidebar.multiselect(
    "Tournament Name",
    sorted(filtered_df["tourney_name"].dropna().unique()),
    default=sorted(filtered_df["tourney_name"].dropna().unique())
)

selected_surfaces = st.sidebar.multiselect(
    "Surface",
    sorted(filtered_df["surface"].dropna().unique()),
    default=sorted(filtered_df["surface"].dropna().unique())
)

selected_levels = st.sidebar.multiselect(
    "Tournament Level",
    sorted(filtered_df["tourney_level"].dropna().unique()),
    default=sorted(filtered_df["tourney_level"].dropna().unique())
)

filtered_df = filtered_df[
    filtered_df["tourney_name"].isin(selected_tournaments)
]

filtered_df = filtered_df[
    filtered_df["surface"].isin(selected_surfaces)
]

filtered_df = filtered_df[
    filtered_df["tourney_level"].isin(selected_levels)
]

# --------------------------------------------------
# BUILD RACE POINTS
# --------------------------------------------------

player_points = {}

for _, row in filtered_df.iterrows():

    level = row["tourney_level"]
    round_played = row["round"]

    if level not in POINT_TABLES:
        continue

    table = POINT_TABLES[level]

    # Champion gets winner points
    if round_played == "F":

        winner_points = table["W"]
        loser_points = table["F"]

        player_points[row["winner_name"]] = (
            player_points.get(row["winner_name"], 0)
            + winner_points
        )

        player_points[row["loser_name"]] = (
            player_points.get(row["loser_name"], 0)
            + loser_points
        )

    elif round_played == "SF":

        loser_points = table["SF"]

        player_points[row["loser_name"]] = (
            player_points.get(row["loser_name"], 0)
            + loser_points
        )

    elif round_played == "QF":

        loser_points = table["QF"]

        player_points[row["loser_name"]] = (
            player_points.get(row["loser_name"], 0)
            + loser_points
        )

    elif round_played == "R16":

        loser_points = table["R16"]

        player_points[row["loser_name"]] = (
            player_points.get(row["loser_name"], 0)
            + loser_points
        )

    elif round_played == "R32":

        loser_points = table["R32"]

        player_points[row["loser_name"]] = (
            player_points.get(row["loser_name"], 0)
            + loser_points
        )

    elif round_played == "R64":

        loser_points = table.get("R64", 0)

        player_points[row["loser_name"]] = (
            player_points.get(row["loser_name"], 0)
            + loser_points
        )

    elif round_played == "R128":

        loser_points = table.get("R128", 0)

        player_points[row["loser_name"]] = (
            player_points.get(row["loser_name"], 0)
            + loser_points
        )

# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

race_table = pd.DataFrame(
    list(player_points.items()),
    columns=["Player", "Race Points"]
)

race_table = race_table.sort_values(
    "Race Points",
    ascending=False
).reset_index(drop=True)

race_table.index = race_table.index + 1

# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

st.subheader("ATP Race Rankings")

st.dataframe(
    race_table,
    use_container_width=True
)

st.metric(
    "Players Ranked",
    len(race_table)
)