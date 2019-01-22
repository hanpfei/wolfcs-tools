#!/usr/bin/env python3

import curses
import datetime
import socket
import struct
import sys
import time
import usb.core

WIFI      = 'Wifi'
BLUETOOTH = 'Bluetooth'
USB       = 'Usb'

STD       = 'STD'                     # reply if global_mem, wait for reply
ASYNC     = 'ASYNC'                   # reply if global_mem, never wait for reply
SYNC      = 'SYNC'                    # always with reply, always wait for reply


## USB configuration
ID_VENDOR_LEGO = 0x0694
ID_PRODUCT_EV3 = 0x0005
EP_IN  = 0x81
EP_OUT = 0x01


DIRECT_COMMAND_REPLY = b'\x00'
DIRECT_COMMAND_NO_REPLY = b'\x80'


opNop = b'\x01'
opCom_Set = b'\xD4'
opSound = b'\x94'
opSound_Ready = b'\x96'
opUI_Write = b'\x82'
opUI_Draw = b'\x84'
opTimer_Wait = b'\x85'
opTimer_Ready = b'\x86'
opFile = b'\xC0'
opProgram_Start = b'\x03'
opUI_Button = b'\x83'

opOutput_Power = b'\xA4'
opOutput_Start = b'\xA6'
opOutput_Stop = b'\xA3'
opOutput_Speed = b'\xA5'

Motor_A = 1
Motor_B = 2
Motor_C = 4
Motor_D = 8

cmdSet_BrickName = b'\x08'
cmdSound_Play = b'\x02'
cmdSound_Repeat = b'\x03'
cmdSound_Break = b'\x00'
cmdSound_PlayTone = b'\x01'
cmdUI_LED = b'\x1B'
cmdUIDraw_Update = b'\x00'
cmdUIDraw_Topline = b'\x12'
cmdUIDraw_FillWindow = b'\x13'
cmdUIDraw_BmpFile = b'\x1C'
cmdUIDraw_Line = b'\x03'
cmdUIButton_Press = b'\x05'
cmdUIButton_WaitForPress = b'\x03'

cmdFile_LoadImage = b'\x08'
PRGID_USER = b'\x01'

Button_No = b'\x00'
Button_Up = b'\x01'
Button_Enter = b'\x02'
Button_Down = b'\x03'
Button_Right = b'\x04'
Button_Left = b'\x05'
Button_Back = b'\x06'
Button_Any = b'\x07'


debugMode_Normal = b'\x00'

UI_LED_OFF = b'\x00'
UI_LED_GREEN = b'\x01'
UI_LED_RED = b'\x02'
UI_LED_ORANGE = b'\x03'
UI_LED_GREEN_FLASHING = b'\x04'
UI_LED_RED_FLASHING = b'\x05'
UI_LED_ORANGE_FLASHING = b'\x06'
UI_LED_GREEN_PULSE = b'\x07'
UI_LED_RED_PULSE = b'\x08'
UI_LED_ORANGE_PULSE = b'\x09'


def LCX(value: int) -> bytes:
    if value >= -32 and value < 0:
        # -32 + bit_mode[0:4] = value
        # bit_mode[0:4] = 32 + value
        # bit_mode[0:5] = 32 + (32 + value)
        return struct.pack('b', 0x3F & (value + 64))
    elif value >= 0 and value < 32:
        return struct.pack('b', value)
    elif value >= -127 and value <= 127:
        return b'\x81' + struct.pack('<b', value)
    elif value >= -32767 and value <= 32767:
        return b'\x82' + struct.pack('<h', value)
    else:
        return b'\x83' + struct.pack('<i', value)


def LVX(value: int) -> bytes:
    if value < 0:
        raise RuntimeError('No negative values allowed')
    elif value < 32: # LV0
        return struct.pack('b', (0x1F & value) | 0x40)
    elif value < 256: # LV1
        return b'\xC1' + struct.pack('<b', value)
    elif value < 65536: # LV2
        return b'\xC2' + struct.pack('<h', value)
    else: # LV4
        return b'\xC3' + struct.pack('<i', value)


def GVX(value: int) -> bytes:
    """create a GV0, GV1, GV2, GV4, dependent from the value"""
    if value   <     0:
        raise RuntimeError('No negative values allowed')
    elif value <    32:
        return struct.pack('<b', 0x60 | value)
    elif value <   256:
        return b'\xe1' + struct.pack('<b', value)
    elif value < 65536:
        return b'\xe2' + struct.pack('<h', value)
    else:
        return b'\xe3' + struct.pack('<i', value)


def LCS(value : str) -> bytes:
    retVal = b''.join([
        b'\x84',
        str.encode(value),
        b'\x00'
    ])
    return retVal


class EV3():
    def __init__(self, protocol: str=None, host: str=None, verbosity: bool=True, ev3_obj=None):
        assert ev3_obj or protocol, 'Either protocol or ev3_obj needs to be given'

        assert protocol in [BLUETOOTH, WIFI, USB], 'Protocol ' + protocol + ' is not valid'

        self._protocol = protocol
        self._socket = None
        self._device = None
        self._msg_cnt = 1
        self._verbosity = verbosity
        self._sync_mode = STD

        if protocol == BLUETOOTH:
            self.connect_with_bluetooth(host)
        elif protocol == USB:
            self.connect_with_usb(host)


    def __del__(self):
        if self._socket is not None and isinstance(self._socket, socket.socket):
            self._socket.close()


    def connect_with_bluetooth(self, host: str):
        connect_start_time = time.time()

        self._socket = socket.socket(
            socket.AF_BLUETOOTH,
            socket.SOCK_STREAM,
            socket.BTPROTO_RFCOMM
        )
        self._socket.connect((host, 1))

        connect_time = time.time() - connect_start_time

        if (self._verbosity):
            print("Bluetooth connect time: " + str(connect_time) + " seconds\n")


    def connect_with_usb(self, host:str):
        connect_start_time = time.time()

        self._device = usb.core.find(idVendor=ID_VENDOR_LEGO, idProduct=ID_PRODUCT_EV3)
        if self._device is None:
            raise RuntimeError("No Lego EV3 found")
        self._device.reset()
        serial_number = usb.util.get_string(self._device, self._device.iSerialNumber)
        # if serial_number.upper() != host.replace(':', '').upper():
        #     raise ValueError('found ev3 but not ' + host)
        if self._device.is_kernel_driver_active(0) is True:
            self._device.detach_kernel_driver(0)
        self._device.set_configuration()
        self._device.read(EP_IN, 1024, 100)

        connect_time = time.time() - connect_start_time

        if (self._verbosity):
            print("USB connect time: " + str(connect_time) + " seconds \n")


    def send_with_bluetooth(self, cmd: bytes, global_mem: int):
        self._socket.send(cmd)

        if (self._verbosity):
            print_hex('Sent', cmd)

        if (global_mem > 0):
            reply = self._socket.recv(5 + global_mem)
            if (self._verbosity):
                print_hex('Recv', reply)
        return reply


    def send_with_usb(self, cmd: bytes, global_mem: int):
        self._device.write(EP_OUT, cmd, 100)

        if (self._verbosity):
            print_hex('Sent', cmd)

        reply = None
        if (global_mem > 0):
            reply = self._device.read(EP_IN, 1024, 100)[0:5 + global_mem]
            if (self._verbosity):
                print_hex('Recv', reply)
        return reply


    def send_direct_cmd(self, ops: bytes, local_mem: int=0, global_mem: int=0, sync_mode: str=STD) -> bytes:
        send_start_time = time.time()

        cur_sync_mode = sync_mode
        if (global_mem > 0 and cur_sync_mode == STD):
            cmd_type = DIRECT_COMMAND_REPLY
        elif (cur_sync_mode == SYNC):
            cmd_type = DIRECT_COMMAND_REPLY
        else:
            cmd_type = DIRECT_COMMAND_NO_REPLY

        cmd = b''.join([
            struct.pack('<h', len(ops) + 5),
            struct.pack('<h', self._msg_cnt),
            cmd_type,
            struct.pack('<h', local_mem*1024 + global_mem),
            ops
        ])

        reply = None
        if self._protocol == BLUETOOTH:
            reply = self.send_with_bluetooth(cmd, global_mem)
        elif self._protocol == USB:
            reply = self.send_with_usb(cmd, global_mem)

        send_time = time.time() - send_start_time

        if self._verbosity:
            print("\nMessage send time: " + str(send_time) + " seconds")

        self._msg_cnt = self._msg_cnt + 1
        return reply


    def set_brick_name(self, brick_bame):
        ops = b''.join([
            opCom_Set,
            cmdSet_BrickName,
            LCS(brick_bame)
        ])

        self.send_direct_cmd(ops)


    def play_sound(self, volume: int, filepath: str):
        ops = b''.join([
            opSound,
            cmdSound_Play,
            LCX(volume),
            LCS(filepath)
        ])
        self.send_direct_cmd(ops)


    def play_sound_repeat(self, volume: int, filepath: str):
        ops = b''.join([
            opSound,
            cmdSound_Repeat,
            LCX(volume),
            LCS(filepath)
        ])
        self.send_direct_cmd(ops)


    def play_sound_break(self):
        ops = b''.join([
            opSound,
            cmdSound_Break
        ])
        self.send_direct_cmd(ops)


    def play_sound_tone(self, volume: int, freq: int, duration: int):
        ops = b''.join([
            opSound,
            cmdSound_PlayTone,
            LCX(volume),
            LCX(freq),
            LCX(duration)
        ])
        self.send_direct_cmd(ops)


    def start_program_cont_cmd(self, exe_file_path: str):
        ops = b''.join([
            opFile,
            cmdFile_LoadImage,
            PRGID_USER,
            LCS(exe_file_path),
            LVX(0),
            LVX(4),

            opProgram_Start,
            PRGID_USER,
            LVX(0),
            LVX(4),
            debugMode_Normal
        ])

        ret = self.send_direct_cmd(ops = ops, local_mem=8)

        # ops = b''.join([
        #     opProgram_Start,
        #     PRGID_USER,
        #     ret,
        #     debugMode_Normal
        # ])
        # ret = self.send_direct_cmd(ops = ops)

    def start_program(self, exe_file_path: str):
        ops = b''.join([
            opFile,
            cmdFile_LoadImage,
            PRGID_USER,
            LCS(exe_file_path),
            GVX(0),
            GVX(4)
        ])

        ret = self.send_direct_cmd(ops=ops, global_mem=8)

        ops = b''.join([
            opProgram_Start,
            PRGID_USER,
            GVX(0),
            GVX(4),
            debugMode_Normal
        ])
        ret = self.send_direct_cmd(ops = ops)


    def shutdown_brick(self):
        ops = b''.join([
            opUI_Button,
            cmdUIButton_Press,
            Button_Back,

            opUI_Button,
            cmdUIButton_WaitForPress,

            opUI_Button,
            cmdUIButton_Press,
            Button_Right,

            opUI_Button,
            cmdUIButton_WaitForPress,

            opUI_Button,
            cmdUIButton_Press,
            Button_Enter,
        ])

        self.send_direct_cmd(ops=ops)

    def start_motor(self):
        ops = b''.join([
            opOutput_Power,
            LCX(0),
            struct.pack('b', Motor_A | Motor_D),
            LCX(50),

            opOutput_Start,
            LCX(0),
            struct.pack('b', Motor_A | Motor_D)
        ])
        self.send_direct_cmd(ops=ops)


    def start_motor_with_speed(self, speed: int):
        ops = b''.join([
            opOutput_Speed,
            LCX(0),
            struct.pack('b', Motor_A | Motor_D),
            LCX(speed),

            opOutput_Start,
            LCX(0),
            struct.pack('b', Motor_A | Motor_D)
        ])
        self.send_direct_cmd(ops=ops)


    def stop_motor(self):
        ops = b''.join([
            opOutput_Stop,
            LCX(0),
            struct.pack('b', Motor_A | Motor_D),
            LCX(0)
        ])
        self.send_direct_cmd(ops=ops)


def print_hex(desc: str, data: bytes) -> None:
    now = datetime.datetime.now().strftime('%H:%M:%S.%f')
    print(now + " " + desc + ' 0x|' + ':'.join('{:02X}'.format(byte) for byte in data) + '|')


def test_usb_with_noop():
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')
    ops_nothing = opNop
    my_ev3.send_direct_cmd(ops_nothing, 16, 6)


def test_bluetooth_with_noop():
    print("\n\nBluetooth: ")
    my_ev3 = EV3(protocol=BLUETOOTH, host='00:16:53:60:25:91')
    ops_nothing = opNop
    my_ev3.send_direct_cmd(ops_nothing, 16, 6)


def play_triad_c_test():
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')

    ops = b''.join([
        opSound,
        cmdSound_PlayTone,
        LCX(1),
        LCX(262),
        LCX(500),
        opSound_Ready,

        opSound,
        cmdSound_PlayTone,
        LCX(1),
        LCX(330),
        LCX(500),
        opSound_Ready,

        opSound,
        cmdSound_PlayTone,
        LCX(1),
        LCX(392),
        LCX(500),
        opSound_Ready,

        opSound,
        cmdSound_PlayTone,
        LCX(2),
        LCX(523),
        LCX(1000),
    ])

    my_ev3.send_direct_cmd(ops)


def play_triad_c_with_leds_test():
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')

    ops = b''.join([
        opUI_Write,
        cmdUI_LED,
        UI_LED_RED,

        opSound,
        cmdSound_PlayTone,
        LCX(1),
        LCX(262),
        LCX(500),
        opSound_Ready,

        opUI_Write,
        cmdUI_LED,
        UI_LED_GREEN,

        opSound,
        cmdSound_PlayTone,
        LCX(1),
        LCX(330),
        LCX(500),
        opSound_Ready,

        opUI_Write,
        cmdUI_LED,
        UI_LED_ORANGE,

        opSound,
        cmdSound_PlayTone,
        LCX(1),
        LCX(392),
        LCX(500),
        opSound_Ready,

        opUI_Write,
        cmdUI_LED,
        UI_LED_GREEN_FLASHING,

        opSound,
        cmdSound_PlayTone,
        LCX(2),
        LCX(523),
        LCX(1000),
        cmdSound_PlayTone,

        opUI_Write,
        cmdUI_LED,
        UI_LED_GREEN
    ])

    my_ev3.send_direct_cmd(ops)


def draw_test():
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')
    ops = b''.join([
        opUI_Draw,
        cmdUIDraw_Topline,
        LCX(0),

        opUI_Draw,
        cmdUIDraw_BmpFile,
        LCX(1),
        LCX(0),
        LCX(0),
        LCS("../apps/Motor Control/MotorCtlAD.rgf"),

        opUI_Draw,
        cmdUIDraw_Update
    ])

    my_ev3.send_direct_cmd(ops)

    time.sleep(5)

    ops = b''.join([
        opUI_Draw,
        cmdUIDraw_Topline,
        LCX(1),

        opUI_Draw,
        cmdUIDraw_FillWindow,
        LCX(0),
        LCX(0),
        LCX(0),

        opUI_Draw,
        cmdUIDraw_Update
    ])

    my_ev3.send_direct_cmd(ops)


def timer_test():
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')

    ops = b''.join([
        opUI_Draw,
        cmdUIDraw_Topline,
        LCX(0), # DISABLE,

        opUI_Draw,
        cmdUIDraw_FillWindow,
        LCX(0), # COLOR
        LCX(0), # Y0
        LCX(0), # Y1

        opUI_Draw,
        cmdUIDraw_Update,

        opTimer_Wait,
        LCX(1000), # TIME, 1 seconds
        LVX(0), # TIMER

        opTimer_Ready,
        LVX(0),

        opUI_Draw,
        cmdUIDraw_Line,
        LCX(1),  # COLOR
        LCX(2),  # X0
        LCX(125),  # Y0
        LCX(88),  # X1
        LCX(2),  # Y1

        opUI_Draw,
        cmdUIDraw_Update,

        opTimer_Wait,
        LCX(500),  # TIME, 1 seconds
        LVX(0),  # TIMER

        opTimer_Ready,
        LVX(0),

        opUI_Draw,
        cmdUIDraw_Line,
        LCX(1),  # COLOR
        LCX(88),  # X0
        LCX(2),  # Y0
        LCX(175),  # X1
        LCX(125),  # Y1

        opUI_Draw,
        cmdUIDraw_Update,

        opTimer_Wait,
        LCX(500),  # TIME, 1 seconds
        LVX(0),  # TIMER

        opTimer_Ready,
        LVX(0),

        opUI_Draw,
        cmdUIDraw_Line,
        LCX(1),  # COLOR
        LCX(175),  # X0
        LCX(125),  # Y0
        LCX(2),  # X1
        LCX(125),  # Y1

        opUI_Draw,
        cmdUIDraw_Update
    ])

    my_ev3.send_direct_cmd(ops, local_mem=4)


def start_program_test():
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')
    my_ev3.start_program('../apps/Motor Control/Motor Control.rbf')


def shutdown_test():
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')
    my_ev3.shutdown_brick()


def start_motor_test():
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')
    my_ev3.start_motor()

    time.sleep(1.5)

    my_ev3.stop_motor()


def start_motor_with_speed_test(speed: int):
    my_ev3 = EV3(protocol=USB, host='00:16:53:60:25:91')
    my_ev3.start_motor_with_speed(speed)

    time.sleep(1)

    my_ev3.stop_motor()


speed = 0
turn  = 0
stdscr = None
myEV3 = None


def move(speed: int, turn: int) -> None:
    global myEV3, stdscr
    stdscr.addstr(5, 0, 'speed: {}, turn: {}      '.format(speed, turn))
    if turn > 0:
        speed_right = speed
        speed_left  = round(speed * (1 - turn / 100))
    else:
        speed_right = round(speed * (1 + turn / 100))
        speed_left  = speed
    ops = b''.join([
        opOutput_Speed,
        LCX(0),                       # LAYER
        LCX(Motor_A),              # NOS
        LCX(speed_right),             # SPEED
        opOutput_Speed,
        LCX(0),                       # LAYER
        LCX(Motor_D),              # NOS
        LCX(speed_left),              # SPEED
        opOutput_Start,
        LCX(0),                       # LAYER
        LCX(Motor_A + Motor_D)  # NOS
    ])
    myEV3.send_direct_cmd(ops)

    time.sleep(0.1)
    stop()

def stop() -> None:
    global myEV3, stdscr
    stdscr.addstr(5, 0, 'vehicle stopped                         ')
    ops = b''.join([
        opOutput_Stop,
        LCX(0),                       # LAYER
        LCX(Motor_A + Motor_D), # NOS
        LCX(0)                        # BRAKE
    ])
    myEV3.send_direct_cmd(ops)

def react(c):
    global speed, turn
    if c in [ord('q'), 27, ord('p')]:
        stop()
        curses.endwin()
        sys.exit(0)
        return
    elif c == curses.KEY_LEFT:
        turn = 60
        turn = min(turn, 200)
    elif c == curses.KEY_RIGHT:
        turn = -60
        turn = max(turn, -200)
    elif c == curses.KEY_UP:
        speed = 50
        speed = min(speed, 100)
    elif c == curses.KEY_DOWN:
        speed = -50
        speed = max(speed, -100)

    move(speed, turn)


def main(window) -> None:
    global stdscr

    stdscr = window
    stdscr.clear()  # print introduction
    stdscr.refresh()

    stdscr.addstr(0, 0, 'Use Arrows to navigate your EV3-vehicle')
    stdscr.addstr(1, 0, 'Pause your vehicle with key <p>')
    stdscr.addstr(2, 0, 'Terminate with key <q>')

    while True:
        c = stdscr.getch()
        if c in [ord('q'), 27]:
            react(c)
            break
        elif c in [ord('p'),
                   curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            react(c)


def remote_control_test():
    global myEV3
    global stdscr

    myEV3 = EV3(protocol=USB, host='00:16:53:60:25:91', verbosity=False)

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    stdscr.keypad(True)
    curses.wrapper(main)


if __name__ == '__main__':
    # myEV3 = EV3(protocol=USB, host='00:16:53:60:25:91')
    # myEV3.stop_motor()
    play_triad_c_with_leds_test()
    # remote_control_test()
