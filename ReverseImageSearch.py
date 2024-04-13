# Reverse image search based on: https://github.com/towhee-io/examples/blob/main/image/reverse_image_search/1_build_image_search_engine.ipynb

import pymilvus as pmv
import logging as log

import ImageUtil
import Embedder

# constants
METRIC_TYPE='L2'
INDEX_TYPE='IVF_FLAT'

class ReverseImageSearch(pmv.MilvusClient):

    def _getCollection(self, collectionName: str, clearCollection:bool=False, distanceMetric=METRIC_TYPE, index_type=INDEX_TYPE):
        if clearCollection:
            self.drop_collection(collectionName)
        if collectionName in self.list_collections():
            return
        fields = [
            pmv.FieldSchema(name="url", dtype=pmv.DataType.VARCHAR, description="URL to image", max_length = 500, is_primary = True, auto_id=False),
            pmv.FieldSchema(name="embedding", dtype=pmv.DataType.FLOAT_VECTOR, description="vector embedding of the image", dim=self.embedder.getDim())
        ]
        index_params = {
            'metric_type': distanceMetric,
            'index_type': index_type,
            'params': {
                'nlist': 2048
            } 
        }
        schema = pmv.CollectionSchema(fields=fields, description='reverse image search')
        self.create_collection_with_schema(collection_name=collectionName, schema=schema, index_params=index_params)

    def insertSingleImage(self, url) -> bool:
        data = {
            'url':url,
            'embedding':None
        }
        image = ImageUtil.ImageUtil.loadImage(url) 
        if image is None:
            print(f'Failed to load image from URL: {url}')
            return False
        image = ImageUtil.ImageUtil.resizeImage(image, self.embedder.imgShape)
        data['embedding'] = self.embedder.embedd(image)
        self.insert(collection_name=self.collectionName, data=data)
        return True

    def querySingleImage(self, url, numResults = 3):
        image = ImageUtil.ImageUtil.loadImage(url) 
        if image is None:
            print(f'Failed to load image from URL: {url}')
            return False
        image = ImageUtil.ImageUtil.resizeImage(image, self.embedder.imgShape)
        query_vectors = [self.embedder.embedd(image)]

        res = self.search(self.collectionName, query_vectors, limit=numResults)

        return res

    def __init__(self, collectionName, clear) -> None:
        super().__init__()
        self.embedder = Embedder.Embedder()
        self.collectionName = collectionName
        self._getCollection(collectionName=collectionName, clearCollection=clear)

if __name__ == "__main__":
    import TestValues
    # revImgSearch = ReverseImageSearch('wikimedia', clear=True)
    revImgSearch = ReverseImageSearch('wikimedia', clear=False)
    # failedUrls = []
    # for url in TestValues.TEST_URLs:
    #     success = revImgSearch.insertSingleImage(url) 
    #     if not success: failedUrls.append(url)

    res = revImgSearch.querySingleImage(TestValues.TEST_QUERY)
    print(res)
