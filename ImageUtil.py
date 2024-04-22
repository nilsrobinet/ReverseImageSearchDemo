import requests
import numpy as np
import cv2


class ImageUtil(object):
    '''
    Helper class for loading images from URLs
    '''

    @staticmethod
    def loadImage(url):
        headers = {'User-Agent': 'reverseImageSearchTest/0.0'}
        resp = requests.get(url,headers=headers)
        bytes = np.asarray(bytearray(resp.content), dtype="uint8")
        # img = cv2.imdecode(bytes, flags=0)
        img = cv2.imdecode(bytes)
        return img

    @staticmethod
    def resizeImage(img, shape):
        return cv2.resize(img, shape)

if __name__ == '__main__':
    #TEST_URL = "https://commons.wikimedia.org/wiki/Main_Page#/media/File:16-03-30-Jerusalem_Mishkenot_Sha%E2%80%99ananim-RalfR-DSCF7637.jpg"
    TEST_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Rottweiler_puppy_-21603071920.jpg/640px-Rottweiler_puppy_-21603071920.jpg"
    ImageUtil.loadImage(TEST_URL)