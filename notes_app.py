import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QTextEdit, QListWidget, QFrame, QDateTimeEdit, QInputDialog, QLineEdit, QColorDialog, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QDateTime

class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.notes = []
        self.selected_note_index = -1

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Notes App")
        self.setGeometry(100, 100, 800, 600)

        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()

        self.setup_left_panel()
        self.setup_right_panel()

        self.layout.addWidget(self.left_panel)
        self.layout.addWidget(self.right_panel)

        self.central_widget.setLayout(self.layout)

    def setup_left_panel(self):
        self.left_panel = QFrame()
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignTop)
        self.left_panel.setFrameShape(QFrame.StyledPanel)

        # Create labels, text edit, and buttons for the left panel
        self.note_label = QLabel("Take a note:")
        self.note_entry = QTextEdit()
        self.setup_text_edit_style(self.note_entry)

        self.reminder_label = QLabel("Set a Reminder:")
        self.reminder_datetime = QDateTimeEdit()
        self.reminder_datetime.setDateTime(QDateTime.currentDateTime())

        self.add_button = QPushButton("Add Note")
        self.setup_button_style(self.add_button)
        self.add_button.clicked.connect(self.add_note)

        self.color_label = QLabel("Change Note Color:")
        self.color_button = QPushButton("Choose Color")
        self.setup_button_style(self.color_button)
        self.color_button.clicked.connect(self.change_color)

        # Add widgets to the left layout
        self.left_layout.addWidget(self.note_label)
        self.left_layout.addWidget(self.note_entry)
        self.left_layout.addWidget(self.reminder_label)
        self.left_layout.addWidget(self.reminder_datetime)
        self.left_layout.addWidget(self.add_button)
        self.left_layout.addWidget(self.color_label)
        self.left_layout.addWidget(self.color_button)
        self.left_panel.setLayout(self.left_layout)

    def setup_right_panel(self):
        self.right_panel = QFrame()
        self.right_layout = QVBoxLayout()
        self.right_panel.setFrameShape(QFrame.StyledPanel)

        # Create list widget and buttons for the right panel
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.select_note)

        self.edit_button = QPushButton("Edit Note")
        self.setup_button_style(self.edit_button)
        self.edit_button.clicked.connect(self.edit_note)

        self.delete_button = QPushButton("Delete Note")
        self.setup_button_style(self.delete_button)
        self.delete_button.clicked.connect(self.delete_note)

        # Add widgets to the right layout
        self.right_layout.addWidget(self.notes_list)
        self.right_layout.addWidget(self.edit_button)
        self.right_layout.addWidget(self.delete_button)
        self.right_panel.setLayout(self.right_layout)

    def setup_text_edit_style(self, text_edit):
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                padding: 8px;
            }
        """)

    def setup_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: #ffffff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

    def add_note(self):
        # Get note and reminder input
        note = self.note_entry.toPlainText()
        reminder_datetime = self.reminder_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        if note:
            # Get selected color for note
            color = self.color_button.palette().color(self.color_button.backgroundRole())
            self.notes.append({"note": note, "reminder": reminder_datetime, "color": color})
            self.note_entry.clear()
            self.update_notes_list()

    def update_notes_list(self):
        self.notes_list.clear()
        for note_data in self.notes:
            note = note_data["note"]
            reminder = note_data["reminder"]
            color = note_data["color"]
            # Display note with formatted text and color
            self.notes_list.addItem(f"Note: {note}\nReminder: {reminder}")
            self.notes_list.item(self.notes_list.count() - 1).setBackground(color)

    def select_note(self, item):
        self.selected_note_index = self.notes_list.indexFromItem(item).row()

    def edit_note(self):
        if self.selected_note_index >= 0:
            current_note_data = self.notes[self.selected_note_index]
            new_note, ok = QInputDialog.getText(self, "Edit Note", "Edit your note:", QLineEdit.Normal, current_note_data["note"])
            if ok and new_note:
                self.notes[self.selected_note_index]["note"] = new_note
                self.update_notes_list()

    def delete_note(self):
        if self.selected_note_index >= 0:
            del self.notes[self.selected_note_index]
            self.selected_note_index = -1
            self.update_notes_list()

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
            self.color_button.setAutoFillBackground(True)

def main():
    app = QApplication(sys.argv)
    notes_app = NotesApp()
    notes_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
