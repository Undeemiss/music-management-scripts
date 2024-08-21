import os
import json
import sys
import argparse
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
            print(f"Warning: {
                  filename} is listed in the JSON but not found in the current directory.")


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

    args = parser.parse_args()

    # Handle conflicting switches
    if args.read and args.write:
        print("Error: Both -r and -w options cannot be used at the same time. Please choose either -r or -w.")
        sys.exit(1)

    # Perform the appropriate action based on the switch
    if args.read:
        mp3_files_info = get_mp3_file_info()
        save_to_json(mp3_files_info, args.json_path)
    elif args.write:
        mp3_files_info = load_from_json(args.json_path)
        apply_timestamps(mp3_files_info)
    else:
        print("Error: No action specified. Use -r to read timestamps or -w to write them.")


if __name__ == "__main__":
    main()
