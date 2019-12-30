import sys
import os
import os.path
import shutil
import filecmp
import difflib

#
# This hook will check to move files/directories from the initial_directory
# to their final location. When the corresponding file at the final location
# already exists and differs from the newly generated version, a diff will
# displayed. Otherwise, if it doesn't exists, the file will simply be moved to
# the final location, or if it does exists, simply be deleted.
#

initial_directory = "__initial"
initial_gradle_directory = "__initial_gradle"
initial_maven_directory = "__initial_maven"

color_green = '\033[92m'
color_yellow = '\033[93m'
color_red = '\033[91m'
reset_color = '\033[0m'


def show_file_diff(file1, file2):
    with open(file1) as fh1:
        file1_lines = fh1.readlines()
    with open(file2) as fh2:
        file2_lines = fh2.readlines()
    diff = difflib.context_diff(file1_lines, file2_lines, file1, file2)
    sys.stdout.writelines(diff)


def print_directory(dirname):
    for f in os.listdir(dirname):
        if os.path.isdir(dirname + "/" + f):
            print_directory(dirname + "/" + f)
        else:
            print("{}New file: {}{}".format(color_green, dirname + "/" + f, reset_color))


def handle_file(dir_prefix, initial_filename):
    final_filename = initial_filename[len(dir_prefix) + 1:]
    if not os.path.exists(final_filename):
        # NEW file or directry: just move it in place.
        shutil.move(initial_filename, final_filename)
        if os.path.isdir(final_filename):
            print_directory(final_filename)
        else:
            print("{}New file: {}{}".format(color_green, final_filename, reset_color))
    elif os.path.isfile(final_filename):
        if filecmp.cmp(initial_filename, final_filename, shallow=False):
            os.unlink(initial_filename)
            print("{}Existing File: {} [Untouched]{}".format(
                color_green, final_filename, reset_color))
        else:
            shutil.move(initial_filename, final_filename)
            print("{}File:{} [Overwritten, please check with 'git diff']{}".format(
                color_yellow, initial_filename, reset_color))
    elif os.path.isdir(final_filename):
        if final_filename == "src":
            # If the src directory already exists in its final location, then
            # we assume there is already an application present and as such
            # the directory can be entirely ignored.
            shutil.rmtree(initial_filename)
        else:
            for f in os.listdir(initial_filename):
                handle_file(dir_prefix, initial_filename + "/" + f)
            shutil.rmtree(initial_filename)
    else:
        print("FILE {} is neither file nor directory... Please check manually.")


def clean_directory(dirname):
    safe_to_remove_directory = True
    # for f in os.listdir(dirname):
    #     if os.path.isdir(dirname + "/" + f):
    #         clean_directory(dirname + "/" + f)
    #     else:
    #         safe_to_remove_directory = False
    if safe_to_remove_directory:
        os.rmdir(dirname)


def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


if __name__ == "__main__":
    if "{{cookiecutter.build_automation_tool}}" == "Gradle":
        remove(initial_maven_directory)
        for f in os.listdir(initial_gradle_directory):
            handle_file(initial_gradle_directory, initial_gradle_directory + "/" + f)
        clean_directory(initial_gradle_directory)
    elif "{{cookiecutter.build_automation_tool}}" == "Maven":
        remove(initial_gradle_directory)
        for f in os.listdir(initial_maven_directory):
            handle_file(initial_maven_directory, initial_maven_directory + "/" + f)
        clean_directory(initial_maven_directory)

    for f in os.listdir(initial_directory):
        handle_file(initial_directory, initial_directory + "/" + f)
    clean_directory(initial_directory)

    # if os.path.exists(initial_directory) or os.path.exists(initial_gradle_directory) or os.path.exists(initial_maven_directory):
    #     print("\n  1 or more files have been changed. Please merge changes manually!\n")
