import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


def load_data(file_path):
    """
    Load data from an Excel file containing multiple sheets into a single Pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        pandas.DataFrame: A DataFrame containing the combined data from all sheets in the Excel file.
    """

    sheets_to_read = ['Government', 'Secondary Care', 'Primary Care']
    dfs = {
        sheet: pd.read_excel(file_path, sheet_name=sheet)
        for sheet in sheets_to_read
    }
    combined_df = pd.concat(dfs, keys=sheets_to_read, names=['Sheet'])
    combined_df.reset_index(level='Sheet', inplace=True)

    return combined_df


def main():
    """
    The main function that runs the Streamlit app.

    Returns:
    None
    """
    st.title("Healthcare Centers in Jamaica")

    file_path = "Jamaica Locations Healthcare settings.xlsx"
    combined_df = load_data(file_path)

    combined_df.dropna(subset=["Latitude", "Longitude"], inplace=True)
    combined_df["Latitude"] = pd.to_numeric(
        combined_df["Latitude"], errors='coerce')
    combined_df["Longitude"] = pd.to_numeric(
        combined_df["Longitude"], errors='coerce')
    combined_df.dropna(subset=["Latitude", "Longitude"], inplace=True)

    color_map = {
        'Government': 'red',
        'Secondary Care': 'yellow',
        'Primary Care': 'green'
    }

    fm = folium.Map(location=[combined_df['Latitude'].mean(
    ), combined_df['Longitude'].mean()], zoom_start=10)

    # Loop through sheets in specified order to control layering
    for sheet in ['Primary Care', 'Secondary Care', 'Government']:
        sheet_df = combined_df[combined_df['Sheet'] == sheet]
        for _, row in sheet_df.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=9,  # circle size
                color=color_map[row['Sheet']],  # pick color based on Sheet
                fill=True,
                fill_opacity=0.4,
                popup=row['Name']
            ).add_to(fm)

    folium_static(fm)


if __name__ == "__main__":
    main()
