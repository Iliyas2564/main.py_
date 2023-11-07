from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem
import pickle

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        self.setFixedSize(444, 347)
        self.setWindowTitle("Joga bonito")

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the vertical layout for the central widget
        central_layout = QVBoxLayout(central_widget)
        central_layout.addStretch(5)

        # Create a horizontal layout for the "Load" and "Save" buttons
        load_save_layout = QHBoxLayout()

        # Create the "Load" button
        self.loadButton = QToolButton(self)
        self.loadButton.setText("Load")
        self.loadButton.setFixedSize(211, 41)
        load_save_layout.addWidget(self.loadButton)

        # Create the "Save" button
        self.saveButton = QToolButton(self)
        self.saveButton.setText("Save")
        self.saveButton.setFixedSize(211, 41)
        load_save_layout.addWidget(self.saveButton)

        # Add the load_save_layout to the central layout
        central_layout.addLayout(load_save_layout)

        # Create the list widget
        self.listView = QListWidget(self)
        self.listView.setFixedSize(421, 231)
        central_layout.addWidget(self.listView)
        central_layout.addStretch(5)

        # Create the horizontal layout for the "Add" and "Delete" buttons
        buttons_layout = QHBoxLayout()
        central_layout.addStretch(5)

        # Create the "Add item to list" button
        self.plusButton = QToolButton(self)
        self.plusButton.setText("Add item to list")
        self.plusButton.setFixedSize(211, 41)
        buttons_layout.addWidget(self.plusButton)
        buttons_layout.addSpacing(0)

        # Create the "Delete item from list" button
        self.minusButton = QPushButton("Delete item from list", self)
        self.minusButton.setFixedSize(211, 41)
        buttons_layout.addWidget(self.minusButton)
        central_layout.addStretch(5)

        # Add the buttons layout to the central layout
        central_layout.addLayout(buttons_layout)

        # Connect button signals to functions
        self.plusButton.clicked.connect(self.add_todo)
        self.minusButton.clicked.connect(self.remove_todo)
        self.loadButton.clicked.connect(self.open_file)
        self.saveButton.clicked.connect(self.save_file)

    def add_todo(self):
        # Function to add a new todo item to the list
        todo, confirmed = QInputDialog.getText(self, "Add Todo", "New Todo:", QLineEdit.Normal, "")
        if confirmed and not todo.isspace():
            self.listView.addItem(todo)

    def remove_todo(self):
        # Function to remove selected todo items from the list
        selected_items = self.listView.selectedItems()
        for item in selected_items:
            self.listView.takeItem(self.listView.row(item))

    def save_file(self):
        # Function to save the current todo list to a file
        item_list = [self.listView.item(i).text() for i in range(self.listView.count())]
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Allow existing files to be read-only
        options |= QFileDialog.DontUseNativeDialog  # Use PyQt's file dialog

        file_dialog = QFileDialog(self)
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Todo Files (*.todo)")
        file_dialog.setDefaultSuffix("todo")

        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, "wb") as f:
                pickle.dump(item_list, f)

    def open_file(self):
        # Function to open a previously saved todo list from a file
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Todo Files (*.todo)", options=options)
        if filename:
            with open(filename, "rb") as f:
                item_list = pickle.load(f)
                self.listView.clear()
                self.listView.addItems(item_list)

if __name__ == "__main__":
    app = QApplication([])
    window = MyGUI()
    window.show()
    app.exec_()
