import requests
from bs4 import BeautifulSoup
import pandas as pd

import re

from google_play_scraper import app

url = "https://play.google.com/store/games?hl=en_IN&gl=US"


def get_app_ids(url_link):
    url = url_link
    data = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(data.text, "html.parser")

    # Find the anchor tag
    a_tag = soup.find("a", class_="Si6A0c Gy4nib")

    # Extract the href attribute
    if a_tag and "href" in a_tag.attrs:
        href_value = a_tag["href"]
        print(f"Extracted href: {href_value}")
    else:
        print("No href attribute found in the specified <a> tag.")
    my_data = []

    html = BeautifulSoup(data.text, "html.parser")

    # `Gy4nib` tag to select app_id/package name
    articles = html.select("a.Gy4nib")

    articles[0]

    # Extract the href attributes and store them in a list
    my_data = [article["href"] for article in articles if "href" in article.attrs]

    # Print the extracted href values
    for href in my_data:
        print(href)
    len(my_data)

    # Regular expression pattern to extract id from href
    pattern = re.compile(r"/store/apps/details\?id=([^&]+)")

    # Extract ids using regex
    ids = []
    for href in my_data:
        match = pattern.search(href)
        if match:
            ids.append(match.group(1))

    # Create a DataFrame
    df = pd.DataFrame(ids, columns=["App_ID"])

    # Extract App_IDs from the DataFrame
    app_ids = df["App_ID"].tolist()

    return app_ids


def extract_app_data(app_ids):
    print("------------------\n\n\nEntered in extract_app_data\n\n\n------------")

    # Define the columns to be extracted
    columns = [
        "appId",
        "title",
        "description",
        "summary",
        "installs",
        "score",
        "ratings",
        "developer",
        "categories",
        "icon",
        "headerImage",
        "contentRating",
        "contentRatingDescription",
        "released",
        "lastUpdatedOn",
        "version",
        "url",
    ]

    # Initialize a list to store the extracted data
    data = []

    # Iterate over each App_ID and fetch its details
    for app_id in app_ids:
        print(app_id, "\n\n")
        try:
            result = app(
                app_id, lang="en", country="in"  # defaults to 'en'  # defaults to 'in'
            )

            # Extract the specified attributes for the current app_id
            extracted_data = {column: result.get(column, None) for column in columns}
            data.append(extracted_data)

        except Exception as e:
            print(f"Error fetching details for App_ID {app_id}: {e}")

    # Create a DataFrame from the extracted data
    dataset = pd.DataFrame(data)

    return dataset


def extract_game_date(app_ids):
    # Call the function with the extracted App_IDs
    dataset = extract_app_data(app_ids)
    print("Got the Dataset \n\n\n")
    dataset.head(2)
    # Rename the "appId" column to "appId_or_package_name"
    dataset.rename(columns={"appId": "appId_or_package_name"}, inplace=True)

    print(dataset.head())

    # Load the preserved dataset and merger with new data set then save the new dataset with unique rows

    old_data = pd.read_csv("Data/app_details.csv")

    print(old_data.head())

    merged_data = pd.concat([old_data, dataset], axis=0, ignore_index=True)

    merged_data.drop_duplicates(subset=["appId_or_package_name"], inplace=True)

    merged_data["appId_or_package_name"]

    merged_data.reset_index()

    print(merged_data.info())

    # Save the DataFrame to a CSV file
    merged_data.to_csv("Data/app_details.csv", index=False)

    print("Dataset saved successfully.")


if __name__ == "__main__":

    link = input("Enter the URL link:")

    app_ids = get_app_ids(link)

    print(app_ids)

    extract_game_date(app_ids)
