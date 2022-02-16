if __name__ == '__main__':
    print('This file is not meant to be run directly.')
    exit(0)

from abc import abstractmethod


class Listener:
    """
        Parent class for game controller listeners.
    """
    
    @abstractmethod
    def button_pressed(self, button: str):
        pass
    
    @abstractmethod
    def button_released(self, button: str):
        pass

    @abstractmethod
    def axis_moved(self, axis: str, value: int):
        pass

