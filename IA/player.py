from abc import ABC, abstractmethod

class Player(ABC) :
    
    @abstractmethod
    def move(self,board,ignore_history=True) :
        pass
    
    @abstractmethod
    def get_name(self) :
        pass
    
    @abstractmethod
    def get_numbergames(self) :
        pass