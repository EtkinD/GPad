from inputs import devices
from Controller.Controller import Controller
from defaultlistener import DefaultListener

controllers: list[Controller] = []


def main():
    count = 0
    for device in devices:
        if str(device) == 'Microsoft X-Box 360 pad':
            # State manager for the controller.
            state = {'alive': True, 'sleep': False, 'interrupt': False}
            controllers.append(Controller(device, count, state, DefaultListener(state, count, device.set_vibration)))
            count += 1
    
    for controller in controllers:
        controller.join()
    if count == 0:
        input('No controller found.\nPress enter to exit.')
        exit(0)


if __name__ == "__main__":
    main()
else:
    print('main.py is not supposed to be imported.')
    exit(0)
