import argparse
import json
import re 
import sys

from multiprocessing import Process, Queue
from queue import Empty
from serial import Serial, SerialException
from time import sleep, time

READ_UNTIL_CHARACTER = '<'

class SensorsProcess(Process):

    def __init__(self, q_cmd, q_result, debug=False):
        super().__init__()

        self.__do_debug = debug
        self.__set_initial_values()
        self.__set_arduino()
        self.__configure_queues(q_cmd, q_result)
        self.__init_state_dictionary()


    def __set_initial_values(self):
        settings = json.load(open('/home/pi/port.json'))
        self.__port = settings['port']
        self.__baudrate = settings['baudrate']
        self.__timeout = settings['timeout']
        self.__read_until_character = READ_UNTIL_CHARACTER
        self.__ser = None


    def __configure_queues(self, q_cmd, q_result):
        self.cmd = None
        self.q_cmd = q_cmd
        self.q_result = q_result


    def __set_arduino(self):
        try:
            self.__ser = Serial(self.__port, baudrate=self.__baudrate, timeout=self.__timeout)
        except SerialException as e:
            print("[ ERROR ] ", self.__port, 'failed with %s' % e)
            sys.exit(1)
        except UnicodeDecodeError as e:
            print("[ ERROR ] ", self.__port, 'failed with %s' % e)
            sys.exit(1)

    def __init_state_dictionary(self):
        self.state = {
            'frw_rgt_dst'       : None,
            'frw_lft_dst'       : None,
            'lft_frw_dst'       : None,
            'lft_bkw_dst'       : None,
            'rgt_frw_dst'       : None,
            'rgt_bkw_dst'       : None,
            'v_battery'         : None,
            'nc'                : None,
            'current_lft_motor' : None,
            'current_rgt_motor' : None,
            'frw_rgt_ik'        : None,
            'frw_lft_ik'        : None,
            'lft_ik'            : None,
            'rgt_ik'            : None,
            'bkw_ik'            : None,
        }

    def run(self):
        while 1:
            try:
                self.cmd = self.q_cmd.get(block=False)
                if self.cmd['action'] == 'EXIT':
                    self.__ser.close()
                    break
                elif self.cmd['action'] == 'state':
                    self.__get_state()
            except Empty:
                pass
            self.__update_state()

    def __get_state(self):
        self.q_result.put({**self.state})


    def __update_state(self):
        try:
            received  = self.__ser.read_until(self.__read_until_character).decode('ascii').replace('\n',' ')
            data = re.findall(r'(.*?)<', received)[-1]
            assert data, f'wrong packet has come ({received})!'
            parsed = [int(x) for x in re.findall(r'(\d+)',data)]
            self.state = {
                'frw_rgt_dst'       : parsed[0],
                'lft_frw_dst'       : parsed[1],
                'frw_lft_dst'       : parsed[2],
                'rgt_frw_dst'       : parsed[3],
                'rgt_bkw_dst'       : parsed[4],
                'lft_bkw_dst'       : parsed[5],
                'v_battery'         : round(parsed[6] * 0.0261489, 2),
                'nc'                : parsed[7],
                'current_lft_motor' : round(parsed[8] / 57.692307, 2),
                'current_rgt_motor' : round(parsed[9] / 57.692307, 2),
                'frw_lft_ik'        : 0 if parsed[10] else 1,
                'frw_rgt_ik'        : 0 if parsed[11] else 1,
                'bkw_lft_ik'        : 0 if parsed[12] else 1,
                'lft_frw_ik'        : 0 if parsed[13] else 1,
                'lft_bkw_ik'        : 0 if parsed[14] else 1,
                'bkw_rgt_ik'        : 0 if parsed[15] else 1,
                'rgt_bkw_ik'        : 0 if parsed[16] else 1,
                'rgt_frw_ik'        : 0 if parsed[17] else 1,
                }
        except Exception as e:
            if self.__do_debug: print(f"[ INFO ] {e}", file=sys.stderr)
            

if __name__ == '__main__':
    q_cmd, q_result = Queue(), Queue()
    sensors_proc = SensorsProcess(q_cmd, q_result, debug=1)
    sensors_proc.start()

    while 1:
        sleep(1)
        try:
            q_cmd.put({'action':'state'})
            print(time(), " ", q_result.get())
        except KeyboardInterrupt:
            break

    q_cmd.put({'action':'EXIT'})

    sensors_proc.join()
