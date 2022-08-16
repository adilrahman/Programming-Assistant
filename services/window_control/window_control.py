import pyautogui

minimize_window_coordinates = { "x" : 1836, "y" : 47 }
close_window_coordinates = { "x" : 1836, "y" : 45 }

def minimize_window():

    x = minimize_window_coordinates["x"]
    y = minimize_window_coordinates["y"]
    pyautogui.moveTo(x,y)
    pyautogui.click()

def close_window():
    x = close_window_coordinates["x"]
    y = close_window_coordinates["y"]
    pyautogui.click(x = x, y = y)


if __name__ == "__main__":
    minimize_window()
    