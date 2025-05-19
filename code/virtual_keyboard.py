import os
import cv2
import numpy as np
from pynput.keyboard import Controller, Key
from time import time
import mediapipe as mp

class VirtualKeyboard:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        
        # Improved MediaPipe parameters
        self.mp_hands = mp.solutions.hands
        try:
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.8,
                min_tracking_confidence=0.7,
                model_complexity=1
            )
        except Exception as e:
            self.cap.release()
            raise RuntimeError(f"MediaPipe initialization failed: {e}")

        try:
            self.keyboard = Controller()
        except Exception as e:
            print(f"Warning: Keyboard control disabled ({e})")
            self.keyboard = None

        # Define keyboard layouts (display in uppercase, but store lowercase)
        self.keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
        ]
        
        # Store lowercase versions for input
        self.input_keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
            ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]
        ]
        
        self.special_keys = [
            ["Shift", "Caps", "Del", "Space"]
        ]

        self.final_text = ""
        self.last_press_time = 0
        self.press_cooldown = 0.3
        self.max_text_length = 100
        self.caps_lock = False
        self.shift_pressed = False

        self.button_list = self._initialize_buttons()
        
        # Add smoothing parameters for each hand
        self.smoothing_factor = 0.5
        self.hand_positions = {
            0: {'prev_thumb': None, 'prev_index': None},  # First hand
            1: {'prev_thumb': None, 'prev_index': None}   # Second hand
        }

    def _initialize_buttons(self):
        button_list = []
        # Define key sizes
        regular_key_size = (50, 50)  # Smaller regular keys
        special_key_size = (80, 50)  # Wider special keys
        space_key_size = (280, 50)   # Adjusted space key width to fit exactly

        # Starting position
        start_x = 50
        start_y = 150
        key_spacing = 5  # Space between keys

        # Add number and letter keys
        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                x = start_x + j * (regular_key_size[0] + key_spacing)
                y = start_y + i * (regular_key_size[1] + key_spacing)
                button_list.append(Button((x, y), key, regular_key_size))

        # Add special keys in a single row
        special_start_y = start_y + 4 * (regular_key_size[1] + key_spacing)
        
        # Add Shift key
        button_list.append(Button((start_x, special_start_y), "Shift", special_key_size))
        
        # Add Caps key
        button_list.append(Button((start_x + special_key_size[0] + key_spacing, special_start_y), 
                                "Caps", special_key_size))
        
        # Add Del key
        button_list.append(Button((start_x + 2 * (special_key_size[0] + key_spacing), special_start_y), 
                                "Del", special_key_size))
        
        # Add Space key (adjusted width)
        button_list.append(Button((start_x + 3 * (special_key_size[0] + key_spacing), special_start_y), 
                                " ", space_key_size))

        return button_list

    def draw_all(self, img, buttons):
        for button in buttons:
            x, y = button.pos
            w, h = button.size
            if button.hovered:
                cv2.rectangle(img, (x-2, y-2), (x + w + 2, y + h + 2), (255, 255, 0), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), cv2.FILLED)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), cv2.FILLED)
            
            # Draw button text
            if button.text == " ":
                continue  # Skip drawing text for space bar
            elif button.text in ["Shift", "Caps", "Del", "Space"]:
                # Draw special keys with smaller font
                text_size = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
                text_x = x + (w - text_size[0]) // 2
                text_y = y + (h + text_size[1]) // 2
                cv2.putText(img, button.text, (text_x, text_y),
                           cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
            else:
                # Draw regular keys (always in uppercase)
                text_size = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 1.5, 1)[0]
                text_x = x + (w - text_size[0]) // 2
                text_y = y + (h + text_size[1]) // 2
                cv2.putText(img, button.text, (text_x, text_y),
                           cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1)
        return img

    def preprocess_image(self, img):
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Apply histogram equalization for better contrast
        img_yuv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        img_rgb = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
        
        # Apply slight Gaussian blur to reduce noise
        img_rgb = cv2.GaussianBlur(img_rgb, (3, 3), 0)
        
        return img_rgb

    def smooth_landmarks(self, current_pos, prev_pos):
        if prev_pos is None:
            return current_pos
        return (
            int(self.smoothing_factor * current_pos[0] + (1 - self.smoothing_factor) * prev_pos[0]),
            int(self.smoothing_factor * current_pos[1] + (1 - self.smoothing_factor) * prev_pos[1])
        )

    def process_hand_gestures(self, img, results):
        current_time = time()
        pressed_this_frame = False
        
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                if len(hand_landmarks.landmark) < 9:
                    continue

                # Draw hand landmarks with MediaPipe's original colors
                mp.solutions.drawing_utils.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_utils.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp.solutions.drawing_utils.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )
                
                h, w = img.shape[:2]
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                
                # Get current positions
                current_thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
                current_index_pos = (int(index_tip.x * w), int(index_tip.y * h))
                
                # Apply smoothing using hand-specific previous positions
                tx, ty = self.smooth_landmarks(current_thumb_pos, self.hand_positions[hand_idx]['prev_thumb'])
                ix, iy = self.smooth_landmarks(current_index_pos, self.hand_positions[hand_idx]['prev_index'])
                
                # Update previous positions for this specific hand
                self.hand_positions[hand_idx]['prev_thumb'] = (tx, ty)
                self.hand_positions[hand_idx]['prev_index'] = (ix, iy)
                
                # Use custom colors for interaction elements
                hand_color = (0, 255, 0) if hand_idx == 0 else (0, 0, 255)
                
                # Draw finger tips and connecting line with hand-specific color
                cv2.circle(img, (tx, ty), 8, hand_color, cv2.FILLED)
                cv2.circle(img, (ix, iy), 8, hand_color, cv2.FILLED)
                cv2.line(img, (tx, ty), (ix, iy), hand_color, 2)
                
                # Calculate distance between thumb and index finger
                distance = np.sqrt((tx - ix)**2 + (ty - iy)**2)
                
                # Draw distance indicator for each hand
                distance_text_pos = (10, 30 + hand_idx * 30)
                cv2.putText(img, f"Hand {hand_idx + 1} Distance: {int(distance)}", 
                          distance_text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, hand_color, 2)
                
                # Visual feedback for pinch gesture - moved more to the left
                if distance < 50:
                    pinch_text_pos = (img.shape[1] - 500, 30 + hand_idx * 30)  # Changed from -300 to -500
                    cv2.putText(img, f"Hand {hand_idx + 1} PINCH DETECTED", 
                              pinch_text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, hand_color, 2)
                
                mx, my = (tx + ix) // 2, (ty + iy) // 2
                cv2.circle(img, (mx, my), 6, hand_color, cv2.FILLED)
                
                for button in self.button_list:
                    bx, by = button.pos
                    bw, bh = button.size
                    
                    # Check if middle point is within button bounds
                    if bx < mx < bx + bw and by < my < by + bh:
                        button.hovered = True
                        
                        # Draw button highlight with hand-specific color
                        cv2.rectangle(img, (bx - 2, by - 2), 
                                    (bx + bw + 2, by + bh + 2), 
                                    hand_color, 2)
                        
                        # Check for pinch gesture and cooldown
                        if not pressed_this_frame and (current_time - self.last_press_time) > self.press_cooldown:
                            if distance < 50:
                                # Visual feedback for button press
                                cv2.rectangle(img, (bx - 5, by - 5), 
                                            (bx + bw + 5, by + bh + 5),
                                            hand_color, cv2.FILLED)
                                
                                # Add slight delay to ensure the press is intentional
                                if current_time - self.last_press_time > 0.5:
                                    self._handle_button_press(button)
                                    self.last_press_time = current_time
                                    pressed_this_frame = True
                                    # Add visual feedback for successful press
                                    cv2.putText(img, "PRESSED", (bx, by - 10), 
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                                              hand_color, 2)

    def _handle_button_press(self, button):
        if len(self.final_text) >= self.max_text_length:
            self.final_text = self.final_text[-self.max_text_length:]
            
        if button.text == " ":
            if self.keyboard:
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)
            self.final_text += " "
        elif button.text == "Shift":
            self.shift_pressed = not self.shift_pressed
        elif button.text == "Caps":
            self.caps_lock = not self.caps_lock
        elif button.text == "Del":
            if self.keyboard:
                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
            self.final_text = self.final_text[:-1]
        else:
            # Find the corresponding lowercase key
            key_index = None
            for i, row in enumerate(self.keys):
                if button.text in row:
                    key_index = (i, row.index(button.text))
                    break
            
            if key_index:
                i, j = key_index
                key_to_press = self.input_keys[i][j]
                if self.shift_pressed or self.caps_lock:
                    key_to_press = key_to_press.upper()
                if self.keyboard:
                    self.keyboard.press(key_to_press)
                    self.keyboard.release(key_to_press)
                self.final_text += key_to_press
                if self.shift_pressed:
                    self.shift_pressed = False  # Auto-release shift after one key press

    def run(self):
        try:
            while True:
                success, img = self.cap.read()
                if not success:
                    print("Failed to capture image")
                    break

                img = cv2.flip(img, 1)
                
                # Preprocess the image
                img_rgb = self.preprocess_image(img)
                
                # Draw text display area
                cv2.rectangle(img, (50, 50), (1230, 120), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, self.final_text, (60, 110), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 255, 255), 5)
                
                # Reset button hover states
                for button in self.button_list:
                    button.hovered = False
                
                # Process hand gestures
                results = self.hands.process(img_rgb)
                if results:
                    self.process_hand_gestures(img, results)
                
                # Draw all buttons
                img = self.draw_all(img, self.button_list)
                
                try:
                    cv2.imshow("Virtual Keyboard", img)
                except cv2.error as e:
                    if os.environ.get("DISPLAY"):
                        print(f"Display error: {e}")
                    else:
                        print("No display detected")
                    break

                if cv2.waitKey(1) == 27:
                    break

        finally:
            self.cap.release()
            if hasattr(self, 'hands'):
                self.hands.close()
            cv2.destroyAllWindows()

class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text
        self.hovered = False

if __name__ == "__main__":
    try:
        vk = VirtualKeyboard()
        vk.run()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)