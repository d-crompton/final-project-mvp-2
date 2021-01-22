# Window opened from the Scanner Window
# Displays any saved Suspicious Devices
from tkinter import *
from Windows import Device_Info_Window
from Devices import Suspicious_Device
import File_Handler


class SuspiciousWindow:
    # Constructor
    def __init__(self):
        # Opening List File
        self.file = None
        self.devices = File_Handler.load_suspicious_file() # Used to store devices locally
        # Creating Window
        self.root = Tk()
        self.root.title("Suspicious Devices")
        self.root.geometry("300x350")
        self.root.resizable(0, 0)  # Disables Maximum button
        self.root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky="NSEW")
        frame.grid_columnconfigure(0, weight=1)  # Make column fill width
        title_lbl = Label(frame, text="Suspicious Devices").grid(row=0, padx=(10, 5), sticky="WE")
        # Frame Devices are entered into
        device_frame = Frame(frame, bg="#f0f0f5", height=260, width=260,
                             highlightbackground="black", highlightthickness=1)
        device_frame.grid(row=1, pady=10, padx=10, sticky="nsew")
        device_frame.grid_columnconfigure(0, weight=1)
        # device_frame.grid_rowconfigure(0, weight=1)
        device_frame.grid_propagate(0)
        row = 0
        for device in self.devices:
            # Creating Widgets for Device's frame
            inner_frame = Frame(device_frame, bg="#ffb3b3", highlightbackground="black", highlightthickness=1)
            inner_frame.grid(row=row, sticky="WE")
            inner_frame.grid_columnconfigure(0, weight=9)
            inner_frame.grid_columnconfigure(1, weight=1)
            mac_label = Label(inner_frame, text=device.get_mac(), bg="#ffb3b3").grid(row=0, column=0, sticky="W")
            manufacturer_label = Label(inner_frame, text=device.get_manufacturer(), bg="#ffb3b3")
            manufacturer_label.grid(row=1, column=0, sticky="W")
            info_button = Button(inner_frame, text="Info", command=lambda device=device: self.info_button(device))
            info_button.grid(row=0, rowspan=2, column=1, sticky="NSEW")
            row += 1
        return_btn = Button(frame, text="Return", bg="#669999", command=self.root.destroy).grid(row=2, padx=10, sticky="SWE")
        self.root.mainloop()

    def info_button(self, device):
        self.root.destroy()
        window = Device_Info_Window.InfoWindow(device, "suspicious_list")
