import time

bob = time.time()

time.sleep(0.000000000000000001)

print(time.time() - bob)

import pyautogui
pyautogui.moveTo(100, 150)
time.sleep(3)
pyautogui.moveRel(0, 1000)  # move mouse 10 pixels down
time.sleep(3)
pyautogui.dragTo(100, 150)
time.sleep(3)
pyautogui.dragRel(0, 1000)  # drag mouse 10 pixels down
time.sleep(3)