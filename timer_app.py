from errno import ENOTCONN
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# documentation for the imports:
# 1. sys : provides access to command line arguments and system-specific functionality
# 2. QApplication : the main application class for creating a PyQt6 application
# 3. QMainWindow : the main window class for creating a PyQt6 application
# 4. QWidget : the base class for all UI widgets
# 5. QVBoxLayout : a vertical box layout for arranging widgets vertically
# 6. QLabel : a label widget for displaying text
# 7. Qt : contants, alignement etc 
# 8. QFont : a font class for setting font properties


class DigitalTimerApp(QMainWindow): #this class inherits from QMainWindow
    def __init__(self): #this is the constructor for the class
        super().__init__() #this calls the constructor of the parent class
        self.init_ui() #this calls the init_ui method 

    def init_ui(self):
        self.setWindowTitle('Digital Timer') #this sets the title of the window

        #create centre widget and layout
        central_widget = QWidget() # creates an empty widget container for the main window
        self.setCentralWidget(central_widget) #makes it the main content area of the window
        layout = QVBoxLayout() # creates a vertical layout (stacks widget top to bottom)
        central_widget.setLayout(layout) #attaches the layout to the central widget

        #add a test label
        test_label = QLabel('Hello, World!')
        layout.addWidget(test_label)

        self.setGeometry(100, 100, 300, 400) #sets to  position(x,y) and size(width,height)

def main(): #this is the main function that creates the application and starts the event loop
    app=QApplication(sys.argv) #creates an instance of the QApplication class
    window=DigitalTimerApp() #creates the main window object
    window.show() #displays the window
    sys.exit(app.exec()) #starts the event loop and waits for the application to close

if __name__ == '__main__': #this is the entry point of the program
    main() #Runs main() only if script is executed directly (not imported)