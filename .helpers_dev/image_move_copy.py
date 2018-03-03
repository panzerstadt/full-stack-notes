import os

temp = list(os.walk('../data'))
destination_folder = '../static/images'

image_filepaths = []
for group in temp:
    check = os.path.basename(group[0])
    if 'images' in check:
        for file in group[2]:
            image_filepaths.append(os.path.join(group[0], file))

print('images found: ')
[print(file) for file in image_filepaths]

answer = input('\nwhat do you want to do with these files? (move/copy)')

if 'move' in answer:
    if 'yes' in input("\nare you sure you want to move these files to {0}? (yes/no)".format(destination_folder)).lower():
        for file in image_filepaths:
            destination_path = os.path.join(destination_folder, os.path.basename(file))
            os.rename(file, destination_path)
            print('renamed {0}  -->  {1}'.format(file, destination_path))

if 'copy' in answer:
    if 'yes' in input("\nare you sure you want to copy these files to {0}? (yes/no)".format(destination_folder)).lower():
        from shutil import copyfile
        for file in image_filepaths:
            destination_path = os.path.join(destination_folder, os.path.basename(file))
            copyfile(file, destination_path)
            print('copied {0}  -->  {1}'.format(file, destination_path))