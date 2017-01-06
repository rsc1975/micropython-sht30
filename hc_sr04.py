
import pyb

# Pin configuration.
# WARNING: Do not use PA4-X5 or PA5-X6 as the echo pin without a 1k resistor.

class Ultrasonic:
    def __init__(self, tPin, ePin):
        self.triggerPin = tPin
        self.echoPin = ePin

        # Init trigger pin (out)
        self.trigger = pyb.Pin(self.triggerPin)
        self.trigger.init(pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.trigger.low()

        # Init echo pin (in)
        self.echo = pyb.Pin(self.echoPin)
        self.echo.init(pyb.Pin.IN, pyb.Pin.PULL_NONE)

    def distance_in_inches(self):
        return (self.distance_in_cm() * 0.3937)

    def distance_in_cm(self):
        start = 0
        end = 0

        # Create a microseconds counter.
        micros = pyb.Timer(2, prescaler=83, period=0x3fffffff)
        micros.counter(0)

        # Send a 10us pulse.
        self.trigger.high()
        pyb.udelay(10)
        self.trigger.low()

        # Wait 'till whe pulse starts.
        while self.echo.value() == 0:
            start = micros.counter()

        # Wait 'till the pulse is gone.
        while self.echo.value() == 1:
            end = micros.counter()

        # Deinit the microseconds counter
        micros.deinit()

        # Calc the duration of the recieved pulse, divide the result by
        # 2 (round-trip) and divide it by 29 (the speed of sound is
        # 340 m/s and that is 29 us/cm).
        dist_in_cm = ((end - start) / 2) / 29

        return dist_in_cm
