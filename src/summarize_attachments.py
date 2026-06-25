import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd

attachments = pd.read_excel("output/attachments.xlsx")

summary = (
    attachments
    .groupby("CommentID")
    .size()
    .reset_index(name="AttachmentCount")
)

summary["HasAttachments"] = "Yes"

summary = summary[
    ["CommentID", "HasAttachments", "AttachmentCount"]
]

summary = summary.sort_values("CommentID")

summary.to_excel(
    "output/comments_with_attachments.xlsx",
    index=False
)

print()
print(f"Comments with attachments: {len(summary)}")
print(f"Attachment files: {attachments.shape[0]}")
print()
print(summary.head(10))
print()
print("Saved:")
print("output/comments_with_attachments.xlsx")