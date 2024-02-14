from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

import configparser
Config = configparser.ConfigParser()
Config.read('src\config.ini')

class KeyCaptureDialog(QDialog):
    def __init__(self, parent=None):
        super(KeyCaptureDialog, self).__init__(parent)
        self.setWindowTitle('Press a Key')
        self.key = None  # To store the pressed key
        layout = QVBoxLayout()
        self.label = QLabel("Press any key to assign it for screen capture.\nPress ESC to cancel.")
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.keylist = []
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # If ESC is pressed, close the dialog without saving a key
            self.close()
            return

        # Use the modified keyevent_to_string to handle the conversion.
        key_str = keyevent_to_string(event)

        # Check if the event is a combination (contains a modifier and another key).
        if '+' in key_str:
            # This is a combination; check if the last entry in keylist is part of this combination.
            if self.keylist and any(modifier in key_str for modifier in modmap.values()):
                # If the last key in keylist is a modifier of the current combination, remove it.
                last_key = self.keylist[-1]
                if any(modifier == last_key for modifier in modmap.values()):
                   self.keylist.pop()

        # Append the current key or combination to keylist if not already included.
        if not key_str in self.keylist:
            self.keylist.append(key_str)
            print("appended ", key_str)

        self.firstrelease = True


    def keyReleaseEvent(self, event):
        if self.firstrelease == True: 
            keystr = self.processmultikeys(self.keylist)
            self.key = keystr
            self.accept()

        self.firstrelease = False

        del self.keylist[-1]

    def processmultikeys(self,keyspressed):
        keylist = ""
        for i in range(len(keyspressed)):
            keylist += keyspressed[i]
            if(i != len(keyspressed) -1):
                keylist += "+"
        print("in process", keylist)
        return keylist
        
keymap = {}
for key, value in vars(Qt).items():
    if isinstance(value, Qt.Key):
        keymap[value] = key.partition('_')[2]

modmap = {
    Qt.ControlModifier: keymap[Qt.Key_Control],
    Qt.AltModifier: keymap[Qt.Key_Alt],
    Qt.ShiftModifier: keymap[Qt.Key_Shift],
    Qt.MetaModifier: keymap[Qt.Key_Meta],
    Qt.GroupSwitchModifier: keymap[Qt.Key_AltGr],
    Qt.KeypadModifier: keymap[Qt.Key_NumLock],
    }

def keyevent_to_string(event):
    sequence = []
    for modifier, text in modmap.items():
        if event.modifiers() & modifier:
            sequence.append(text)
    key = keymap.get(event.key(), event.text())
    if key not in sequence:
        sequence.append(key)
    return '+'.join(sequence)

def assign_key(callback=None):
    dialog = KeyCaptureDialog()
    if dialog.exec_() == QDialog.Accepted and dialog.key:
        print("saved", dialog.key)
        saveKey(dialog.key)  # Save the captured key
        Config.write(open("src\config.ini", "w"))  # Save changes to config file
    if callback:
        callback()

def saveKey(key):
    key = convert_to_qkeysequence_format(key)
    Config.set('CaptureKey', 'Key', key)

def convert_to_qkeysequence_format(key_sequence):
    # Mapping from the saved format to QKeySequence format
    replacements = {
        'Control': 'Ctrl',
        'Alt': 'Alt',
        'Shift': 'Shift',
        'Meta': 'Meta'
    }
    for key, replacement in replacements.items():
        key_sequence = key_sequence.replace(key, replacement)
    return key_sequence