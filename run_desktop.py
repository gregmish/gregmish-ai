"""
Simple Desktop App - Just opens your HTML in a clean window
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl

app = QApplication(sys.argv)

# Create window
window = QMainWindow()
window.setWindowTitle("My AI Desktop")
window.setGeometry(100, 50, 1400, 900)

# Create browser
browser = QWebEngineView()

# Enable local storage and other features
settings = browser.settings()
settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

# Load HTML
html_file = os.path.abspath("ai_desktop.html")
browser.setUrl(QUrl.fromLocalFile(html_file))

# Show
window.setCentralWidget(browser)
window.show()

sys.exit(app.exec_())
