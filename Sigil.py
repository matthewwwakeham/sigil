import os
import datetime
import sys
import subprocess
import readline
import atexit
import shutil
from subprocess import run

# Enable command history
histfile = os.path.join(os.path.expanduser("~"), ".sigil_history")
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, histfile)

def show_system_info():
    if shutil.which("neofetch"):
        run(["neofetch"])
    else:
        run(["uname", "-a"])

def list_files():
    path = os.getcwd()
    files = os.listdir(path)
    if files:
        for file in files:
            file_path = os.path.join(path, file)
            size = os.path.getsize(file_path)
            file_type = os.path.splitext(file)[1]
            permissions = oct(os.stat(file_path).st_mode)[-3:]
            mod_time = os.path.getmtime(file_path)
            mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')

            print(f"{file} (Type: {file_type}, Size: {size} bytes, Permissions: {permissions}, Modified: {mod_time_str})")
    else:
        print("No files or folders in the current directory.")

def change_directory():
    path = input("Enter path: ")
    try:
        if path == "..":
            os.chdir(os.path.dirname(os.getcwd()))
        else:
            expanded_path = os.path.expanduser(path)
            os.chdir(expanded_path)
    except FileNotFoundError:
        print("Directory not found.")

def create_file():
    file_name = input("Enter file name: ")
    try:
        if not file_name:
            print("File name cannot be empty.")
            return

        with open(file_name, 'w') as file:
            file.write("File created!")
        print("File created successfully.")
    except IOError:
        print("Error creating the file.")

def create_folder():
    folder_name = input("Enter folder name: ")
    try:
        if not folder_name:
            print("Folder name cannot be empty.")
            return

        os.mkdir(folder_name)
        print("Folder created successfully.")
    except FileExistsError:
        print("Folder already exists.")
    except OSError:
        print("Error creating the folder.")

def delete_file():
    file_path = input("Enter file path: ")
    try:
        if not file_path:
            print("File path cannot be empty.")
            return

        os.remove(file_path)
        print("File deleted successfully.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")

def open_path():
    path = input("Enter path: ")
    try:
        if not path:
            print("Path cannot be empty.")
            return

        expanded_path = os.path.expanduser(path)
        if sys.platform.startswith("win"):
            subprocess.run(["start", expanded_path], shell=True)
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", expanded_path])
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", expanded_path])
    except FileNotFoundError:
        print("Error opening the path.")

def clear_screen():
    if sys.platform.startswith("win"):
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def print_welcome_message():
    print("           __")
    print("   __,-~~/~    `---.")
    print(" _/_,---(      ,    )")
    print("/        \    /    /")
    print("~         `\ /'   /")
    print("            |    |")
    print("            |    |")
    print("            |    |")
    print("            |    |")
    print("            |    |")
    print("           /     |")
    print("          /      /")
    print("         /      /")
    print("        /     ,'  Sigil")
    print("       /     /")
    print("      /    ,'")
    print("     (    (     ")
    print("      `.___'")
    print("")

def show_help():
    print("Available commands:")
    print("neofetch     - Display system information")
    print("ls           - List files and folders in the current directory")
    print("cd           - Change the current directory")
    print("mkfile       - Create a new file")
    print("mkfolder     - Create a new folder")
    print("del          - Delete a file")
    print("open         - Open a file or folder")
    print("rename       - Rename a file or folder")
    print("move         - Move a file or folder")
    print("copy         - Copy a file or folder")
    print("search       - Search for files based on a pattern")
    print("cls          - Clear the screen")
    print("exit         - Exit the program")

def rename_file():
    old_name = input("Enter the current name of the file or folder: ")
    new_name = input("Enter the new name: ")
    try:
        if not old_name or not new_name:
            print("Invalid names.")
            return

        os.rename(old_name, new_name)
        print("File or folder renamed successfully.")
    except FileNotFoundError:
        print("File or folder not found.")
    except FileExistsError:
        print("A file or folder with the new name already exists.")
    except OSError:
        print("Error renaming the file or folder.")

def move_file():
    source_path = input("Enter the source file or folder path: ")
    destination_path = input("Enter the destination path: ")
    try:
        if not source_path or not destination_path:
            print("Invalid paths.")
            return

        destination_path = os.path.join(destination_path, os.path.basename(source_path))
        shutil.move(source_path, destination_path)
        print("File or folder moved successfully.")
    except FileNotFoundError:
        print("Source file or folder not found.")
    except shutil.Error:
        print("Error moving the file or folder.")

def copy_file():
    source_path = input("Enter the source file or folder path: ")
    destination_path = input("Enter the destination path: ")
    try:
        if not source_path or not destination_path:
            print("Invalid paths.")
            return

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print("File copied successfully.")
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
            print("Directory copied successfully.")
        else:
            print("Source file or folder not found.")
    except FileNotFoundError:
        print("Source file or folder not found.")
    except shutil.Error:
        print("Error copying the file or folder.")

def search_files():
    pattern = input("Enter the search pattern: ")
    try:
        if not pattern:
            print("Invalid search pattern.")
            return

        matches = []
        for root, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if pattern in filename:
                    matches.append(os.path.join(root, filename))

        if matches:
            print("Matching files:")
            for match in matches:
                print(match)
        else:
            print("No matching files found.")
    except Exception:
        print("Error occurred during the search.")

def main():
    print_welcome_message()

    while True:
        command = input("[Sigil]$ ")
        if command == "neofetch":
            show_system_info()
        elif command == "ls":
            list_files()
        elif command == "cd":
            change_directory()
        elif command == "mkfile":
            create_file()
        elif command == "mkfolder":
            create_folder()
        elif command == "del":
            delete_file()
        elif command == "open":
            open_path()
        elif command == "cls":
            clear_screen()
        elif command == "exit":
            sys.exit()
        elif command == "help":
            show_help()
        elif command == "rename":
            rename_file()
        elif command == "move":
            move_file()
        elif command == "copy":
            copy_file()
        elif command == "search":
            search_files()
        else:
            print("Invalid command. Type 'help' to see the available commands.")

if __name__ == "__main__":
    main()