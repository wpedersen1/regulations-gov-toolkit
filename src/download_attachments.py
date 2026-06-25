import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
import requests
import pandas as pd

from config import API_KEY

COMMENTS_FILE = "output/comments.csv"
BASE_URL = "https://api.regulations.gov/v4/comments"

headers = {
    "X-Api-Key": API_KEY
}

comments = pd.read_csv(COMMENTS_FILE)

attachments = []

print(f"Checking {len(comments)} comments for attachments...\n")

for i, row in comments.iterrows():

    comment_id = row["CommentID"]
    url = f"{BASE_URL}/{comment_id}/attachments"

    while True:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            break

        elif response.status_code == 429:

            retry_after = response.headers.get("Retry-After")

            if retry_after:
                wait_time = int(retry_after)
            else:
                wait_time = 5

            print(f"Rate limit reached. Waiting {wait_time} seconds...")

            time.sleep(wait_time)

            continue

        else:
            print(f"{comment_id} -> HTTP {response.status_code}")
            response = None
            break

    if response is None:
        continue

    data = response.json()

    for attachment in data.get("data", []):

        attrs = attachment.get("attributes", {})
        formats = attrs.get("fileFormats", [])

        if not formats:

            attachments.append({
                "CommentID": comment_id,
                "AttachmentID": attachment.get("id"),
                "Format": None,
                "FileURL": None,
                "Size": None
            })

        else:

            for f in formats:

                attachments.append({
                    "CommentID": comment_id,
                    "AttachmentID": attachment.get("id"),
                    "Format": f.get("format"),
                    "FileURL": f.get("fileUrl"),
                    "Size": f.get("size")
                })

    if (i + 1) % 25 == 0:
        print(f"Processed {i + 1} of {len(comments)} comments...")

    # Be polite to the API
    time.sleep(0.25)

os.makedirs("output", exist_ok=True)

df = pd.DataFrame(attachments)

df.to_csv("output/attachments.csv", index=False)
df.to_excel("output/attachments.xlsx", index=False)

print()
print("=" * 50)
print(f"Finished!")
print(f"Comments checked: {len(comments)}")
print(f"Attachment records found: {len(df)}")
print("=" * 50)
print()
print("Saved:")
print("  output/attachments.csv")
print("  output/attachments.xlsx")