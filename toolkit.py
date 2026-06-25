import subprocess
import sys

print("=" * 60)
print(" Regulations.gov Toolkit")
print("=" * 60)

steps = [
    ("Downloading comments", "src/download_comments.py"),
    ("Checking attachments", "src/download_attachments.py"),
    ("Building summary report", "src/summarize_attachments.py")
]

for title, script in steps:

    print()
    print("-" * 60)
    print(title)
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:
        print()
        print(f"ERROR running {script}")
        sys.exit(1)

print()
print("=" * 60)
print("Toolkit completed successfully!")
print("=" * 60)