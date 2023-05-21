import sys
import numpy as np

from time import sleep, time

try:
    import smbus
    USEGPIO = True
except ModuleNotFoundError:
    USEGPIO = False

class Gyroscope():

    def __init__(self, debug=False):
        print("[ INFO ] Init gyro ... ", end='', flush=1, file=sys.stderr)
        self.__debug = debug
        self.__calibrated = False
        self.last_z = [0, 0, 0]
        self.last_t = [time(), time(), time()]
        if USEGPIO:
            self.bus = smbus.SMBus(1)
            self.bus.write_byte_data(0x68, 0x3E, 0x01)
            self.bus.write_byte_data(0x68, 0x16, 0x18)
            sleep(0.5)
            print("completed", file=sys.stderr)
            self.current_time = time()
            self.S_gz, self.gz, self.angle_z, self.avg_gz = 0, 0, 0, 0
            self.__calibrate__()
        else:
            print("\n[ ERROR ] No bus found", file=sys.stderr)        
            self.z = None


    def __calibrate__(self):
        print("[ INFO ] Get average gz ... ", end='', flush=1, file=sys.stderr)
        a_gz = np.zeros(5000)
        for i in range(len(a_gz)):
            a_gz[i] = self.__get_z__(a_gz[i - 1])
            # sleep(0.1)
        self.avg_gz = a_gz.mean()
        if self.__debug:
            print(a_gz)
            print(self.avg_gz)

        print(f" completed {self.avg_gz}.", file=sys.stderr)
        self.__calibrated = True


    def __get_z__(self, angle_z):
        if USEGPIO:
            try:
                data = self.bus.read_i2c_block_data(0x68, 0x1D, 6)
                z = data[4] * 256 + data[5]
                if z > 32767 :
                    z -= 65536
            except Exception as e:
                p = np.polyfit(self.last_t, self.last_z, 5)
                zp = np.poly1d(p)
                z = zp(time())
        else:
            z = None
        return z

    def __get_z_smooth__(self):
        if USEGPIO:
            dt = time() - self.current_time
            self.current_time = time()
            z = self.__get_z__(self.angle_z)
            self.S_gz += (z - self.avg_gz) * dt - self.gz
            self.gz = self.S_gz / 10
            self.angle_z += self.gz / 14.25
            self.last_z, self.last_z[-1] = self.last_z[1:] + self.last_z[:1], self.angle_z
            self.last_t, self.last_t[-1] = self.last_t[1:] + self.last_t[:1], time()
            if self.__debug:
                print('t, dt', self.current_time, dt)
                print('z', z)
                print('avg_gz', self.avg_gz)
                print('S_gz', self.S_gz)
                print('gz', self.gz)
                print('a', self.angle_z)
        else:
            self.angle_z = None
        return self.angle_z, z

    def get_z(self):
        return self.__get_z_smooth__()[0]

    def __repr__(self):
        if self.__calibrated:
            z, z_ = self.__get_z_smooth__()
        else:
            z = self.__get_z__()
            z_ = 0
        return f"{z} {z_} {self.avg_gz}"

if __name__ == '__main__':
    g = Gyroscope(debug=False)
    for i in range(1000):
        print(g.get_z())
        sleep(0.1)
