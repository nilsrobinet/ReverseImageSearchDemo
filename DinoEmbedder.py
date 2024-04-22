from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import requests
import torch
from Embedder import Embedder

class DinoEmbedder(Embedder):

    def getDim(self):
        return 768 # len(out[1][0])

    @property
    def imgShape(self):
        return (224,224)

    def embedd(self, url):
        headers = {'User-Agent': 'reverseImageSearchTest/0.0'}
        image = Image.open(requests.get(url, stream=True, headers=headers).raw)
        inputs = self.processor(images=image, return_tensors="pt")
        out = self.model(**inputs)
        # return pooler output: pooler_output
        return out[1][0].detach().cpu().numpy()

    def __init__(self):
        self.model = AutoModel.from_pretrained("models/dinov2-base")
        self.processor = AutoImageProcessor.from_pretrained("models/dinov2-base")

if __name__ == "__main__":
    import TestValues
    # breakpoint()

    pass
    #import ImageUtil
    #import TestValues
    #embedder = HogEmbedder()
    #embeddings = []
    #print(f'Embedder dimension {embedder.getDim()}')
    #for url in TestValues.TEST_URLs:
    #    img = ImageUtil.ImageUtil.loadImage(url)
    #    if img is None:
    #        print(f"Could not load {url}")
    #        continue
    #    img = ImageUtil.ImageUtil.resizeImage(img, embedder.imgShape)
    #    print(f'img shape: {img.shape}')
    #    embeddings.append(embedder.embedd(img))
    #    print(embeddings[-1].shape)

    #breakpoint()
