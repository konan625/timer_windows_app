import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTimeEdit, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QTimer, QTime, QPoint
from PyQt6.QtGui import QFont, QScreen
from datetime import datetime, timedelta
import json
import os

class TimerWidget(QWidget):
    """Widget for individual timer/stopwatch"""
    def __init__(self, parent=None, is_stopwatch=False, duration_seconds=None):
        super().__init__(parent)
        self.is_stopwatch = is_stopwatch
        self.is_running = False
        self.remaining_seconds = duration_seconds if not is_stopwatch else 0
        self.elapsed_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Title label
        title = "Stopwatch" if self.is_stopwatch else "Timer"
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Time display
        self.time_label = QLabel(self.format_time())
        self.time_label.setFont(QFont("Consolas", 16, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("color: #00ff00; background-color: #000000; padding: 5px; border-radius: 5px;")
        layout.addWidget(self.time_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_pause_btn = QPushButton("Start")
        self.start_pause_btn.clicked.connect(self.toggle_timer)
        self.start_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_timer)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        self.delete_btn = QPushButton("×")
        self.delete_btn.clicked.connect(self.delete_self)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        
        button_layout.addWidget(self.start_pause_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.delete_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 8px;
                margin: 2px;
            }
        """)
        
    def format_time(self):
        """Format time for display"""
        if self.is_stopwatch:
            total_seconds = self.elapsed_seconds
        else:
            total_seconds = self.remaining_seconds
            
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def toggle_timer(self):
        """Start or pause the timer"""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.start_pause_btn.setText("Start")
            self.start_pause_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
        else:
            self.timer.start(1000)  # Update every second
            self.is_running = True
            self.start_pause_btn.setText("Pause")
            self.start_pause_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff9800;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e68900;
                }
            """)
    
    def update_time(self):
        """Update the timer/stopwatch time"""
        if self.is_stopwatch:
            self.elapsed_seconds += 1
        else:
            if self.remaining_seconds > 0:
                self.remaining_seconds -= 1
            else:
                self.timer.stop()
                self.is_running = False
                self.start_pause_btn.setText("Start")
                self.time_label.setStyleSheet("color: #ff0000; background-color: #000000; padding: 5px; border-radius: 5px;")
                # Flash effect could be added here
                return
        
        self.time_label.setText(self.format_time())
    
    def reset_timer(self):
        """Reset the timer/stopwatch"""
        self.timer.stop()
        self.is_running = False
        if self.is_stopwatch:
            self.elapsed_seconds = 0
        else:
            # Reset to original duration - we need to store this
            if hasattr(self, 'original_duration'):
                self.remaining_seconds = self.original_duration
        self.time_label.setText(self.format_time())
        self.time_label.setStyleSheet("color: #00ff00; background-color: #000000; padding: 5px; border-radius: 5px;")
        self.start_pause_btn.setText("Start")
        self.start_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    
    def delete_self(self):
        """Remove this timer widget"""
        if self.parent():
            self.parent().remove_timer(self)
    
    def set_duration(self, seconds):
        """Set the timer duration"""
        self.remaining_seconds = seconds
        self.original_duration = seconds
        self.time_label.setText(self.format_time())


class DigitalTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timers = []
        self.init_ui()
        self.position_window()
        
        # Clock update timer
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)  # Update every second
        self.update_clock()
        
    def init_ui(self):
        self.setWindowTitle("Digital Timer")
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Digital clock display
        self.clock_label = QLabel()
        self.clock_label.setFont(QFont("Consolas", 24, QFont.Weight.Bold))
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                background-color: #000000;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #00ff00;
            }
        """)
        main_layout.addWidget(self.clock_label)
        
        # Scroll area for timers
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(400)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #333;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #666;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #777;
            }
        """)
        
        self.timers_container = QWidget()
        self.timers_layout = QVBoxLayout()
        self.timers_layout.setSpacing(5)
        self.timers_layout.setContentsMargins(0, 0, 0, 0)
        self.timers_container.setLayout(self.timers_layout)
        scroll.setWidget(self.timers_container)
        main_layout.addWidget(scroll)
        
        # Add timer/stopwatch controls
        controls_layout = QHBoxLayout()
        
        # Timer input
        self.timer_input = QTimeEdit()
        self.timer_input.setDisplayFormat("mm:ss")
        self.timer_input.setTime(QTime(0, 5, 0))  # Default 5 minutes
        self.timer_input.setStyleSheet("""
            QTimeEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        
        add_timer_btn = QPushButton("Add Timer")
        add_timer_btn.clicked.connect(self.add_timer)
        add_timer_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        add_stopwatch_btn = QPushButton("Add Stopwatch")
        add_stopwatch_btn.clicked.connect(self.add_stopwatch)
        add_stopwatch_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        
        controls_layout.addWidget(self.timer_input)
        controls_layout.addWidget(add_timer_btn)
        controls_layout.addWidget(add_stopwatch_btn)
        main_layout.addLayout(controls_layout)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        main_layout.addWidget(close_btn)
        
        main_widget.setLayout(main_layout)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: white;
            }
        """)
        
        # Enable dragging
        self.drag_position = QPoint()
        
    def mousePressEvent(self, event):
        """Enable window dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def position_window(self):
        """Position window at bottom-right of screen"""
        screen = QApplication.primaryScreen().geometry()
        window_width = 350
        window_height = 600
        x = screen.width() - window_width - 20
        y = screen.height() - window_height - 50
        self.setGeometry(x, y, window_width, window_height)
    
    def update_clock(self):
        """Update the digital clock display"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        self.clock_label.setText(f"{time_str}\n{date_str}")
    
    def add_timer(self):
        """Add a new timer"""
        time = self.timer_input.time()
        total_seconds = time.hour() * 3600 + time.minute() * 60 + time.second()
        
        if total_seconds == 0:
            return
        
        timer_widget = TimerWidget(self.timers_container, is_stopwatch=False, duration_seconds=total_seconds)
        timer_widget.set_duration(total_seconds)
        self.timers_layout.addWidget(timer_widget)
        self.timers.append(timer_widget)
    
    def add_stopwatch(self):
        """Add a new stopwatch"""
        stopwatch_widget = TimerWidget(self.timers_container, is_stopwatch=True)
        self.timers_layout.addWidget(stopwatch_widget)
        self.timers.append(stopwatch_widget)
    
    def remove_timer(self, timer_widget):
        """Remove a timer widget"""
        if timer_widget in self.timers:
            self.timers.remove(timer_widget)
            timer_widget.setParent(None)
            timer_widget.deleteLater()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better appearance
    
    window = DigitalTimerApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

