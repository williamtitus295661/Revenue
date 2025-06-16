from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QSizePolicy
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import sys

# RevenueTotals Class
class RevenueTotals(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Store reference to main window
        self.setWindowTitle("Monthly & Yearly Revenue")
        self.setGeometry(100, 100, 600, 700)

        layout = QVBoxLayout()

        # Year Selection Dropdown
        self.year_selector = QComboBox()
        self.year_selector.addItems([str(y) for y in range(2015, 2026)])
        layout.addWidget(self.year_selector, alignment=Qt.AlignCenter)

        # Yearly Revenue Table (Expanded & Centered)
        self.table_yearly = QTableWidget(12, 2)
        self.table_yearly.setHorizontalHeaderLabels(["Month", "Revenue ($)"])
        self.table_yearly.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_yearly.horizontalHeader().setStretchLastSection(True)
        self.table_yearly.setMinimumHeight(450)  # Increased height
        self.table_yearly.setMinimumWidth(450)
       


        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        for i, month in enumerate(months):
            self.table_yearly.setItem(i, 0, QTableWidgetItem(month))
        layout.addWidget(self.table_yearly, alignment=Qt.AlignCenter)

        # Button Styles
        button_stylesheet = """
            QPushButton {
                background-color: #800080; /* Purple */
                color: white;
                font-size: 18px;
                border-radius: 20px; /* Fully rounded */
                padding: 12px;
                margin: 10px; /* Keeps spacing */
            }
            QPushButton:hover {
                background-color: #4B0082; /* Dark purple hover */
            }
        """

        # Show Graph Button
        self.button_show_graph = QPushButton("Show Graph")
        self.button_show_graph.setFixedWidth(250)
        self.button_show_graph.setStyleSheet(button_stylesheet)
        layout.addWidget(self.button_show_graph, alignment=Qt.AlignCenter)
        self.button_show_graph.clicked.connect(self.compare_years_graph)

        # Back Button
        self.button_back = QPushButton("Back")
        self.button_back.setStyleSheet(button_stylesheet)
        layout.addWidget(self.button_back, alignment=Qt.AlignCenter)
        self.button_back.clicked.connect(self.go_back)

        self.setLayout(layout)

    def paintEvent(self, event):
        """ Ensures red-to-purple gradient is correctly displayed """
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 0, 0))  # Red
        gradient.setColorAt(1, QColor(128, 0, 128))  # Purple
        painter.fillRect(self.rect(), gradient)

        # Ensure window repaints correctly
        self.update()

    def compare_years_graph(self):
        """ Generates a comparison graph for yearly revenue """
        selected_year = self.year_selector.currentText()
        revenue_data = [float(self.table_yearly.item(i, 1).text()) if self.table_yearly.item(i, 1) and self.table_yearly.item(i, 1).text().isdigit() else 0 for i in range(12)]

        months_short = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        plt.figure(figsize=(6, 4))
        plt.plot(months_short, revenue_data, marker='o', linestyle='-', color='blue', label=f"Year {selected_year}")
        plt.xlabel("Months")
        plt.ylabel("Revenue ($)")
        plt.title(f"Revenue Trend for {selected_year}")
        plt.legend()
        plt.show()

    def go_back(self):
        if self.main_window:  # Ensure main window reference exists
            self.close()
            self.main_window.show()
        else:
            print("Error: Main window reference missing!")  # Debugging message

# RevenueCalculator Class
class RevenueCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Revenue Calculator")
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 red, stop:1 purple);")


        layout = QVBoxLayout()

        # Labels and Input Fields
        self.label_fixed = QLabel("Fixed Costs:")
        self.label_fixed.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(self.label_fixed, alignment=Qt.AlignCenter)

        self.entry_fixed = QLineEdit()
        layout.addWidget(self.entry_fixed, alignment=Qt.AlignCenter)

        self.label_amount = QLabel("Amount Made:")
        self.label_amount.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(self.label_amount, alignment=Qt.AlignCenter)

        self.entry_amount = QLineEdit()
        layout.addWidget(self.entry_amount, alignment=Qt.AlignCenter)
        
        # Button Styles
        button_stylesheet = """
            QPushButton {
                background-color: #800080; /* Purple */
                color: white;
                font-size: 18px;
                border-radius: 20px; /* Fully rounded */
                padding: 12px;
                margin: 10px; /* Keeps spacing */
            }
            QPushButton:hover {
                background-color: #4B0082; /* Dark purple hover */
            }
        """
        

        # Calculate Revenue Button
        self.button_calculate = QPushButton("Calculate Revenue")
        self.button_calculate.setFixedWidth(250)
        self.button_calculate.setStyleSheet(button_stylesheet)
        layout.addWidget(self.button_calculate, alignment=Qt.AlignCenter)
        self.button_calculate.clicked.connect(self.calculate_revenue)

        # Revenue Totals Page Button
        self.button_totals = QPushButton("Revenue Totals")
        self.button_totals.setFixedWidth(250)
        self.button_totals.setStyleSheet(button_stylesheet)
        layout.addWidget(self.button_totals, alignment=Qt.AlignCenter)
        self.button_totals.clicked.connect(self.open_totals_page)

        # Result Label
        self.label_result = QLabel("Revenue:")
        self.label_result.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(self.label_result, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def calculate_revenue(self):
        try:
            fixed_costs = float(self.entry_fixed.text())
            amount_made = float(self.entry_amount.text())
            revenue = amount_made - fixed_costs
            self.label_result.setText(f"Revenue: ${revenue:.2f}")
        except ValueError:
            self.label_result.setText("Invalid input!")

    def open_totals_page(self):
        """ Opens the revenue totals page """
        self.hide()
        self.totals_page = RevenueTotals(self)  # Pass main window reference
        self.totals_page.show()

# Start application
app = QApplication(sys.argv)
window = RevenueCalculator()
window.show()
sys.exit(app.exec_())











