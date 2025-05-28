📸 Google Takeout Metadata Updater

A command-line tool to automatically apply metadata from your Google Takeout .json files to corresponding photo and video files using exiftool.

✅ Features

🗂️ Works across multiple Takeout folders (e.g., Takeout, Takeout 2, Takeout 3, etc.)

📁 Supports all standard Google Photos exports (Photos from YYYY folders).

🔍 Matches media files (.jpg, .jpeg, .png, .mp4, .mov) with their .supplemental-metadata.json files.

💠 Uses exiftool to embed the metadata directly into the files.

📊 Shows a global progress bar at the top of the screen.

📄 Saves a detailed summary report with:

✅ Files successfully updated

❌ Files failed and why:

Unsupported extension

No JSON metadata found

Unknown error

🧠 Skips already processed folders to save time.

🧼 Optionally reset progress for a fresh run.

📦 Requirements

Python 3.6+

exiftool installed and accessible in your PATH

Install exiftool (if needed):

# macOS (with Homebrew)
brew install exiftool

# Ubuntu/Debian
sudo apt-get install libimage-exiftool-perl

🚀 How to Use

Save the script as update_metadata.py.

Run the script:

python3 update_metadata.py

Follow the prompts:

Enter the full path to the folder containing all your Takeout, Takeout 2, etc.

Enter how many Takeout folders you have.

💡 The script will:

Scan all relevant folders.

Update metadata on matching media files.

Show live progress.

Log results to metadata_update_summary.txt.

📁 Files Generated

metadata_update_summary.txt: Summary of matched and unmatched files, saved in the same root directory.

processed_folders.log: Keeps track of which folders have been processed.

🔁 Resetting Progress

To rerun the tool from scratch:

Delete metadata_update_summary.txt and processed_folders.log from your root directory.

Rerun the script and select new inputs.

🔢 Example Folder Structure

/Users/yourname/Downloads/
├── Takeout/
│   └── Google Photos/
│       ├── Photos from 2021/
│       ├── Photos from 2022/
│       └── ...
├── Takeout 2/
│   └── Google Photos/
│       └── Photos from 2023/

