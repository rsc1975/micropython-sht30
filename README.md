#SHT30 Sensor driver in micropython

Micropython driver for [SHT30 Shield](https://www.wemos.cc/product/sht30-shield.html) for [Wemos D1 Mini (and PRO)](https://www.wemos.cc/product/d1-mini-pro.html).

##Motivation
The SHT30 shield for ESP8266 board Wemos D1 Mini has an Arduino driver but not a micropython one.

##References:

* [Sensor Datasheet](https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/2_Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Datasheet_digital.pdf)
* [Arduino driver](https://github.com/wemos/WEMOS_SHT3x_Arduino_Library)
* [SHT30 C Code Examples](https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/11_Sample_Codes_Software/Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Sample_Code_V2.pdf) from sensor manufacturer

##Examples of use:

###How to get the temperature and relative humidity:

The `SHT30#measure()` method returns a tuple with the temperature in celsius grades and the relative humidity in percentage.

```python
from sht30 import SHT30

sensor = SHT30()

temperature, humidity = sensor.measure()

print('Temperature:', temperature, 'ºC, RH:', humidity, '%')

```

###Check if shield is connected

```python
from sht30 import SHT30

sensor = SHT30()

print('Is connected:', sensor.is_present())

```


###Read sensor status

Check the [Sensor Datasheet](https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/2_Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Datasheet_digital.pdf) for further info about sensor status register
```python
from sht30 import SHT30

sensor = SHT30()

print('Status register:', bin(sensor.status()))
print('Single bit check, HEATER_MASK:', bool(sensor.status() & SHT30.HEATER_MASK))

```


###Error management

When the driver cannot access to the measurement it returns None values and the field `last_error` is set

```python
from sht30 import SHT30

sensor = SHT30()

t, h = sensor.measure()

if t is None:
    print('Error in measurement:', sensor.last_error)
    # Possible values: SHT20.DATA_ERROR, SHT20.BUS_ERROR, SHT20.CRC_ERROR

```
