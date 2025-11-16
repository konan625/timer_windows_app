from errno import ENOTCONN
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# documentation for the imports:
# 1. sys : provides access to command line arguments and system-specific functionality
# 2. QApplication : the main application class for creating a PyQt6 application
# 3. QMainWindow : the main window class for creating a PyQt6 application
# 4. QWidget : the base class for all UI widgets
# 5. QVBoxLayout : a vertical box layout for arranging widgets vertically
# 6. QLabel : a label widget for displaying text
# 7. Qt : contants, alignement etc
# 8. QTimer : a timer class for scheduling timed events
# 8. QFont : a font class for setting font properties
# 9. QPushButton : a button widget for user interaction


class DigitalTimerApp(QMainWindow): #this class inherits from QMainWindow
    def __init__(self): #this is the constructor for the class
        super().__init__() #this calls the constructor of the parent class
        self.elapsed_seconds = 0 #track how many seconds have passed
        self.is_running = False #track if the timer is running
        self.timer = QTimer() #create a timer object
        self.timer.timeout.connect(self.update_stopwatch) #connect the timer to the update function
        self.init_ui() #this calls the init_ui method 

    def init_ui(self):
        self.setWindowTitle('Digital Timer') #this sets the title of the window

        #create centre widget and layout
        central_widget = QWidget() # creates an empty widget container for the main window
        self.setCentralWidget(central_widget) #makes it the main content area of the window
        layout = QVBoxLayout() # creates a vertical layout (stacks widget top to bottom)
        central_widget.setLayout(layout) #attaches the layout to the central widget

        # #add a test label
        # test_label = QLabel('Hello, World!')
        # layout.addWidget(test_label)

        #stopwatch display label
        self.time_label = QLabel('00:00:00')
        self.time_label.setFont(QFont('Consolas', 24, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet('color: #00ff00; background-color: #000000; paddinf: 15px; border-radius: 10px;')
        layout.addWidget(self.time_label)

        #Start/Pause button
        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.toggle_stopwatch)
        layout.addWidget(self.start_btn)

        #Reset button
        self.reset_btn = QPushButton('Reset')
        self.reset_btn.clicked.connect(self.reset_stopwatch)
        layout.addWidget(self.reset_btn)


        self.setGeometry(100, 100, 300, 400) #sets to  position(x,y) and size(width,height)

    def format_time(self, total_seconds):
        """Converts seconds to HH:MM:SS format"""
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_stopwatch(self):
        """Called every seconds when timer is running"""
        self.elapsed_seconds += 1
        self.time_label.setText(self.format_time(self.elapsed_seconds))

    def toggle_stopwatch(self):
        """Starts or pauses the stopwatch"""
        if self.is_running:
            #currently running , pause it
            self.timer.stop()
            self.is_running = False
            self.start_btn.setText('Start')
        else:
            #currently paused, start it
            self.timer.start(1000) ##update every 1000 ms (1 second)
            self.is_running = True
            self.start_btn.setText('Pause')

    def reset_stopwatch(self):
        """Resets the stopwatch to 0"""
        self.timer.stop()
        self.is_running = False
        self.elapsed_seconds =0
        self.time_label.setText('00:00:00')
        self.start_btn.setText('Start')

def main(): #this is the main function that creates the application and starts the event loop
    app=QApplication(sys.argv) #creates an instance of the QApplication class
    window=DigitalTimerApp() #creates the main window object
    window.show() #displays the window
    sys.exit(app.exec()) #starts the event loop and waits for the application to close

if __name__ == '__main__': #this is the entry point of the program
    main() #Runs main() only if script is executed directly (not imported)