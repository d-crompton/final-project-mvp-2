# Trusted Device - Child of Device
from Devices import Device


class TrustedDevice(Device.Device):
    # Constructor
    def __init__(self, last_ip, mac, manufacturer, os, name):
        super().__init__(last_ip, mac, manufacturer, os)
        self.name = name
        self.type = "trusted"

    # Additional Functions
    # Setters
    def set_name(self, name):
        self.name = name

    # Getters
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type
