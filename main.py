from pathlib import Path


def read_file_and_folder():
    path = Path(".")
    items = list(path.rglob("*"))
    for i, item in enumerate(items, start=1):
        print(f"{i} : {item}")


def create_file():
    try:
        read_file_and_folder()
        file_name = input("Enter name of file: ")
        p = Path(file_name)

        if not p.exists():
            data = input("What data do you want to write in it: ")
            with open(p, "w") as fs:
                fs.write(data)
            print("FILE CREATED SUCCESSFULLY")
        else:
            print("FILE ALREADY EXISTS")
    except Exception as err:
        print(f"An error occurred: {err}")


def read_file():
    try:
        read_file_and_folder()
        file_name = input("Enter name of file: ")
        p = Path(file_name)

        if p.exists() and p.is_file():
            with open(p, "r") as fs:
                data = fs.read()
                print(data)
            print("FILE READ SUCCESSFULLY")
        else:
            print("FILE DOES NOT EXIST")
    except Exception as err:
        print(f"An error occurred: {err}")


def append_file():
    try:
        read_file_and_folder()
        file_name = input("Enter name of file: ")
        p = Path(file_name)

        if p.exists() and p.is_file():
            data = input("What data do you want to write in it: ")
            with open(p, "a") as fs:
                fs.write("\n" + data)
            print("FILE UPDATED SUCCESSFULLY")
        else:
            print("FILE DOES NOT EXIST")
    except Exception as err:
        print(f"An error occurred: {err}")


def delete_file():
    try:
        read_file_and_folder()
        file_name = input("Enter file name: ")
        p = Path(file_name)

        if p.exists() and p.is_file():
            p.unlink()
            print("FILE DELETED SUCCESSFULLY")
        else:
            print("FILE DOES NOT EXIST")
    except Exception as err:
        print(f"An error occurred: {err}")


try:
    user_choice = int(input(
        "Choose the number you want to implement:\n"
        "1: Create file\n"
        "2: Add data in file\n"
        "3: Read file\n"
        "4: Delete file\n"
        ": "
    ))

    if user_choice == 1:
        create_file()
    elif user_choice == 2:
        append_file()
    elif user_choice == 3:
        read_file()
    elif user_choice == 4:
        delete_file()
    else:
        print("Invalid choice")
except ValueError as err:
    print(f"Please enter a valid number ")