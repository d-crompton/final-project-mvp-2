# Class for Suspicious Device Objects
class SuspiciousDevice:
    # Constructor
    def __init__(self, last_ip, mac, manufacturer, os):
        self.last_ip = last_ip
        self.mac = mac
        self.manufacturer = manufacturer
        self.os = os
        self.type = "suspicious"

    # Additional Functions
    # Setters
    def set_last_ip(self, last_ip):
        self.last_ip = last_ip

    def set_mac(self, mac):
        self.mac = mac

    def set_manufacturer(self, manufacturer):
        self.manufacturer = manufacturer

    def set_os(self, os):
        self.os = os

    # Getters
    def get_last_ip(self):
        return self.last_ip

    def get_mac(self):
        return self.mac

    def get_manufacturer(self):
        return self.manufacturer

    def get_os(self):
        return self.os

    def get_type(self):
        return self.type
