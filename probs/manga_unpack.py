# File Unpack
from os import listdir, rename, rmdir
from os.path import join
from shutil import move
root_directory = "C:\\Users\\Alex\\Documents"


def extract(base_path):
    for chapter in listdir(base_path):
        print(" ".join(("Access", chapter)))
        sub_path = join(base_path, chapter)
        for image in listdir(sub_path):
            print(" ".join(("Access", image)))
            expanded_name = "-".join((chapter, image))
            expanded_path = join(sub_path, expanded_name)
            rename(join(sub_path, image), join(sub_path, expanded_path))
            print(" ".join(("Expand Name", expanded_name)))
            move(expanded_path, join(base_path, expanded_name))
            print(" ".join(("Move to Parent", expanded_name)))
        rmdir(sub_path)
        print("Remove Chapter Folder")
    print("Finish")


def prompt():
    return str.lower(input("Manga Unpack: "))


if __name__ == "__main__":
    user_response = prompt()
    while user_response != "exit":
        path = join(root_directory, user_response)
        try:
            extract(path)
        except FileNotFoundError:
            print("Invalid File")
        user_response = prompt()
