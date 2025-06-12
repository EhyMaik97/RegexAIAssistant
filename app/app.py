import sys
import os
import warnings


from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                             QLineEdit, QMessageBox, QSplitter, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor
from dotenv import load_dotenv, find_dotenv, set_key

# Add support for PyInstaller packaged app
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Import chains only after setting up resource path
# This prevents import errors when running as executable
sys.path.insert(0, resource_path("app"))
from chains import Chain

class RegexGeneratorThread(QThread):
    """Thread to handle regex generation without blocking the UI"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, chain, sample_text, target_value):
        super().__init__()
        self.chain = chain
        self.sample_text = sample_text
        self.target_value = target_value
        
    def run(self):
        try:
            result = self.chain.write_regex(self.sample_text, self.target_value)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class ModernFrame(QFrame):
    """Custom frame with modern styling"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernFrame")
        self.setStyleSheet("""
            #modernFrame {
                background-color: #2D2D30;
                border-radius: 8px;
                border: 1px solid #3E3E42;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
            
class RegexGenerator(QMainWindow):
    """Main window for the Regex Generator application"""
    
    def __init__(self):
        super().__init__()
        self.chain = None
        self.apply_dark_theme()
        self.set_application_icon()
        self.init_ui()
        self.check_api_key()
        
    def set_application_icon(self):
        """Set the application icon from assets folder"""
        icon_path = resource_path(os.path.join("assets", "app_icon.ico"))
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
        
    def check_api_key(self):
        """Check if API key is set and prompt user if not"""
        # Try loading from .env again just to be sure
        dotenv_path = find_dotenv(usecwd=True)
        load_dotenv(dotenv_path)
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            self.status_label.setText("API Key not found")
            
            dialog = QMessageBox(self)
            dialog.setWindowTitle("API Key Required")
            dialog.setText("GROQ API Key is required to generate regex patterns.")
            dialog.setInformativeText("Please enter your GROQ API Key:")
            
            # Add input field
            text_input = QLineEdit(dialog)
            text_input.setEchoMode(QLineEdit.Password)
            text_input.setMinimumWidth(300)
            
            # Add layout for better appearance
            layout = dialog.layout()
            if layout is not None:
                layout.addWidget(text_input, 1, 0, 1, layout.columnCount())
            
            dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            result = dialog.exec_()
            
            if result == QMessageBox.Ok:
                new_api_key = text_input.text().strip()
                if new_api_key:
                    # Save to .env file if it exists
                    if dotenv_path:
                        set_key(dotenv_path, "GROQ_API_KEY", new_api_key)
                    # Also set in environment
                    os.environ["GROQ_API_KEY"] = new_api_key
                    self.status_label.setText("API Key saved")
                    self.chain = Chain()
                else:
                    QMessageBox.warning(self, "No API Key", "No API key was provided. The application may not function correctly.")
            else:
                QMessageBox.warning(self, "No API Key", "No API key was provided. The application may not function correctly.")
        else:
            self.chain = Chain()
        
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QWidget {
                color: #E0E0E0;
                background-color: #1E1E1E;
            }
            QTextEdit, QLineEdit {
                background-color: #252526;
                border: 1px solid #3E3E42;
                border-radius: 4px;
                padding: 8px;
                color: #E0E0E0;
                selection-background-color: #264F78;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1C8AE6;
            }
            QPushButton:pressed {
                background-color: #00569C;
            }
            QPushButton:disabled {
                background-color: #3E3E42;
                color: #9D9D9D;
            }
            QSplitter::handle {
                background-color: #3E3E42;
            }
            QSplitter::handle:horizontal {
                width: 2px;
            }
            QSplitter::handle:vertical {
                height: 2px;
            }
            QLabel {
                color: #E0E0E0;
            }
        """)
        
    def init_ui(self):
        self.setWindowTitle("AI Regex Generator")
        self.setMinimumSize(900, 700)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # App title
        title_label = QLabel("AI Regex Generator")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #0078D7; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(8)
        splitter.setChildrenCollapsible(False)
        
        # Input section
        input_frame = ModernFrame()
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(20, 20, 20, 20)
        input_layout.setSpacing(15)
        
        # Sample text section
        sample_text_label = QLabel("Sample Text")
        sample_text_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.sample_text_edit = QTextEdit()
        self.sample_text_edit.setPlaceholderText("Enter the text that contains your target value...")
        self.sample_text_edit.setMinimumHeight(120)
        self.sample_text_edit.setFont(QFont("Consolas", 11))
        
        # Target value section
        target_value_label = QLabel("Target Value to Extract")
        target_value_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.target_value_edit = QLineEdit()
        self.target_value_edit.setPlaceholderText("Enter the specific value you want to extract from the sample text")
        self.target_value_edit.setFont(QFont("Consolas", 11))
        
        # Add to input layout
        input_layout.addWidget(sample_text_label)
        input_layout.addWidget(self.sample_text_edit)
        input_layout.addWidget(target_value_label)
        input_layout.addWidget(self.target_value_edit)
        
        # Output section
        output_frame = ModernFrame()
        output_layout = QVBoxLayout(output_frame)
        output_layout.setContentsMargins(20, 20, 20, 20)
        output_layout.setSpacing(15)
        
        result_label = QLabel("Generated Regex Pattern")
        result_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setFont(QFont("Consolas", 12))
        self.result_edit.setStyleSheet("""
            background-color: #202020;
            border: 1px solid #3E3E42;
            border-radius: 4px;
            padding: 10px;
        """)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.generate_button = QPushButton("Generate Regex")
        self.generate_button.setFont(QFont("Segoe UI", 10))
        self.generate_button.setMinimumHeight(40)
        self.generate_button.clicked.connect(self.generate_regex)
        self.generate_button.setIcon(QIcon.fromTheme("system-run"))
        
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setFont(QFont("Segoe UI", 10))
        self.copy_button.setMinimumHeight(40)
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setIcon(QIcon.fromTheme("edit-copy"))
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.setFont(QFont("Segoe UI", 10))
        self.clear_button.setMinimumHeight(40)
        self.clear_button.clicked.connect(self.clear_all)
        self.clear_button.setStyleSheet("""
            background-color: #484848;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
        """)
        self.clear_button.setIcon(QIcon.fromTheme("edit-clear"))
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.clear_button)
        
        # Status indicator
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignRight)
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #999999;")
        
        # Add to output layout
        output_layout.addWidget(result_label)
        output_layout.addWidget(self.result_edit)
        output_layout.addLayout(button_layout)
        output_layout.addWidget(self.status_label)
        
        # Add widgets to splitter
        splitter.addWidget(input_frame)
        splitter.addWidget(output_frame)
        
        # Set default sizes
        splitter.setSizes([350, 350])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set central widget
        self.setCentralWidget(main_widget)
        
    def generate_regex(self):
        """Handle the generation of regex patterns"""
        # Check if chain is available
        if self.chain is None:
            QMessageBox.critical(self, "API Key Missing", 
                               "Cannot generate regex pattern without a valid API key. Please restart the application and provide a valid API key.")
            self.check_api_key()
            return
            
        sample_text = self.sample_text_edit.toPlainText().strip()
        target_value = self.target_value_edit.text().strip()
        
        if not sample_text:
            QMessageBox.warning(self, "Missing Input", "Please enter sample text.")
            return
            
        if not target_value:
            QMessageBox.warning(self, "Missing Input", "Please enter a target value to extract.")
            return
            
        if target_value not in sample_text:
            QMessageBox.warning(self, "Value Not Found", 
                               "The target value doesn't appear in the sample text. Please check your input.")
            return
            
        # Disable button and show status
        self.generate_button.setEnabled(False)
        self.status_label.setText("Generating regex pattern...")
        
        # Create and start the worker thread
        self.thread = RegexGeneratorThread(self.chain, sample_text, target_value)
        self.thread.finished.connect(self.handle_result)
        self.thread.error.connect(self.handle_error)
        self.thread.start()
        
    def handle_result(self, result):
        """Handle the result returned by the worker thread"""
        self.result_edit.setText(result)
        self.status_label.setText("Regex pattern generated!")
        self.generate_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        
    def handle_error(self, error_message):
        """Handle errors from the worker thread"""
        QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")
        self.status_label.setText("Ready")
        self.generate_button.setEnabled(True)
        
    def copy_to_clipboard(self):
        """Copy the generated regex to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_edit.toPlainText())
        self.status_label.setText("Copied to clipboard!")
        
    def clear_all(self):
        """Clear all input and output fields"""
        self.sample_text_edit.clear()
        self.target_value_edit.clear()
        self.result_edit.clear()
        self.status_label.setText("Ready")
        self.copy_button.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    
    # Set application icon
    icon_path = resource_path(os.path.join("assets", "app_icon.ico"))
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    
    window = RegexGenerator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 