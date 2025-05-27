# Virtual Keyboard with Hand Gesture Recognition

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A sophisticated Python-based virtual keyboard system that leverages computer vision and hand gesture recognition for touchless typing interaction. This project combines MediaPipe's advanced hand tracking capabilities with OpenCV's real-time video processing to create an intuitive and responsive virtual typing experience.

## 📑 Table of Contents

- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Detailed Setup Guide](#-detailed-setup-guide)
- [Usage Instructions](#-usage-instructions)
- [Technical Architecture](#-technical-architecture)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Functionality
- **Advanced Hand Tracking**
  - Real-time tracking of up to two hands simultaneously
  - High-precision finger landmark detection
  - Robust tracking in various lighting conditions

- **Intelligent Gesture Recognition**
  - Precise pinch gesture detection between thumb and index finger
  - Customizable gesture sensitivity
  - Position smoothing for stable interaction

- **Interactive Keyboard Interface**
  - Full QWERTY layout with number row
  - Special function keys support
  - Visual feedback system
  - Customizable key layouts

### Special Keys and Functions
- **Input Modifiers**
  - Shift key for uppercase letters
  - Caps Lock toggle functionality
  - Backspace for character deletion
  - Spacebar for word separation

- **Visual Feedback System**
  - Real-time hand position visualization
  - Key highlight on hover
  - Gesture confirmation indicators
  - Input preview display

## 💻 System Requirements

### Hardware Requirements
- CPU: Intel Core i5/AMD Ryzen 5 or better
- RAM: 8GB minimum (16GB recommended)
- Webcam: HD camera with minimum 720p resolution
- Storage: 500MB free space
- Display: 1280x720 minimum resolution

### Software Requirements
- Operating System:
  - Windows 10/11 (64-bit)
  - macOS 10.14 or later
  - Ubuntu 18.04 or later
- Python 3.7 or higher
- Package Dependencies:
  - OpenCV (cv2) >= 4.5.0
  - MediaPipe >= 0.8.9
  - NumPy >= 1.19.0
  - PyAutoGUI >= 0.9.53
  - pynput >= 1.7.0

## 🚀 Installation

### Method 1: Using pip (Recommended)

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

### Method 2: Using Conda

1. Clone the repository:
```bash
git clone https://github.com/yourusername/virtual-keyboard.git
cd virtual-keyboard
```

2. Create and activate a Conda environment:
```bash
conda create -n virtual-keyboard python=3.9
conda activate virtual-keyboard
```

3. Install dependencies:
```bash
conda install --file requirements.txt
```

## 📖 Detailed Setup Guide

### Windows Setup
1. Install Python 3.7+ from [python.org](https://www.python.org/downloads/)
2. Add Python to PATH during installation
3. Install Visual C++ Build Tools:
   - Download from [Visual Studio Downloads](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Select "Desktop development with C++"
4. Follow the standard installation steps above

### macOS Setup
1. Install Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python:
```bash
brew install python@3.9
```

3. Install required system libraries:
```bash
brew install cmake pkg-config
```

4. Follow the standard installation steps above

### Linux (Ubuntu/Debian) Setup
1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev build-essential cmake pkg-config
sudo apt-get install -y libopencv-dev python3-opencv
```

2. Follow the standard installation steps above

## 🎮 Usage Instructions

### Starting the Application
1. Navigate to the project directory:
```bash
cd virtual-keyboard
```

2. Activate your virtual environment:
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Run the application:
```bash
python Code/virtual_keyboard.py
```

### Hand Gesture Controls
- **Key Selection**:
  1. Position your hand in the camera's field of view
  2. Move your hand to hover over desired key
  3. Perform a pinch gesture with thumb and index finger
  4. Hold the pinch for key activation
  5. Release to complete the keystroke

- **Special Functions**:
  - Shift: Pinch and hold with second hand while typing
  - Caps Lock: Double pinch on Caps Lock key
  - Delete: Pinch and hold on Delete key
  - Space: Quick pinch on spacebar

### Camera Setup
- Position camera at eye level
- Ensure good lighting conditions
- Maintain 50-70cm distance from camera
- Keep hands within the marked tracking area

## 🔧 Technical Architecture

### Core Components
1. **Hand Tracking Module**
   - MediaPipe hand landmark detection
   - 21-point hand skeleton tracking
   - Confidence threshold management
   - Multi-hand coordination

2. **Gesture Recognition System**
   - Pinch detection algorithm
   - Position smoothing implementation
   - Gesture state management
   - Multi-gesture processing

3. **Virtual Keyboard Interface**
   - Dynamic key layout rendering
   - Input processing pipeline
   - Visual feedback system
   - Text buffer management

### Performance Optimization
- Frame rate: 30 FPS target
- Tracking latency: <100ms
- Memory usage: <500MB
- CPU usage: <30% on recommended hardware

## ❗ Troubleshooting

### Common Issues and Solutions

1. **Camera Not Detected**
   - Check camera connections
   - Verify camera permissions
   - Try different USB ports
   - Update camera drivers

2. **Poor Hand Tracking**
   - Improve lighting conditions
   - Maintain recommended distance
   - Check for background interference
   - Adjust tracking sensitivity

3. **Performance Issues**
   - Close resource-heavy applications
   - Check system requirements
   - Update graphics drivers
   - Reduce video resolution

4. **Installation Errors**
   - Verify Python version compatibility
   - Check for missing dependencies
   - Update pip and setuptools
   - Install Visual C++ Build Tools (Windows)

## 🤝 Contributing

We welcome contributions to improve the Virtual Keyboard project! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation as needed
- Maintain compatibility with supported Python versions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MediaPipe team for their hand tracking solution
- OpenCV community for computer vision tools
- PyAutoGUI developers for keyboard control functionality
- All contributors and users of this project

---

For additional support or questions, please open an issue on GitHub. 
