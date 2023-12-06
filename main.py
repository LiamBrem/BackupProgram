import PySimpleGUI as sg
import backup


sg.theme = 'DarkAmber'

layout = [  [sg.Text('Backup or Restore Data')],
            [sg.Button("Backup")],
            [sg.Button('Restore')],
            [sg.Button("Transfer")] ]



# Create the Window
window = sg.Window('Backup', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == "Backup":
        print("backup")
        window.close()
        backup.backupWindow()
    elif event == "Restore":
        print("restore")
    elif event == "Transfer":
        print("transfer")
    
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break


window.close()
