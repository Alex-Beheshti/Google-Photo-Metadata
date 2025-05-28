import os
import sys
import json
import time
import glob
import shutil
from pathlib import Path
from datetime import datetime
import subprocess


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_global_progress_bar(current, total):
    width = 30
    percent = int(current * 100 / total)
    filled = int(percent * width / 100)
    empty = width - filled
    bar = '█' * filled + '░' * empty
    print(f"🌍 Global Progress       — [{bar}] {percent:3d}% ({current}/{total} folders complete)")


def run_exiftool(image_path, json_path):
    try:
        result = subprocess.run([
            'exiftool',
            f'-overwrite_original',
            f'-json={json_path}',
            image_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False


def get_file_match_reason(image, year_dir):
    ext = image.suffix.lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.mp4', '.mov']:
        return 'Unsupported extension'

    json_matches = list(year_dir.glob(f"{image.name}.supplemental-metadata*.json"))
    if not json_matches:
        return 'No JSON metadata file found'

    return 'Unknown failure'


def main():
    clear_terminal()

    print("📁 Google Takeout Metadata Updater")
    root_dir = input("Enter the full path to your Takeout folders root: ").strip()
    folder_count = int(input("How many Takeout folders do you have? ").strip())

    takeout_folders = [f"Takeout" if i == 0 else f"Takeout {i+1}" for i in range(folder_count)]
    folders = []

    for t_folder in takeout_folders:
        full_path = Path(root_dir) / t_folder / "Google Photos"
        if full_path.exists():
            folders += sorted(full_path.glob("Photos from*/"))

    total_folders = len(folders)
    if total_folders == 0:
        print("❌ No valid folders found.")
        sys.exit(1)

    processed_log = Path(root_dir) / "processed_folders.log"
    report_file = Path(root_dir) / "metadata_update_summary.txt"
    processed = set()
    if processed_log.exists():
        processed = set(processed_log.read_text().splitlines())

    clear_terminal()
    print_global_progress_bar(0, total_folders)
    print()

    count = 0
    with report_file.open("w") as report:
        for year_dir in folders:
            year_str = str(year_dir)
            if year_str in processed:
                count += 1
                continue

            folder_name = year_dir.name
            print(f"\n📂 {folder_name}")
            images = list(year_dir.glob("*.jpg")) + list(year_dir.glob("*.jpeg")) + \
                     list(year_dir.glob("*.JPG")) + list(year_dir.glob("*.JPEG")) + \
                     list(year_dir.glob("*.png")) + list(year_dir.glob("*.PNG")) + \
                     list(year_dir.glob("*.mp4")) + list(year_dir.glob("*.MP4")) + \
                     list(year_dir.glob("*.mov")) + list(year_dir.glob("*.MOV"))

            success, fail = 0, 0
            unmatched = []
            match_summary = {'Unsupported extension': 0, 'No JSON metadata file found': 0, 'Unknown failure': 0}

            for image in images:
                matched_json = list(year_dir.glob(f"{image.name}.supplemental-metadata*.json"))
                if matched_json and run_exiftool(str(image), str(matched_json[0])):
                    success += 1
                else:
                    reason = get_file_match_reason(image, year_dir)
                    match_summary[reason] += 1
                    unmatched.append(image.name)
                    fail += 1

            print(f"✅ Success: {success} | ❌ Failed: {fail}")
            report.write(f"Folder: {year_str}\n")
            report.write(f"✅ Success: {success}\n❌ Failed: {fail}\n")
            for reason, num in match_summary.items():
                if num:
                    report.write(f"   🔹 {reason}: {num}\n")
            if unmatched:
                report.write("   ❗ Unmatched files:\n")
                for file in unmatched:
                    report.write(f"     - {file}\n")
            report.write("----------------------------------------\n")

            with processed_log.open("a") as plog:
                plog.write(f"{year_str}\n")

            count += 1
            print_global_progress_bar(count, total_folders)

    print("\n✅ All done! Summary saved to:", report_file)


if __name__ == '__main__':
    main()
