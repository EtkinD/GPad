from threading import Thread
from time import sleep, time

from Controller.Listener import Listener

from mouse import press, release, move, wheel
from mouse._mouse_event import LEFT, RIGHT, MIDDLE

from keyboard import press_and_release as press_and_release_key


class DefaultListener(Listener):

    def __init__(self, state: dict, id: int, vibration_function: callable):
        super().__init__()
        self.vibration = vibration_function
        self.id = id
        self.mouse_motion = MouseMotion(state)
        self.keyboard_arrow_motion = KeyboardArrowMotion(state)
        self.locker = Locker(state, vibration_function)
        self.state: dict = state

    def button_pressed(self, button: str):
        self.locker.button_pressed(button)
        if self.state['interrupt']:
            return
        
        if button == 'START':
            self.state['sleep'] = not self.state['sleep']
            self.vibration(1, 1, 250)
            print(f'Sleep mode: {self.state["sleep"]} for controller {self.id}')
            return
        elif button == 'SELECT':
            self.state['alive'] = False
            self.vibration(1, 1, 400)
            return
        elif self.state['sleep']:
            return
        
        button_press_actons[button]()

    def button_released(self, button: str):
        self.locker.button_released(button)
        if self.state['interrupt']:
            return

        if self.state['sleep']:
            return
        button_release_actons[button]()
    
    def axis_moved(self, axis: str, value: int):
        self.locker.axis_moved(axis, value)
        if self.state['interrupt']:
            return
        
        if self.state['sleep']:
            return
        
        if axis == 'left_x':
            self.mouse_motion.set_velocity_x(value / 32767 if value > 0 else value / 32768)
        elif axis == 'left_y':
            self.mouse_motion.set_velocity_y(value / 32767 if value > 0 else value / 32768)
        
        elif axis == 'right_x':
            self.keyboard_arrow_motion.set_horizontal_arrow(value / 32767 if value > 0 else value / 32768)
        elif axis == 'right_y':
            self.keyboard_arrow_motion.set_vertical_arrow(value / 32767 if value > 0 else value / 32768)

        elif axis == 'left_t':
            self.mouse_motion.set_multiplier(value / 255)
        elif axis == 'right_t':
            pass

        elif axis == 'dx':
            if value == 1:
                press_and_release_key('windows+ctrl+right')
            elif value == -1:
                press_and_release_key('windows+ctrl+left')
        elif axis == 'dy':
            self.mouse_motion.set_wheel_direction(value)


# ----------------------------------------------------------------
# Lambda functions for button actions (press and release) and Gamepad axes dead zones.
button_press_actons = {
    'A': lambda: press(LEFT),
    'B': lambda: press(RIGHT),
    'X': lambda: press_and_release_key('escape'),
    'Y': lambda: press_and_release_key('windows+shift+s'),
    'LSTICK': lambda: press(MIDDLE),
    'RSTICK': lambda: press_and_release_key('altgr+tab'),
    'LSHOULDER': lambda: press_and_release_key('windows+tab'),
    'RSHOULDER': lambda: press_and_release_key('enter'),
    'START': lambda: None,
    'SELECT': lambda: None,
}
button_release_actons = {
    'A': lambda: release(LEFT),
    'B': lambda: release(RIGHT),
    'X': lambda: None,
    'Y': lambda: None,
    'LSTICK': lambda: release(MIDDLE),
    'RSTICK': lambda: None,
    'LSHOULDER': lambda: None,
    'RSHOULDER': lambda: None,
    'START': lambda: None,
    'SELECT': lambda: None,
}
axis_dead_zones = {
    'left_stick': .1,
    'right_stick': .1,
    'left_trigger': .1,
    'right_trigger': .1,
}
# ----------------------------------------------------------------


class MouseMotion:
    """
    Class for handling mouse behavior.
    """

    def __init__(self, state: dict):
        self.state: dict = state
        
        self.multiplier = 1
        self.wheel_y = 0
        
        self.velocity = 5
        self.velocity_x = 0
        self.velocity_y = 0
        
        Thread(target=self.run).start()
    
    def set_velocity_x(self, value: float):
        if value >= axis_dead_zones['left_stick'] or value <= -axis_dead_zones['left_stick']:
            self.velocity_x = value * self.velocity
        else:
            self.velocity_x = 0
    
    def set_velocity_y(self, value: float):
        if value >= axis_dead_zones['left_stick'] or value <= -axis_dead_zones['left_stick']:
            self.velocity_y = value * self.velocity
        else:
            self.velocity_y = 0

    def set_wheel_direction(self, value: int):
        self.wheel_y = value / 10
    
    def set_multiplier(self, value: float):
        if value >= axis_dead_zones['left_trigger']:
            self.multiplier = 1 + (value * 2)
        else:
            self.multiplier = 1

    def run(self):
        while self.state['alive']:
            if self.state['sleep']:
                sleep(0.1)
                continue
            if self.velocity_x != 0 or self.velocity_y != 0:
                move(self.velocity_x * self.multiplier, -self.velocity_y * self.multiplier, False)
            if self.wheel_y != 0:
                wheel(self.wheel_y * self.multiplier)
            sleep(0.01)


class KeyboardArrowMotion:
    """
    Class to handle press arrow keys
    """

    def __init__(self, state: dict):
        self.state: dict = state

        self.values = {'horizontal': 0, 'vertical': 0}

        Thread(target=self.run).start()
    
    def set_horizontal_arrow(self, value: float):
        if value >= axis_dead_zones['right_stick']:
            self.values['horizontal'] = 1
        elif value <= -axis_dead_zones['right_stick']:
            self.values['horizontal'] = -1
        else:
            self.values['horizontal'] = 0

    def set_vertical_arrow(self, value: float):
        if value >= axis_dead_zones['right_stick']:
            self.values['vertical'] = 1
        elif value <= -axis_dead_zones['right_stick']:
            self.values['vertical'] = -1
        else:
            self.values['vertical'] = 0
    
    def run(self):
        while self.state['alive']:
            if self.state['sleep']:
                sleep(0.1)
                continue

            if self.values['horizontal'] == 1:
                press_and_release_key('right')
            elif self.values['horizontal'] == -1:
                press_and_release_key('left')

            if self.values['vertical'] == 1:
                press_and_release_key('up')
            elif self.values['vertical'] == -1:
                press_and_release_key('down')
            
            sleep(0.25)


class Locker(Listener):
    """
        Locker class that locks gamepad states untill performing combination again.
        while right and left triggers are fully pressed, press right stick and wait for 1.5 seconds before releasing.
    """

    def __init__(self, state: dict, vibration_function: callable):
        self.state: dict = state
        self.right_trigger: bool = False
        self.left_trigger: bool = False
        self.last_press_time: float = 0
        self.last_interrupt_time: float = 0
        self.vibration_function: callable = vibration_function

    def button_pressed(self, button: str):
        if self.right_trigger and self.left_trigger and button == 'RSTICK':
            self.last_press_time = time()
    
    def button_released(self, button: str):
        if self.right_trigger and self.left_trigger and button == 'RSTICK' and time() - self.last_press_time > 1.5 and time() - self.last_interrupt_time > 1.0:
            self.last_interrupt_time = time()
            self.state['interrupt'] = not self.state['interrupt']
            self.vibration_function(1, 1, 0.4)
            print('Interrupt:', self.state['interrupt'])
            
    def axis_moved(self, axis: str, value: int):
        if axis == 'left_t' and value == 255:
            self.left_trigger = True
        elif axis == 'left_t' and value < 255:
            self.left_trigger = False
        
        if axis == 'right_t' and value == 255:
            self.right_trigger = True
        elif axis == 'right_t' and value < 255:
            self.right_trigger = False

