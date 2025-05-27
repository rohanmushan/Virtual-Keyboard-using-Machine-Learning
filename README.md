# Virtual Keyboard with Hand Gesture Recognition

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python-based virtual keyboard that enables touchless typing through hand gesture recognition. Using computer vision technology, this project combines MediaPipe's hand tracking capabilities with OpenCV to create an intuitive typing experience without physical contact.

## Features

- **Hand Gesture Control**: Real-time tracking of hand movements and gestures
- **Virtual QWERTY Layout**: Full keyboard layout with numbers and special characters
- **Multi-Hand Support**: Tracks up to two hands simultaneously for enhanced interaction
- **Special Key Functions**: Support for Shift, Caps Lock, Delete, and Space
- **Visual Feedback**: Real-time display of hand tracking and key selection
- **Smooth Interaction**: Implements position smoothing for stable tracking

## Prerequisites

- Python 3.7 or higher
- Webcam with minimum 720p resolution
- System Requirements:
  - 4GB RAM (8GB recommended)
  - Intel Core i3/AMD Ryzen 3 or better
  - Windows 10/11, macOS 10.14+, or Ubuntu 18.04+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/virtual-keyboard.git
cd virtual-keyboard
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. Activate your virtual environment (if not already activated)
2. Run the application:
```bash
python Code/virtual_keyboard.py
```

3. Usage:
   - Position your hands in view of the camera
   - Use pinch gestures (thumb and index finger) to select keys
   - First hand is tracked in green, second in red
   - Pinch and hold for special key functions

## Project Structure

```
virtual-keyboard/
├── Code/
│   └── virtual_keyboard.py    # Main application file
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## Troubleshooting

- Ensure proper lighting conditions
- Maintain 50-70cm distance from camera
- Check camera permissions and connections
- Update graphics drivers if experiencing lag

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- MediaPipe for hand tracking solution
- OpenCV for computer vision capabilities
- PyAutoGUI for keyboard control functionality

---

For support or questions, please open an issue on GitHub. 
