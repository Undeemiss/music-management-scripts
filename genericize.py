import sys


def replace_in_file(file_path, to_replace, replace_with):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            content = file.read()

        # Replace the specified string
        updated_content = content.replace(to_replace, replace_with)

        # Open the file in write mode to overwrite the content
        with open(file_path, 'w') as file:
            file.write(updated_content)

        print(f"Replacement successful in {file_path}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 2:
        print("Usage: python genericize.py <file_path1> [<file_path2> ...]")
    else:
        # Get command-line arguments starting from index 1 (excluding the script name)
        file_paths = sys.argv[1:]

        # Call the function for each file path
        for file_path in file_paths:
            if (file_path.endswith(('.m3u'))):
                replace_in_file(file_path, "/home/undeemiss/Music", "..")
            else:
                print(f"Skipping file {file_path}")
