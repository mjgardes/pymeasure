#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2021 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import (
    strict_discrete_set, strict_range
)

class BHK(Instrument):
    """ Kepco BHK series DC power supply


    .. code-block:: python

        source = BHK("GPIB::8")

        source.ramp_to_zero(1)               # Set output to 0 before enabling
        source.enable()                      # Enables the output
        source.current = 1                   # Sets a current of 1 A

    """

# 
    id = Instrument.measurement(
            "*IDN?", """ Reads the instrument identification """
    )

    VOLTAGE_RANGE = [0, 300]
    CURRENT_RANGE = [0, 0.6]

# Source
    output = Instrument.control(
        "OUTP?", "OUTP %d",
        """ A boolean property that turns on (True, 'on') or off (False, 'off') 
        the output of the function generator. Can be set. """,
        validator=strict_discrete_set,
        map_values=True,
        values={True: 1, 'on': 1, 'ON': 1, False: 0, 'off': 0, 'OFF': 0},
    )

    voltage = Instrument.control(
        "SOUR:VOLT?", "SOUR:VOLT %g",
        """ A floating point property that represents the output voltage
        setting of the power supply in Volts. This property can be set. """,
        validator=strict_range,
        values=VOLTAGE_RANGE
    )

    voltage = Instrument.control(
        "SOUR:VOLT?", "SOUR:VOLT %g",
        """ A floating point property that represents the output voltage
        setting of the power supply in Volts. This property can be set. """,
        validator=strict_range,
        values=VOLTAGE_RANGE
    )

    current = Instrument.control(
        "SOUR:CURR?", "SOUR:CURR %g",
        """ A floating point property that represents the output current of
        the power supply in Amps. This property can be set. """,
        validator=strict_range,
        values=CURRENT_RANGE
    )

    max_voltage = Instrument.control(
        "SOUR:VOLT:LIM?", "SOUR:VOLT:LIM %g",
        """ A floating point property that represents the maximum output
        voltage of the power supply in Volts. This property will be stored
        to flash memory. """,
        validator=strict_range,
        values=VOLTAGE_RANGE
    )

    max_current = Instrument.control(
        "SOUR:CURR:LIM?", "SOUR:CURR:MA %g",
        """ A floating point property that represents the maximum output
        current of the power supply in Amps. This property will be stored
        to flash memory. """,
        validator=strict_range,
        values=CURRENT_RANGE
    )

# Measure
    measure_voltage = Instrument.measurement(
        "MEAS:VOLT?",
        """ Measures the actual output voltage of the power supply in
        Volts. """,
    )

    measure_current = Instrument.measurement(
        "MEAS:CURR?",
        """ Measures the actual output current of the power supply in
        Amps. """,
    )

    measure_vi = Instrument.measurement(
        "MEAS:VOLT?; CURR?",
        """ Measures the actual output voltage and current of the power
        supply in volts and amps. """,
        get_process=lambda response: map(float, response.split(';'))
    )

# Status
    rsd = Instrument.measurement(
        "STAT:OPER:COND?",
        """ Returns the value of the Operation Condition Register. """,
    )

    mode = Instrument.measurement(
        "FUNC:MODE?",
        """ Returns VOLT if power supply operating in constant voltage
        mode, CURR for constant current mode. """,
    )

# Instr
    def __init__(self, resourceName, **kwargs):
        super(BHK, self).__init__(
            resourceName,
            "Kepco BHK Series DC source",
            **kwargs
        )

    def ramp_to_current(self, target_current, current_step=0.1):
        """
        Gradually increase/decrease current to target current.

        :param target_current: Float that sets the target current (in A)
        :param current_step: Optional float that sets the current steps
                             / ramp rate (in mA/s)
        """

        curr = self.current
        n = round(abs(curr - target_current) / current_step) + 1
        for i in linspace(curr, target_current, n):
            self.current = i
            sleep(0.1)

    def ramp_to_zero(self, current_step=0.1):
        """
        Gradually decrease the current to zero.

        :param current_step: Optional float that sets the current steps
                             / ramp rate (in A/s)
        """

        self.ramp_to_current(0, current_step)

    def shutdown(self):
        """
        Set the current to 0 A and disable the output of the power source.
        """
        #self.ramp_to_zero()
        self.output = "OFF"
