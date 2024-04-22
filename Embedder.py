import abc

class Embedder(abc.ABC):

    @abc.abstractmethod
    def embedd():
        raise NotImplementedError()
    
    @abc.abstractmethod
    def getDim():
        raise NotImplementedError()
    
    @property
    @abc.abstractmethod
    def imgShape():
        raise NotImplementedError()
