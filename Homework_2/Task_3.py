import os

PATH = os.getcwd()
directories = list(filter(os.path.isdir, os.listdir(PATH)))  # Reading all directories in PATH
FILE_NAME = 'text.txt'

for directory in directories:  # Searching for the directory with files
    if directory == 'files_for_task_3':
        path_to_files = os.path.join(PATH, directory)
        files = os.listdir(path_to_files)  # Reading the names of all files in 'files_for_task_3'

        all_files = {}

        for file in files:  # Recording all files to the dictionary all_files
            path_to_file = os.path.join(path_to_files, file)

            with open(path_to_file, encoding='utf-8') as text:
                all_files[file] = text.readlines()

        sorted_files = sorted(all_files, key=lambda x: len(all_files[x]))  # Sorting all files by their lines

        for file in sorted_files:
            with open('text.txt', 'a') as new_text:
                new_text.write(file + '\n')
                new_text.write(str(len(all_files[file])) + '\n')
                new_text.writelines(all_files[file] + ['\n'])
    else:
        print("Can not find the folder files_for_task_3 with files")
