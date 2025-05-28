import os
import json
import time
import mimetypes
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.mov', '.mp4']

RESET_LINE = "\033[K"


def extract_timestamp_from_json(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            timestamp_str = data.get('photoTakenTime', {}).get('timestamp')
            if timestamp_str:
                return datetime.fromtimestamp(int(timestamp_str))
    except Exception as e:
        return None
    return None


def set_file_timestamp(file_path, timestamp):
    try:
        mod_time = timestamp.timestamp()
        os.utime(file_path, (mod_time, mod_time))
        return True
    except Exception:
        return False


def count_json_matches(media_files, json_files):
    match_count = 0
    matchable_files = {}
    json_stems = {Path(j).stem.replace(' (1)', ''): j for j in json_files}
    for media_file in media_files:
        stem = Path(media_file).stem
        json_file = json_stems.get(stem)
        if json_file:
            matchable_files[media_file] = json_file
            match_count += 1
    return matchable_files, match_count


def print_global_progress(folder_idx, total_folders):
    percent = int((folder_idx / total_folders) * 100)
    bar_length = 30
    filled_length = int(bar_length * folder_idx // total_folders)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f"\033[1A🌍 Global Progress — [{bar}]  {percent:>3}% ({folder_idx}/{total_folders} folders complete)\033[0m{RESET_LINE}")


def main():
    root_dir = Path.cwd()
    all_folders = [p for p in root_dir.iterdir() if p.is_dir()]

    print(f"\n🧠 Scanning {len(all_folders)} folders...\n")
    folder_match_counts = {}

    for folder in all_folders:
        media_files = [str(f) for f in folder.glob("*") if f.suffix.lower() in SUPPORTED_EXTENSIONS]
        json_files = [str(f) for f in folder.glob("*.json")]
        matches, count = count_json_matches(media_files, json_files)
        folder_match_counts[folder] = (matches, count, len(media_files))
        print(f"📂 {folder.name:<20} — Matchable: {count:>3} / Total Media: {len(media_files):>3}")

    print("\n✅ Starting metadata update...\n")

    total_folders = len(folder_match_counts)
    completed_folders = 0

    for folder, (matches, _, total_media) in folder_match_counts.items():
        success, fail = 0, 0
        print_global_progress(completed_folders, total_folders)
        print(f"📂 {folder.name:<20}")

        progress = tqdm(matches.items(), desc=f"📂 {folder.name:<20}", ncols=80)

        for media_file, json_file in progress:
            timestamp = extract_timestamp_from_json(json_file)
            if timestamp:
                if set_file_timestamp(media_file, timestamp):
                    success += 1
                else:
                    fail += 1
            else:
                fail += 1

        total_attempted = len(matches)
        not_matchable = total_media - total_attempted
        print(f"📁 {folder.name} — ✅ {success}  ❌ {fail}  ⚠️ Not matchable: {not_matchable}")
        completed_folders += 1

    print_global_progress(completed_folders, total_folders)
    print("\n🎉 All folders processed!")


if __name__ == '__main__':
    main()
