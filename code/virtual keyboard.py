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
        self.mp_hands = mp.solutions.hands
        try:
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
        except Exception as e:
            self.cap.release()
            raise RuntimeError(f"MediaPipe initialization failed: {e}")

        try:
            self.keyboard = Controller()
        except Exception as e:
            print(f"Warning: Keyboard control disabled ({e})")
            self.keyboard = None

        self.keys = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
        ]

        self.final_text = ""
        self.last_press_time = 0
        self.press_cooldown = 0.3
        self.max_text_length = 100

        self.button_list = self._initialize_buttons()

    def _initialize_buttons(self):
        button_list = []
        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                button_list.append(Button((100 * j + 50, 100 * i + 150), key))

        button_list.append(Button((100 * 2 + 50, 450), " ", (400, 85)))
        button_list.append(Button((100 * 7 + 50, 450), "clr", (200, 85)))
        return button_list

    def draw_all(self, img, buttons):
        for button in buttons:
            x, y = button.pos
            w, h = button.size
            if button.hovered:
                cv2.rectangle(img, (x-3, y-3), (x + w + 3, y + h + 3), (255, 255, 0), 3)
                cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), cv2.FILLED)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), cv2.FILLED)
            
            if button.text == "clr":
                cv2.putText(img, button.text, (x + 20, y + 65),
                           cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            elif button.text != " ":
                cv2.putText(img, button.text, (x + 20, y + 65),
                           cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        return img

    def process_hand_gestures(self, img, results):
        current_time = time()
        pressed_this_frame = False
        
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                if len(hand_landmarks.landmark) < 9:
                    continue

                mp.solutions.drawing_utils.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2)
                )
                
                h, w = img.shape[:2]
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                
                tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                
                hand_color = (0, 255, 0) if hand_idx == 0 else (0, 0, 255)
                cv2.circle(img, (tx, ty), 15, hand_color, cv2.FILLED)
                cv2.circle(img, (ix, iy), 15, hand_color, cv2.FILLED)
                cv2.line(img, (tx, ty), (ix, iy), (255, 0, 255), 3)
                
                mx, my = (tx + ix) // 2, (ty + iy) // 2
                cv2.circle(img, (mx, my), 10, (0, 255, 255), cv2.FILLED)
                
                for button in self.button_list:
                    bx, by = button.pos
                    bw, bh = button.size
                    
                    if bx < mx < bx + bw and by < my < by + bh:
                        button.hovered = True
                        if not pressed_this_frame and (current_time - self.last_press_time) > self.press_cooldown:
                            distance = np.sqrt((tx - ix)**2 + (ty - iy)**2)
                            
                            if distance < 40:
                                cv2.rectangle(img, (bx - 5, by - 5), 
                                             (bx + bw + 5, by + bh + 5),
                                             (175, 0, 175), cv2.FILLED)
                                self._handle_button_press(button)
                                self.last_press_time = current_time
                                pressed_this_frame = True

    def _handle_button_press(self, button):
        if len(self.final_text) >= self.max_text_length:
            self.final_text = self.final_text[-self.max_text_length:]
            
        if button.text == "clr":
            if self.keyboard:
                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
            self.final_text = self.final_text[:-1]
        elif button.text == " ":
            if self.keyboard:
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)
            self.final_text += " "
        else:
            if self.keyboard:
                self.keyboard.press(button.text)
                self.keyboard.release(button.text)
            self.final_text += button.text

    def run(self):
        try:
            while True:
                success, img = self.cap.read()
                if not success:
                    print("Failed to capture image")
                    break

                img = cv2.flip(img, 1)
                
                cv2.rectangle(img, (50, 50), (1230, 120), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, self.final_text, (60, 110), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 255, 255), 5)
                
                for button in self.button_list:
                    button.hovered = False
                
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = self.hands.process(img_rgb)
                if results:
                    self.process_hand_gestures(img, results)
                
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