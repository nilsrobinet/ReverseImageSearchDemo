# Reverse image search based on: https://github.com/towhee-io/examples/blob/main/image/reverse_image_search/1_build_image_search_engine.ipynb

import pymilvus as pmv
import argparse

import ImageUtil
import DinoEmbedder

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
        try:
            data['embedding'] = self.embedder.embedd(url)
        except Exception as ex:
            print(f'Failed to load/embedd {url} - reason: {ex}')
            return False
        self.insert(collection_name=self.collectionName, data=data)
        return True

    def querySingleImage(self, url, numResults = 3):
        try:
            query_vectors = [self.embedder.embedd(url)]
        except:
            print(f'Failed to load image from URL: {url}')
            return False

        res = self.search(self.collectionName, query_vectors, limit=numResults)

        return res

    def __init__(self, collectionName, clear) -> None:
        super().__init__()
        self.embedder = DinoEmbedder.DinoEmbedder()
        self.collectionName = collectionName
        self._getCollection(collectionName=collectionName, clearCollection=clear)

if __name__ == "__main__":
    import TestValues
    # revImgSearch = ReverseImageSearch('wikimedia', clear=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('--action')
    parser.add_argument('--path')
    parser.add_argument('--url')
    parser.add_argument('--clear',type=bool)
    args = parser.parse_args()
    
    if args.clear:
        print('clearing database')
        revImgSearch = ReverseImageSearch('wikimedia_dino', clear=True)
    else:
        revImgSearch = ReverseImageSearch('wikimedia_dino', clear=False)
    
    if args.action == "insert":
        with open(args.path) as fp:
            urls = [l.replace('\n','') for l in fp.readlines()]

        failedUrls = []
        for count, url in enumerate(urls):
            print(f'Inserting {count} of {len(urls)}\r',end='')
            success = revImgSearch.insertSingleImage(url) 
            if not success: failedUrls.append(url)
        print(f'Failed to insert {len(failedUrls)}images with urls:\n{urls}')

    elif args.action == "query":
        res = revImgSearch.querySingleImage(args.url)
        print(res)
    else:
        print('Unknows action {args.action}. (insert|query)')
