import logging
from time import sleep

from serial import Serial
from serial.serialutil import SerialException

log = logging.getLogger(__name__)

# these codes are for bluetooth
# hint: please check the function "sleep". how does it work?


class Bluetooth:
    """
    The Bluetooth class is used to connect to the Arduino via Bluetooth.
    """

    def __init__(self):
        self.serial = Serial()
        self.rt = ""
        
    def waiting(self) -> bool:
        return self.serial.in_waiting
    
    def do_connect(self, port: str):
        self.serial.close()
        log.info(f"Connecting to {port}...")
        try:
            self.serial = Serial(port, 9600, timeout=2)
            log.info("Success\n")
        except SerialException:
            log.warning("Fail to connect\n")
            return False
        return True

    def disconnect(self):
        self.serial.close()

    def serial_write_string(self, data: str):
        send = data.encode("utf-8")
        self.serial.write(send)

    def serial_write_bytes(self, data: bytes):
        self.serial.write(data)

    # def serial_read_char(self):
    #     waiting = self.serial.in_waiting
    #     if waiting >= 0:
    #         rv = self.rt = self.serial.read(waiting)
    #         return rv
    #     return ""

    def serial_read_byte(self):
        sleep(0.05)
        waiting = self.serial.in_waiting
        rv = self.serial.read(waiting)
        if rv:
            self.serial.reset_input_buffer()
            return rv
        else:
            return 0
