from inputs import devices
from Controller.Controller import Controller
from defaultlistener import DefaultListener

controllers: list[Controller] = []
count = 0


def create_controller(device):
    """
    Creates new gamepad.
    """
    global count
    # State manager for the controller.
    state = {'alive': True, 'sleep': False, 'interrupt': False}
    controllers.append(Controller(device, count, state, DefaultListener(state, count, device.set_vibration)))
    count += 1


def main():
    for device in devices:
        if device.device_type == 'joystick':
            create_controller(device)

    if count == 0:
        input('No controller found.\nPress enter to exit.')
        exit(0)

    for controller in controllers:
        controller.join()


if __name__ == "__main__":
    from LogHandler.logger import redirect_error
    redirect_error()
    main()
