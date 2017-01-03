from machine import I2C, Pin
import time

__version__ = '0.1.0'
__author__ = 'Roberto Sánchez'
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"


class SHT30():
    """
    SHT30 sensor driver in pure python based on I2C bus
    
    References: 
    * https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/2_Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Datasheet_digital.pdf
    * https://www.wemos.cc/sites/default/files/2016-11/SHT30-DIS_datasheet.pdf
    * https://github.com/wemos/WEMOS_SHT3x_Arduino_Library
    * https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/11_Sample_Codes_Software/Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Sample_Code_V2.pdf
    """
    NO_ERROR = None
    BUS_ERROR = 0x01  # Sensor is not correctly connected
    DATA_ERROR = 0x02 # Data from Sensor is not valid (usually It's all 0x00). Review the sensor connection.
    CRC_ERROR = 0x03  # CRC code from sensor is not valid

    POLYNOMIAL = 0x131  # P(x) = x^8 + x^5 + x^4 + 1 = 100110001

    ALERT_PENDING_MASK = 0x8000 # 15
    HEATER_MASK = 0x2000        # 13
    RH_ALERT_MASK = 0x0800		# 11
    T_ALERT_MASK = 0x0400		# 10
    RESET_MASK = 0x0010	        # 4
    CMD_STATUS_MASK = 0x0002	# 1
    WRITE_STATUS_MASK = 0x0001	# 0

    # I2C address B 0x45 ADDR (pin 2) connected to VDD
    ADDRESS = 0x45
    # MSB = 0x2C LSB = 0x06 Repeatability = High, Clock stretching = enabled
    MEASURE_CMD = b'\x2C\x10'
    STATUS_CMD = b'\xF3\x2D'
    RESET_CMD = b'\x30\xA2'
    CLEAR_STATUS_CMD = b'\x30\x41'
    ENABLE_HEATER_CMD = b'\x30\x6D'
    DISABLE_HEATER_CMD = b'\x30\x66'

    def __init__(self, scl_pin=5, sda_pin=4, delta_temp = 0.0, delta_hum = 0.0):
        self.scl = Pin(scl_pin)
        self.sda = Pin(sda_pin)
        self.i2c = I2C(scl=self.scl, sda=self.sda)
        self.last_error = None
        self.set_delta(delta_temp, delta_hum)
        time.sleep(0.1)
    
    def init(self, scl_pin=5, sda_pin=4):
        """
        Init the I2C bus using the new pin values
        """
        self.scl = Pin(scl_pin)
        self.sda = Pin(sda_pin)
        self.i2c.init(scl=self.scl, sda=self.sda)
    
    def is_present(self):
        """
        Return true if the sensor is correctly conneced, False otherwise
        """
        return SHT30.ADDRESS in self.i2c.scan()
    
    def set_delta(self, delta_temp = 0.0, delta_hum = 0.0):
        """
        Apply a delta value on the future measurements of temperature and/or humidity
        The units are Celsius for temperature and percent for humidity (can be negative values)
        """
        self.delta_temp = delta_temp
        self.delta_hum = delta_hum
    
    def _check_crc(self, data):
        # calculates 8-Bit checksum with given polynomial
        crc = 0xFF
        
        for b in data[:-1]:
            crc ^= b;
            for _ in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ SHT30.POLYNOMIAL;
                else:
                    crc <<= 1
        crc_to_check = data[-1]
        return crc_to_check == crc
    
    def send_cmd(self, cmd_request, response_size=6, read_delay=0.1):
        """
        Send a command to the sensor and read (optionally) the response
        The responsed data is validated by CRC
        """
        try:
            self.last_error = None
            self.i2c.start(); 
            self.i2c.writeto(SHT30.ADDRESS, cmd_request); 
            if not response_size:
                self.i2c.stop(); 	
                return SHT30.NO_ERROR
            time.sleep(read_delay)
            data = self.i2c.readfrom(SHT30.ADDRESS, response_size) # pos 2 and 5 are CRC
            self.i2c.stop(); 
            for i in range(response_size//3):
                if not self._check_crc(data[i*3:(i+1)*3]):
                    self.last_error = SHT30.CRC_ERROR
                    return None
            if data == bytearray(response_size):
                self.last_error = SHT30.DATA_ERROR
                return None
            return data
        except:
            self.last_error = SHT30.BUS_ERROR
            return None

    def clear_status(self):
        """
        Clear the status register
        """
        return self.send_cmd(SHT30.CLEAR_STATUS_CMD, None); 

    def reset(self):
        """
        Send a soft-reset to the sensor
        """
        return self.send_cmd(SHT30.RESET_CMD, None); 

    def status(self):
        """
        Get the sensor status register
        """
        data = self.send_cmd(SHT30.STATUS_CMD, 3); 

        if self.last_error:
            return None

        status_register = data[0] << 8 | data[1]
        return status_register
    
    def measure(self):
        """
        Get the temperature (T) and humidity (RH) measurement and return them.
        The units are Celsius and percent
        """
        data = self.send_cmd(SHT30.MEASURE_CMD, 6); 

        if self.last_error:
            return None, None

        temp_celsius = (((data[0] << 8 |  data[1]) * 175) / 0xFFFF) - 45 + self.delta_temp;
        humidity = (((data[3] << 8 | data[4]) * 100.0) / 0xFFFF) + self.delta_hum;
        return temp_celsius, humidity
    
