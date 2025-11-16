# Digital Timer Windows Application

A responsive timer and stopwatch application for Windows that stays on top of all windows, positioned in the bottom-right corner of your screen.

## Features

- **Digital Clock Display**: Shows current time and date in a digital clock format
- **Always on Top**: Stays visible above all other applications
- **Multiple Timers**: Add multiple countdown timers with custom durations
- **Stopwatches**: Add multiple stopwatches to track elapsed time
- **Bottom-Right Positioning**: Automatically positions itself in the bottom-right corner
- **Draggable Window**: Click and drag to reposition the window anywhere on screen
- **Modern UI**: Dark theme with digital clock aesthetics

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python timer_app.py
```

### Adding a Timer

1. Set the desired time using the time picker (MM:SS format)
2. Click "Add Timer" button
3. The timer will appear in the list below
4. Click "Start" to begin the countdown
5. Click "Pause" to pause the timer
6. Click "Reset" to reset the timer to its original duration
7. Click "×" to remove the timer

### Adding a Stopwatch

1. Click "Add Stopwatch" button
2. The stopwatch will appear in the list
3. Click "Start" to begin timing
4. Click "Pause" to pause the stopwatch
5. Click "Reset" to reset to 00:00
6. Click "×" to remove the stopwatch

### Window Controls

- **Drag**: Click and drag anywhere on the window to move it
- **Close**: Click the "Close" button to exit the application

## Notes

- The window will stay on top of all other applications
- The application remembers its position when dragged
- Multiple timers and stopwatches can run simultaneously
- Timers will turn red when they reach zero

