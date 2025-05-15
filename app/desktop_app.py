import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                             QLineEdit, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
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
            
class RegexGenerator(QMainWindow):
    """Main window for the Regex Generator application"""
    
    def __init__(self):
        super().__init__()
        self.chain = Chain()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("AI Regex Generator")
        self.setMinimumSize(800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)
        
        # Input section
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # Sample text section
        sample_text_label = QLabel("Sample Text:")
        sample_text_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.sample_text_edit = QTextEdit()
        self.sample_text_edit.setPlaceholderText("Enter the text that contains your target value...")
        
        # Target value section
        target_value_label = QLabel("Target Value to Extract:")
        target_value_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.target_value_edit = QLineEdit()
        self.target_value_edit.setPlaceholderText("Enter the specific value you want to extract from the sample text")
        
        # Add to input layout
        input_layout.addWidget(sample_text_label)
        input_layout.addWidget(self.sample_text_edit)
        input_layout.addWidget(target_value_label)
        input_layout.addWidget(self.target_value_edit)
        
        # Output section
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        
        result_label = QLabel("Generated Regex Pattern:")
        result_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setFont(QFont("Courier New", 11))
        
        # Button layout
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate Regex")
        self.generate_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.generate_button.clicked.connect(self.generate_regex)
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all)
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.clear_button)
        
        # Status indicator
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignRight)
        
        # Add to output layout
        output_layout.addWidget(result_label)
        output_layout.addWidget(self.result_edit)
        output_layout.addLayout(button_layout)
        output_layout.addWidget(self.status_label)
        
        # Add widgets to splitter
        splitter.addWidget(input_widget)
        splitter.addWidget(output_widget)
        
        # Set default sizes
        splitter.setSizes([300, 300])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set central widget
        self.setCentralWidget(main_widget)
        
    def generate_regex(self):
        """Handle the generation of regex patterns"""
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
    # Set platform to offscreen if in WSL
    if "WSL" in os.uname().release or "microsoft" in os.uname().release.lower():
        print("WSL detected, using offscreen platform")
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        print("Note: In WSL, the GUI will not be visible.")
        print("This app would normally show a GUI window, but is running in headless mode due to WSL limitations.")
        print("To use the full GUI, please run this application directly in Windows with Python and PyQt installed.")
        
        # Create a simple CLI interface for WSL users
        chain = Chain()
        print("\n=== AI Regex Generator (CLI Mode) ===")
        while True:
            try:
                print("\nEnter sample text (or 'quit' to exit):")
                sample_text = input("> ")
                if sample_text.lower() == 'quit':
                    break
                    
                print("Enter target value to extract:")
                target_value = input("> ")
                
                if target_value not in sample_text:
                    print("Error: Target value not found in sample text.")
                    continue
                    
                print("Generating regex pattern...")
                result = chain.write_regex(sample_text, target_value)
                print("\nGenerated Pattern:")
                print(result)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
        
        return
    
    # Normal GUI mode for non-WSL environments
    app = QApplication(sys.argv)
    window = RegexGenerator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 