import clipboard
import time
import schedule
import threading
import json
import subprocess
from PyHotKey import Key, keyboard_manager as manager
from pystray import Icon, MenuItem, Menu
from PIL import Image



'''
example of exclip.json
--
{
    '；': ';',
    '，': ',',
    '、': ',',
    '。': '.',
    '’': '\'',
    '”': '\"',
    '［': '[',
    '］': ']',
    '〔': '[',
    '〕': ']',
    '〈': '<',
    '〉': '>',
    '（': '(',
    '）': ')'
}
--
'''
conversion_dict = {}
json_filename = 'exclip.json'

class taskTray:
    def __init__(self, image):
        self.status = False

        ## アイコンの画像
        image = Image.open(image)
        ## 右クリックで表示されるメニュー
        menu = Menu(
                    MenuItem('Edit json', self.edit_rcjson),
                    MenuItem('Reload json', self.read_rcjson),
                    MenuItem('Write out to json', self.write_rcjson),
                    MenuItem('Exit', self.stopProgram),
                )

        self.icon = Icon(name="XC", title='exclip', icon=image, menu=menu)

    def edit_rcjson(self):
    #    subprocess.run([r"C:\Windows\notepad.exe",r".\exclip.json"])
        subprocess.run([r"C:\Windows\notepad.exe", json_filename])

    def read_rcjson(self):
        global conversion_dict
        # Opening JSON file
        with open(json_filename, 'r') as openfile:
        # Reading from json file
            conversion_dict = json.load(openfile)

        print(conversion_dict)
        print('reloaded')

    def write_rcjson(self):
        global conversion_dict
        # Serializing json
        print(conversion_dict)
        json_object = json.dumps(conversion_dict, indent=4, ensure_ascii=False)
        # Writing to json file
        with open(json_filename, "w") as outfile:
            outfile.write(json_object)

        print('wrote out')

    def runSchedule(self):
        global conversion_dict
        ## 5秒毎にタスクを実行する。
        ## schedule.every(5).seconds.do(self.doTask)

        ## Register HotKey
        hotkey_id1 = manager.register_hotkey([Key.ctrl_l, 'b'],None,edit_clipb)
        print(manager.hotkeys)

        # Opening json file
        with open(json_filename, 'r') as openfile:
        # Reading from json file
            conversion_dict = json.load(openfile)
        print(conversion_dict)
        
        ## status が True である間実行する。
        while self.status:
            ## schedule.run_pending()
            if manager.running == False:
                # Start keyboard listener
                manager.start()
                # Print keyboard listener's running state
                print(manager.running)

            time.sleep(10)
        else:
            manager.stop()

    def stopProgram(self, icon):
        self.status = False

        ## 停止
        self.icon.stop()

    def runProgram(self):
        self.status = True

        ## スケジュールの実行
        task_thread = threading.Thread(target=self.runSchedule)
        task_thread.start()

        ## 実行
        self.icon.run()

def convert_special_chars(input_string):
    for char, replacement in conversion_dict.items():
        input_string = input_string.replace(char, replacement)
    
    return input_string

def edit_clipb():
    # Get the current clipboard content
    current_clipboard = clipboard.paste()

    # Modify the clipboard content
    modified_clipboard = convert_special_chars(current_clipboard)

    # Set the modified content back to the clipboard
    clipboard.copy(modified_clipboard)

    return

if __name__ == '__main__':
    system_tray = taskTray(image="exclip.ico")
    system_tray.runProgram()
