"""
AI Desktop GUI - Loads the beautiful HTML interface in a native desktop window
This gives you the EXACT design from your HTML with all the styling
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class AIDesktopWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.setWindowTitle("My AI Desktop")
        self.setGeometry(100, 50, 1400, 900)
        
        # Create web view
        self.browser = QWebEngineView()
        
        # Load the HTML file
        html_path = os.path.join(os.path.dirname(__file__), 'ai_desktop.html')
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
        
        # Set as central widget
        self.setCentralWidget(self.browser)

def main():
    app = QApplication(sys.argv)
    window = AIDesktopWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
