import PySimpleGUI as sg
import os
import string
import shutil

def getAllDrives():
    drives = []
    for drive_letter in string.ascii_uppercase:
        drive_path = drive_letter + ":\\"
        if os.path.exists(drive_path):
            drives.append(drive_path)
    return drives

def getUserAccounts(drive):
    user_accounts = []
    users_path = os.path.join(drive, "Users")

    if os.path.exists(users_path) and os.path.isdir(users_path):
        user_accounts = [folder for folder in os.listdir(users_path) if os.path.isdir(os.path.join(users_path, folder))]

    return user_accounts

def backupUserFolders(source, destination, progress_bar):
    exclude_folders = ["include", ".hidden_folder"]  # Add folders you want to exclude

    try:
        total_items = sum(1 for item in os.listdir(source) if item not in exclude_folders and not item.startswith("."))
        current_item = 0

        for item in os.listdir(source):
            if item not in exclude_folders and not item.startswith("."):
                source_path = os.path.join(source, item)
                destination_path = os.path.join(destination, item)

                if os.path.isdir(source_path):
                    shutil.copytree(source_path, destination_path)
                else:
                    shutil.copy2(source_path, destination_path)

                current_item += 1
                progress_percent = int((current_item / total_items) * 100)
                progress_bar.update(progress_percent)

        print(f"Backup successful. Folders from {source} copied to {destination}")
    except Exception as e:
        print(f"Backup failed: {e}")


def backupWindow():
    currentDrive = "C"
    allDrives = getAllDrives()
    userAccounts = getUserAccounts(currentDrive)
    currentUser = None
    backupDestination = ""

    layout = [[sg.Text('Select   \nDrive'), sg.Listbox(allDrives, size=(20,4), expand_y = True, enable_events=True, key="-LIST-")],
                  [sg.Text('Select\nAccount'), sg.Listbox(userAccounts, size=(20, 4), enable_events=True, key="-ACCOUNTS-")],
                  [sg.Text('Select Backup Destination')],
                  [sg.InputText(key="-FOLDER-"), sg.FolderBrowse()],
                  [sg.Button('OK')],
                  [sg.ProgressBar(100, orientation='h', size=(20, 20), key="-PROGRESS-", visible=False)]]

    window = sg.Window('Backup', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "OK":
            print(currentDrive, currentUser)
            source_folder = os.path.join(currentDrive, "Users", currentUser)
            backup_destination = values["-FOLDER-"]

            progress_bar = window["-PROGRESS-"]

            progress_bar.update(0, visible=True)

            backupUserFolders(source_folder, backup_destination, progress_bar)

            
            progress_bar.update(100, visible=False)

        elif event == "-LIST-":
            selectedDrive = values["-LIST-"][0]
            currentDrive = selectedDrive
            userAccounts = getUserAccounts(currentDrive)
            window["-ACCOUNTS-"].update(values=userAccounts)
        
        elif event == "-ACCOUNTS-":
            selectedUser = values["-ACCOUNTS-"][0]
            currentUser = selectedUser



    window.close()
