import os
import re
import time
import pyautogui
from PIL import Image


class TakeScreenShot:
    def __init__(self, path: str, prefix: str = "screenShot_by_friday") -> None:
        '''
        inputs:
            path = your screenshot saving location 

            prefix = screenshot image name prefix 
                    `default :- screenShot_by_friday`


        outputs:
            None

        '''
        self.saving_path = path
        self.img_prefix = prefix

        # this is the suffix value of new screenshots
        self.__screenshot_count = self.__track_screenshot_count() + 1

    def __track_screenshot_count(self):
        '''
         description:
            finding the last screenshot suffix value (integer) and afterward screenshots will
            follow the highest suffix stored so far

        inputs:
            None

        outputs:
            return last strored image suffix count
        '''

        stored_imgs_names = os.listdir(self.saving_path)
        large_num = -1

        for img in stored_imgs_names:
            image_count = re.search("[0-9]+", img)

            if image_count:
                if large_num < int(image_count[0]):
                    large_num = int(image_count[0])

        return large_num

    def capture(self):
        '''
        description:
            for capturing screenshots

        inputs:
            None

        outputs:
            return `image path` if `captured` else return False 
        '''
        img = pyautogui.screenshot()

        # adding prefix, suffix and extention of new screenshots
        img_suffix = "_" + str(self.__screenshot_count)
        img_name = self.img_prefix + img_suffix + ".png"
        img_location = os.path.join(self.saving_path, img_name)

        img.save(img_location)

        return img_location

    @staticmethod
    def open_image(img_loc: str):
        '''
        description:
            it open images

        inputs:
            img_loc = images location full path 

        outputs:
            open image

            return `true` if `opened` else `false`
        '''

        img = Image.open(img_loc)
        img.show()


if __name__ == "__main__":
    screenshot = TakeScreenShot(path="/home/adil/Desktop/git_testing_local")
    scr = screenshot.capture()
    print(screenshot.__screenshot_count)
    time.sleep(0.5)
    # screenshot.open_image(scr)
