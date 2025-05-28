# Google-Photo-Metadata-updater
# 📷 Google Photo Metadata Tool

This Python script helps you reapply original metadata (timestamps, GPS, etc.) to media files exported from Google Takeout using accompanying `.json` metadata files.

It uses `exiftool` to write metadata back to media files (photos and videos).

---

## ✅ Features

- Automatically detects and processes folders like `Takeout`, `Takeout 2`, etc.
- Handles `JPG`, `JPEG`, `PNG`, `MP4`, and `MOV` files.
- Shows progress bars for each folder and the overall run.
- Supports resume, reset, and summary report options.
- Skips folders already processed (unless reset).
- Logs successes and unmatched media files.

---

## 🛠️ Requirements

- Python 3.6+
- [`exiftool`](https://exiftool.org/) installed and available in your PATH.

You can install exiftool via:

```bash
# macOS
brew install exiftool

# Ubuntu/Debian
sudo apt update && sudo apt install libimage-exiftool-perl
```

---

## 🚀 How to Run

1. **Clone this repository:**

```bash
git clone https://github.com/Alex-Beheshti/Google-Photo-Metadata.git
cd Google-Photo-Metadata
```

2. **Make the script executable (optional on Unix-like systems):**

```bash
chmod +x Google-Photo-Metadata.py
```

3. **Run the tool:**

```bash
./Google-Photo-Metadata.py
```

Or with Python directly:

```bash
python3 Google-Photo-Metadata.py
```

---

## 📁 Sample Input Folder Structure

```bash
Downloads/
├── Takeout/
│   └── Google Photos/
│       └── Photos from 2020/
│           ├── IMG_20200101.jpg
│           ├── IMG_20200101.jpg.supplemental-metadata.json
├── Takeout 2/
    └── ...
```

---

## 📝 Notes

- The script will prompt you to provide the full path to the root folder containing `Takeout`, `Takeout 2`, etc.
- A summary report is generated at the end and saved in the folder you provide.

---

## 📄 License

MIT
