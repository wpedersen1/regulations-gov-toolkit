import os
import requests
import pandas as pd

from config import API_KEY, DOCKET_ID, PAGE_SIZE

BASE_URL = "https://api.regulations.gov/v4/comments"

headers = {
    "X-Api-Key": API_KEY
}

all_comments = []

page = 1

while True:

    print(f"Downloading page {page}...")

    params = {
        "filter[docketId]": DOCKET_ID,
        "page[size]": PAGE_SIZE,
        "page[number]": page
    }

    response = requests.get(
        BASE_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    json_data = response.json()

    all_comments.extend(json_data["data"])

    meta = json_data["meta"]

    if meta["lastPage"]:
        break

    page += 1

print()
print(f"Downloaded {len(all_comments)} comments.")

rows = []

for comment in all_comments:

    attrs = comment["attributes"]

    rows.append({

        "CommentID": comment["id"],
        "Title": attrs.get("title"),
        "PostedDate": attrs.get("postedDate"),
        "LastModified": attrs.get("lastModifiedDate"),
        "Agency": attrs.get("agencyId"),
        "DocumentType": attrs.get("documentType"),
        "Withdrawn": attrs.get("withdrawn"),
        "ObjectID": attrs.get("objectId")

    })

df = pd.DataFrame(rows)

os.makedirs("output", exist_ok=True)

csv_file = "output/comments.csv"
xlsx_file = "output/comments.xlsx"

df.to_csv(csv_file, index=False)
df.to_excel(xlsx_file, index=False)

print()
print(df.head())

print()
print(f"CSV saved to {csv_file}")
print(f"Excel saved to {xlsx_file}")