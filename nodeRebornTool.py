import hou
import os
import sys
import json
import subprocess
from PySide2 import QtCore, QtWidgets, QtGui

class nodeReborn(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Node Reborn_v1.0.0")
        self.setGeometry(300, 300, 450, 700)
        self.setFixedSize(450, 700)

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint 
                            | QtCore.Qt.WindowStaysOnTopHint)

        self.build_layout()

        # Load the JSON file with the list of nodes
        self.loadListNodes()
        # Update the buttons disenabled state or enabled state
        self.update_buttons()

    def build_layout(self):
        # Build General layout
        self.lyt = QtWidgets.QVBoxLayout()
        self.setLayout(self.lyt)

        # Set Label tool name
        label = QtWidgets.QLabel("Node Reborn_v1.0.0")
        self.lyt.addWidget(label)

        # Add the method horizontalButtonLayout, Contains horizontal buttons
        self.horizontalButtonLayout()

        # Add a ComboBox to filter the list by type
        self.menu = QtWidgets.QComboBox()
        menu_items = ["All", "Top", "Vop", "Chop", "Shop", "Driver",
                      "Sop", "Cop2", "Object", "Dop"]
        self.menu.addItems(menu_items)
        self.menu.currentIndexChanged.connect(self.comboBoxFilter)
        self.lyt.addWidget(self.menu)

        # Create the list widget, it will show the list of nodes
        self.list_widget = QtWidgets.QListWidget()
        self.lyt.addWidget(self.list_widget)
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list_widget.itemChanged.connect(self.update_buttons)

        # Add a QlineEdit to search nodes
        self.field = QtWidgets.QLineEdit()
        self.field.setPlaceholderText("Search nodes...")
        self.field.textChanged.connect(self.qlineEditFilter)
        self.lyt.addWidget(self.field)

        # Create the reborn button
        self.reborn_button = QtWidgets.QPushButton("REBORN THE NODE!!")
        self.reborn_button.setEnabled(False)
        self.reborn_button.clicked.connect(self.reborn_selected_node)  
        self.lyt.addWidget(self.reborn_button)

        # Add credits
        githubLink = '<a style="color: gray;" href= "https://github.com/DanteVFX">Coded by DanteVFX</a>'
        self.credits = QtWidgets.QLabel(githubLink)
        self.credits.setOpenExternalLinks(True)
        
        self.credits.setAlignment(QtCore.Qt.AlignRight)
        self.lyt.addWidget(self.credits)

    def horizontalButtonLayout(self):
        grpbox = QtWidgets.QGroupBox()
        self.lyt.addWidget(grpbox)

        # Create an horizontal layout
        hlyt = QtWidgets.QHBoxLayout()
        grpbox.setLayout(hlyt)

        # Create Button Show Hidden Nodes
        self.button = QtWidgets.QPushButton("Show Hidden Nodes")
        self.button.clicked.connect(self.runCommandHscript)
        hlyt.addWidget(self.button)

        # Create Button Clean List
        self.button2 = QtWidgets.QPushButton("Clean List")
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.clean_list)
        hlyt.addWidget(self.button2)

    def runCommandHscript(self):
        #it send a command to hscript
        command = ['hscript', '-c', 'opunhide']
        self.thread = CommandRunner(command)
        self.thread.result_ready.connect(self.updateListWidget)
        self.thread.start()

    # To avoid click multiple times the button show hidden nodes, it saves the list in a JSON file
    def saveListNodes(self, filename="nodes.json"):
        nodes = [self.list_widget.item(index).text() for index in range(self.list_widget.count())]
        with open(filename, "w") as file:
            json.dump(nodes, file)

    # Load the JSON file with the list of nodes
    def loadListNodes(self, filename="nodes.json"):
        try:
            with open(filename, "r") as file:
                nodes = json.load(file)
                for node in nodes:
                    self.list_widget.addItem(node)
                return nodes
        except FileNotFoundError:
            return []

    def updateListWidget(self, stdout, stderr):
        self.list_widget.clear()
        if stderr:
            self.list_widget.addItem(f"Error: {stderr}")
        else:
            lines = stdout.splitlines()
            if lines:
                # Remove the first element if it starts with 'hbatch'
                if lines[0].startswith("hbatch"):
                    lines.pop(0)
                for line in lines:
                    line = line.replace("ophide", "").strip()
                    self.list_widget.addItem(line)
        self.saveListNodes()  # Save the list after updating
        self.update_buttons()

    def clean_list(self):
        self.list_widget.clear()
        # Remove the JSON file when the list is cleaned
        if os.path.exists("nodes.json"):
            os.remove("nodes.json")
        self.update_buttons()

    def update_buttons(self):  # Modificar la función update_buttons
        has_items = self.list_widget.count() > 0
        json_exists = os.path.exists("nodes.json")

        # Disable the button SHOW HIDDEN NODES if the JSON file exists
        self.button.setEnabled(not json_exists)  

        # Disable the button CLEAN LIST if the list is empty or the JSON file doesn't exist
        self.button2.setEnabled(json_exists)  

        # Enable the button REBORN NODES if the list is not empty
        self.reborn_button.setEnabled(has_items)

    def comboBoxFilter(self):
        #this method filter the list by type using the ComboBox
        filter_text = self.menu.currentText()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if filter_text == "All" or item.text().startswith(filter_text):
                item.setHidden(False)
            else:
                item.setHidden(True)

    def qlineEditFilter(self):
        #this method filter the list by name using the QLineEdit
        filter_text = self.field.text()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if filter_text in item.text():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def reborn_selected_node(self):
        #this method send the selected node name from the list to hscript
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_node_name = selected_items[0].text()
            hscript_command = f'opunhide {selected_node_name}'
            hou.hscript(hscript_command) 

    def openLink(self, url):
        #this method open the Github link in the default browser
        QtCore.QDesktopServices.openUrl(QtCore.QUrl(url))

     
       
            
class CommandRunner(QtCore.QThread):
    result_ready = QtCore.Signal(str, str)

    def __init__(self, command):
        super().__init__()
        self.command = command
    #this method run the hscript command in the background to avoid crahsing the UI
    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout_decoded = stdout.decode()
        stderr_decoded = stderr.decode()
        self.result_ready.emit(stdout_decoded, stderr_decoded)


ui = nodeReborn()
ui.show()
