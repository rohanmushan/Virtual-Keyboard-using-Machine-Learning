# Virtual Keyboard with Hand Gesture Recognition

A Python-based virtual keyboard that uses computer vision and hand gesture recognition to enable touchless typing. This project leverages MediaPipe for hand tracking and OpenCV for real-time video processing.

## Features

- **Real-time Hand Tracking**: Supports tracking of up to two hands simultaneously
- **Gesture-based Input**: Uses pinch gestures between thumb and index finger for key selection
- **Customizable Layout**: QWERTY keyboard layout with number keys and special function keys
- **Visual Feedback**: Real-time visualization of hand tracking and key selection
- **Smooth Interaction**: Implements position smoothing for stable hand tracking
- **Special Keys Support**:
  - Shift: Toggle uppercase letters
  - Caps Lock: Toggle caps lock mode
  - Delete: Remove last character
  - Space: Insert space character

## Requirements

- Python 3.7+
- OpenCV (cv2)
- MediaPipe
- NumPy
- PyAutoGUI (pynput)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/virtual-keyboard.git
cd virtual-keyboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the virtual keyboard:
```bash
python Code/virtual_keyboard.py
```

2. Position your hands in front of the camera:
   - Use your thumb and index finger to form a pinch gesture
   - Move your hand to hover over the desired key
   - Perform a pinch gesture to select the key

3. Keyboard Controls:
   - First hand is tracked in green
   - Second hand is tracked in red
   - Pinch gesture distance is displayed for each hand
   - Visual feedback shows when a key is selected

## Technical Details

### Hand Tracking
- Uses MediaPipe's hand tracking solution
- Detection confidence threshold: 0.8
- Tracking confidence threshold: 0.7
- Supports up to 2 hands simultaneously

### Keyboard Layout
- 4 rows of keys (numbers, QWERTY, and special keys)
- Regular key size: 50x50 pixels
- Special key size: 80x50 pixels
- Space key size: 280x50 pixels
- 5-pixel spacing between keys

### Performance Features
- Position smoothing factor: 0.5
- Key press cooldown: 0.3 seconds
- Maximum text length: 100 characters
- Real-time video processing at 1280x720 resolution

## Project Structure

```
virtual-keyboard/
├── Code/
│   └── virtual_keyboard.py    # Main application file
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## Implementation Details

### Key Components

1. **VirtualKeyboard Class**
   - Handles camera initialization
   - Manages hand tracking
   - Processes keyboard input
   - Renders the virtual keyboard interface

2. **Button Class**
   - Manages individual key properties
   - Handles key state (hovered/pressed)
   - Stores key position and size

3. **Hand Tracking**
   - Real-time hand landmark detection
   - Pinch gesture recognition
   - Position smoothing for stable tracking

4. **Input Processing**
   - Converts hand gestures to keyboard input
   - Manages special key functions
   - Handles text input and display


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MediaPipe for hand tracking solution
- OpenCV for computer vision capabilities
- PyAutoGUI for keyboard control functionality 
