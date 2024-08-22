import os
import json
import sys
import argparse
import shutil
import time


def get_mp3_file_info():
    current_directory = os.getcwd()
    file_info_list = []

    for filename in os.listdir(current_directory):
        if filename.lower().endswith('.mp3'):
            file_path = os.path.join(current_directory, filename)
            timestamp = os.path.getmtime(file_path)
            file_info_list.append((filename, timestamp))

    return file_info_list


def save_to_json(data, json_path):
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {json_path}")


def load_from_json(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data


def apply_timestamps(mp3_files_info):
    current_directory = os.getcwd()
    current_files = {filename: os.path.join(
        current_directory, filename) for filename in os.listdir(current_directory)}

    for filename, original_timestamp in mp3_files_info:
        if filename in current_files:
            file_path = current_files[filename]

            os.utime(file_path, (original_timestamp, original_timestamp))
        else:
            print(f"Warning: {filename} not found.")


def recreate_files_sequentially(mp3_files_info, sleep_time):
    current_directory = os.getcwd()
    current_files = {filename: os.path.join(
        current_directory, filename) for filename in os.listdir(current_directory)}

    # Sort files by timestamp (oldest to newest)
    mp3_files_info.sort(key=lambda x: x[1])

    total_files = len(mp3_files_info)
    for i, (filename, _) in enumerate(mp3_files_info, start=1):
        if filename in current_files:
            file_path = current_files[filename]
            temp_path = file_path + ".temp"

            # Recreate the file sequentially
            shutil.copy2(file_path, temp_path)
            os.remove(file_path)
            shutil.move(temp_path, file_path)

            # Set the atime and mtime to the current timestamp to prevent invalid data
            new_timestamp = os.stat(file_path).st_ctime
            os.utime(file_path, (new_timestamp, new_timestamp))

            # Print progress information
            print(f"({i}/{total_files}) {filename}")

            # Sleep for the specified duration
            time.sleep(sleep_time)
        else:
            print(f"Warning: {filename} not found.")


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Read or write MP3 file timestamps using a JSON file.")
    parser.add_argument('json_path', type=str,
                        help="Specify the path for the JSON file.")
    parser.add_argument('-r', '--read', action='store_true',
                        help="Read and save MP3 timestamps to JSON.")
    parser.add_argument('-w', '--write', action='store_true',
                        help="Write timestamps from JSON to MP3 files.")
    parser.add_argument('-s', '--sequence', type=float, nargs='?', const=0,
                        help="Recreate files sequentially by timestamp, with an optional sleep time between files (in seconds).")

    args = parser.parse_args()

    # Handle conflicting switches
    if sum([args.read, args.write, args.sequence is not None]) > 1:
        print("Error: Only one action can be specified at a time. Please choose -r, -w, or -s.")
        sys.exit(1)

    # Perform the appropriate action based on the switch
    if args.read:
        mp3_files_info = get_mp3_file_info()
        save_to_json(mp3_files_info, args.json_path)
    elif args.write:
        mp3_files_info = load_from_json(args.json_path)
        apply_timestamps(mp3_files_info)
    elif args.sequence is not None:
        mp3_files_info = load_from_json(args.json_path)
        sleep_time = args.sequence if args.sequence else 0
        recreate_files_sequentially(mp3_files_info, sleep_time)
    else:
        print("Error: No action specified. Use -r to read timestamps, -w to write them, or -s to sequence files.")


if __name__ == "__main__":
    main()
