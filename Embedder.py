import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from skimage.feature import hog
from skimage import exposure

import cv2

class Embedder(object):
    '''
    This class is used to generate embeddings for images.
    '''

    hogParams = {
        'orientations': 9,
        'pixels_per_cell':(16,16), # default (8,8)
        'cells_per_block':(2, 2),
        'block_norm':'L2-Hys',
        'visualize':True, 
    }

    def _hogEmbedding(self, img):
        # Histogram of Oriented Gradients
        features, _ = hog(img, **self.hogParams)
        
        return features

    def embedd(self, img) -> np.ndarray:
        if self.method == "HOG":
            return self._hogEmbedding(img)
        else:
            raise(Exception("Unknown embedding method"))
    
    def getDim(self):
        return self._dim

    def __init__(self, method="HOG"):
        self.method = method
        if self.method == "HOG":
            self.imgShape = (400,400)
            assert self.imgShape[0] % self.hogParams['pixels_per_cell'][0] == 0 and self.imgShape[1] % self.hogParams['pixels_per_cell'][1] == 0, "Shape and cell size need to be multiples"
            blocks_x = (self.imgShape[0] / self.hogParams['pixels_per_cell'][0]) - self.hogParams['cells_per_block'][0] + 1
            blocks_y = (self.imgShape[1] / self.hogParams['pixels_per_cell'][1]) - self.hogParams['cells_per_block'][1] + 1
            self._dim = int(blocks_x * blocks_y * self.hogParams['cells_per_block'][0] * self.hogParams['cells_per_block'][1] * self.hogParams['orientations'])
        else:
            raise(Exception("Unknown embedding method"))

if __name__ == "__main__":
    import ImageUtil
    import TestValues
    embedder = Embedder()
    embeddings = []
    print(f'Embedder dimension {embedder.getDim()}')
    for url in TestValues.TEST_URLs:
        img = ImageUtil.ImageUtil.loadImage(url)
        if img is None:
            print(f"Could not load {url}")
            continue
        img = ImageUtil.ImageUtil.resizeImage(img, embedder.imgShape)
        print(f'img shape: {img.shape}')
        embeddings.append(embedder.embedd(img))
        print(embeddings[-1].shape)

    breakpoint()