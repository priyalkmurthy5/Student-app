from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QListWidget, QMessageBox
import sys
import sqlite3

conn = sqlite3.connect('project4db.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS student (
    studentid INTEGER PRIMARY KEY,
    studentname TEXT,
    studentscore INTEGER
)
''')

conn.commit()
conn.close()

class StudentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("StudentApp")
        self.setGeometry(100, 100, 600, 400)

        # Create tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Student Info")
        self.tabs.addTab(self.tab2, "Student Grade")

        self.tab1UI()
        self.tab2UI()

        self.setCentralWidget(self.tabs)

    def tab1UI(self):
        layout = QVBoxLayout()

        # Student Info inputs
        self.id_label = QLabel("Student ID:")
        self.id_input = QLineEdit()
        self.name_label = QLabel("Student Name:")
        self.name_input = QLineEdit()
        self.score_label = QLabel("Student Score:")
        self.score_input = QLineEdit()

        # Buttons
        self.display_btn = QPushButton("Display Data")
        self.insert_btn = QPushButton("Insert Data")
        self.display_btn.clicked.connect(self.displayData)
        self.insert_btn.clicked.connect(self.insertData)

        # DataGridView
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Score"])

        # Layout arrangement
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.score_label)
        layout.addWidget(self.score_input)
        layout.addWidget(self.display_btn)
        layout.addWidget(self.insert_btn)
        layout.addWidget(self.table)

        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QVBoxLayout()

        # List box
        self.listbox = QListWidget()
        self.tabs.currentChanged.connect(self.showGrades)

        # Export button
        self.export_btn = QPushButton("Export Data")
        self.export_btn.clicked.connect(self.exportData)

        # Layout arrangement
        layout.addWidget(self.listbox)
        layout.addWidget(self.export_btn)

        self.tab2.setLayout(layout)

    def displayData(self):
        conn = sqlite3.connect('project4db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        conn.close()

    def insertData(self):
        student_id = self.id_input.text()
        student_name = self.name_input.text()
        student_score = self.score_input.text()

        if not student_id or not student_name or not student_score:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out")
            return

        try:
            student_id = int(student_id)
            student_score = int(student_score)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "ID and Score must be integers")
            return

        conn = sqlite3.connect('project4db.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO student (studentid, studentname, studentscore) VALUES (?, ?, ?)", (student_id, student_name, student_score))
            conn.commit()
            QMessageBox.information(self, "Success", "Data inserted successfully")
            self.id_input.clear()
            self.name_input.clear()
            self.score_input.clear()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Input Error", "Student ID already exists")

        conn.close()

    def showGrades(self):
        if self.tabs.currentIndex() == 1:
            conn = sqlite3.connect('project4db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student")
            rows = cursor.fetchall()
            self.listbox.clear()

            for row in rows:
                student_id, student_name, student_score = row
                if student_score < 60:
                    grade = 'F'
                elif 60 <= student_score < 70:
                    grade = 'D'
                elif 70 <= student_score < 80:
                    grade = 'C'
                elif 80 <= student_score < 90:
                    grade = 'B'
                else:
                    grade = 'A'
                self.listbox.addItem(f"{student_id} - {student_name} - {grade}")

            conn.close()

    def exportData(self):
        conn = sqlite3.connect('project4db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()

        with open('studentgrades.txt', 'w') as f:
            for row in rows:
                student_id, student_name, student_score = row
                if student_score < 60:
                    grade = 'F'
                elif 60 <= student_score < 70:
                    grade = 'D'
                elif 70 <= student_score < 80:
                    grade = 'C'
                elif 80 <= student_score < 90:
                    grade = 'B'
                else:
                    grade = 'A'
                f.write(f"{student_id}, {student_name}, {grade}\n")

        QMessageBox.information(self, "Success", "Data exported successfully")
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StudentApp()
    ex.show()
    sys.exit(app.exec_())
