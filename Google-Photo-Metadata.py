#!/usr/bin/env python3

import os
import glob
import subprocess
from datetime import datetime

ROOT_DIR = input("📁 Enter full path to the Takeout folders (e.g., /home/user/Downloads): ").strip()
NUM_FOLDERS = int(input("🔢 How many Takeout folders are there? (e.g., 3): ").strip())

REPORT = os.path.join(ROOT_DIR, "metadata_update_summary.txt")
PROCESSED_LOG = os.path.join(ROOT_DIR, "processed_folders.log")

def show_menu():
    print("""
📷 What would you like to do?
1. ▶️  Resume processing
2. 🔄  Start over (reset progress)
3. 📄  View last summary report
4. ❌  Exit
    """)
    return input("Enter option [1-4]: ").strip()

option = show_menu()
if option == "2":
    if os.path.exists(PROCESSED_LOG): os.remove(PROCESSED_LOG)
    if os.path.exists(REPORT): os.remove(REPORT)
    print("✅ Progress reset.")
elif option == "3":
    print("\n📄 Showing last summary report:")
    print("----------------------------------------")
    if os.path.exists(REPORT):
        with open(REPORT, 'r') as r:
            print(r.read())
    else:
        print("No report found yet.")
    exit()
elif option == "4":
    print("👋 Exiting.")
    exit()
elif option != "1":
    print("❌ Invalid option. Exiting.")
    exit()

# Ensure log files exist
open(PROCESSED_LOG, 'a').close()

FOLDERS = []
for i in range(NUM_FOLDERS):
    folder_name = "Takeout" if i == 0 else f"Takeout {i+1}"
    folder_path = os.path.join(ROOT_DIR, folder_name)
    if os.path.isdir(folder_path):
        for path in glob.glob(f'{folder_path}/**/Google Photos/Photos from*', recursive=True):
            file_count = len(glob.glob(os.path.join(path, '*.[jJpP]*')))
            file_count += len(glob.glob(os.path.join(path, '*.[mM][pP]4')))
            file_count += len(glob.glob(os.path.join(path, '*.[mM][oO][vV]')))
            print(f"📁 Found {file_count} media files in: {path}")
            FOLDERS.append(path)
    else:
        print(f"⚠️ Folder does not exist: {folder_path}")

TOTAL = len(FOLDERS)
COUNT = 0

def print_progress_bar(current, total, prefix):
    percent = int(current * 100 / total)
    filled = int(percent * 30 / 100)
    empty = 30 - filled
    bar = '█' * filled + '░' * empty
    print(f"\r{prefix} — [{bar}] {percent:3d}% ({current}/{total} folders complete)", end='')

print("\n🌍 Global Progress       — [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]   0% (0/{} folders complete)".format(TOTAL))
print()

for folder in FOLDERS:
    if folder in open(PROCESSED_LOG).read():
        COUNT += 1
        continue

    folder_name = os.path.basename(folder)
    success = 0
    fail = 0
    unmatched = []

    patterns = ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG', '*.mp4', '*.MP4', '*.mov', '*.MOV')
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(folder, pat)))

    total_files = len(files)
    file_count = 0
    print(f"\n📂 {folder_name:<20}")

    for media in files:
        file_count += 1
        percent = int(file_count * 100 / total_files)
        filled = int(percent * 30 / 100)
        empty = 30 - filled
        bar = '█' * filled + '░' * empty
        print(f"\r📂 {folder_name:<20} — [{bar}] {percent:3d}% | ✅ {success} ❌ {fail}", end='')

        base = os.path.basename(media)
        possible_jsons = glob.glob(os.path.join(folder, f"{base}.supplemental-metadata*.json"))

        if possible_jsons:
            try:
                subprocess.run(["exiftool", f"-json={possible_jsons[0]}", "-overwrite_original", media], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                success += 1
            except subprocess.CalledProcessError:
                unmatched.append(base)
                fail += 1
        else:
            unmatched.append(base)
            fail += 1

    print(f"\n📁 {folder_name} — ✅ {success}  ❌ {fail}")

    with open(REPORT, 'a') as r:
        r.write(f"Folder: {folder}\n")
        r.write(f"✅ Success: {success}\n")
        r.write(f"❌ Failed: {fail}\n")
        if unmatched:
            r.write(f"❗ Files not matched or failed:\n")
            for u in unmatched:
                r.write(f"  - {u}\n")
        r.write("----------------------------------------\n")

    with open(PROCESSED_LOG, 'a') as p:
        p.write(f"{folder}\n")

    COUNT += 1
    print_progress_bar(COUNT, TOTAL, "🌍 Global Progress")

print("\n\n✅ All done! Summary saved to:", REPORT)
