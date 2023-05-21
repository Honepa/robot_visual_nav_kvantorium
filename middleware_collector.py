from gpio.lights import Lights
from multiprocessing import Process
from settings import SERVICES


class MiddleWareCollector():
    
    def __init__(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(True)
        except ModuleNotFoundError:
            GPIO = None
        self.gpio = GPIO
        self.pins = {
            'forward_left'  : 31,
            'forward_right' : 36,
            'backward_right': 38,
            'backward_left' : 40,
        }
        self.lights_process = Process(target=self.start_lights_app)
        self.lights_process.start()

    def start_lights_app(self):
        self.lights_app = Lights(__name__, self.gpio, self.pins)
        # print(self.lights_app.q_state)
        
        self.lights_app.run(host='0.0.0.0', port=SERVICES['ports']['lights'])
        
    def __del__(self):
        self.lights_process.join()
        try:
            self.gpio.cleanup()
        except AttributeError as e:
            print(e)


if __name__ == '__main__':
    
            