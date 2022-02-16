if __name__ == '__main__':
    print('This file is not meant to be run directly.')
    exit(0)

from inputs import UnpluggedError
from threading import Thread
from Controller.Listener import Listener
from Controller._dict import sticks, triggers, dpads, buttons


class Controller:

    def __init__(self, gamepad, id: int, state: dict, listener: Listener):
        # initializing gamepad event environment.
        self._gamepad = gamepad
        self.id = id
        self.state: dict = state
        self._listener: Listener = listener
        # Starting controller thread.
        self._loop = Thread(target=self._run)
        self._loop.start()
        print(f'Session started for {self._gamepad} {self.id}')

    def join(self):
        self._loop.join()
    
    def _run(self):
        while self.state['alive']:
            try:
                for event in self._gamepad.read():
                    self.handle_event(event)
            except UnpluggedError:
                print(f'Controller {self.id} unplugged.')
                self.state['alive'] = False
                break
            except Exception:
                print(f'Controller {self.id} crashed.')
                self.state['alive'] = False
                break
        print(f'Session finished for {self._gamepad} {self.id}')

    def handle_event(self, event):
        if event.ev_type == 'Key':
            if event.state == 1:
                Thread(target=self._listener.button_pressed, args=(buttons[event.code],)).start()
            elif event.state == 0:
                Thread(target=self._listener.button_released, args=(buttons[event.code],)).start()
        elif event.ev_type == 'Absolute':                    
            if event.code in sticks:
                Thread(target=self._listener.axis_moved, args=(sticks[event.code], event.state)).start()
            elif event.code in triggers:
                Thread(target=self._listener.axis_moved, args=(triggers[event.code], event.state)).start()
            elif event.code in dpads:
                Thread(target=self._listener.axis_moved, args=('dx', event.state) if event.code == 'ABS_HAT0X' else ('dy', -event.state)).start()

