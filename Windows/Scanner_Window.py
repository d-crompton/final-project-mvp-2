# Window appears after User submits email address
# Users scan their network on this window and open device lists
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import tkinter.messagebox
import tkinter.simpledialog
import nmap
import smtplib
from email.mime.text import MIMEText
import os
import File_Handler
from Devices import Device, Trusted_Device, Suspicious_Device
from Windows import Trusted_Window, Suspicious_Window, Device_Info_Window


class ScannerWindow:
    # Constructor
    def __init__(self, email):
        # Creating Arrays to store previously saved devices
        # Although defined here, cleared whenever files are loaded at the start of each scan
        self.curr_device = None  # Used when handling scanned devices
        self.trusted_devices = []  # List of Trusted_Device Objects
        self.suspicious_devices = []  # List of Suspicious Device Objects
        self.device_frame_row = 0  # Row used when adding devices to the device frame
        # Create Found Device Lists to pass to email function
        self.found_trusted = []
        self.found_suspicious = []
        # Creating Root Window
        root = Tk()
        root.title("Network Device Scanner")
        root.geometry("500x490")
        root.resizable(0, 0)  # Disables Maximum button
        # Set two Columns for structure
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        # ADDING ELEMENTS
        # Email title and Titles
        self.email = email  # Self property used with email function later
        curr_email_text = "Email: " + self.email
        email_lbl = Label(root, text=curr_email_text, pady=0).grid(row=0, column=0, pady=0, sticky="W")
        title_lbl = Label(root, pady=0, text="Home Network Scanner")
        title_lbl.grid(row=1, columnspan=2, pady=(0, 10), sticky="WE")
        # Scan Button
        button_bg = "#669999"  # Background Colour for Buttons
        scan_btn = Button(root, text="Scan Network", width=50, padx=5, pady=5, bg=button_bg, command=self.scan_button)
        scan_btn.grid(row=2, columnspan=2)
        # Progress Bar
        bar_style = ttk.Style()
        bar_style.theme_use('default')
        bar_style.configure("black.Horizontal.TProgressbar", background=button_bg)
        self.progress_bar = Progressbar(root, length=450, s="black.Horizontal.TProgressbar")
        self.progress_bar['value'] = 0
        self.progress_bar.grid(row=3, columnspan=2, padx=10, pady=5, sticky="WE")
        # Device Frame
        self.device_frame = Frame(root, bg="#f0f0f5", height=300, width=450,
                                  highlightbackground="black", highlightthickness=1)
        self.device_frame.grid(row=4, columnspan=2, pady=(5, 10), padx=10, sticky="nsew")
        # Setting initial weighting
        self.device_frame.grid_columnconfigure(0, weight=1)
        self.device_frame.grid_columnconfigure(0, weight=1)
        self.device_frame.grid_propagate(0)  # Prevent children re-shaping frame
        # Buttons at bottom
        trusted_btn = Button(root, text="Trusted Devices", width=30, pady=5, bg=button_bg,
                             command=self.open_trusted_window)
        trusted_btn.grid(row=5)
        suspect_btn = Button(root, text="Suspicious Devices", width=30, pady=5, bg=button_bg,
                             command=self.open_suspicious_window)
        suspect_btn.grid(row=5, column=1)
        # Main Loop - No code after this
        root.mainloop()

    # ADDITIONAL FUNCTIONS
    # Function that runs when the scan button is pressed
    def scan_button(self):
        # Populate device lists
        self.trusted_devices = File_Handler.load_trusted_file()
        self.suspicious_devices = File_Handler.load_suspicious_file()
        # Run code to remove devices currently in frame (loop through devices, destroy)
        for child in self.device_frame.winfo_children():
            child.destroy()
        self.device_frame_row = 0  # Sets row back to 0
        # Set Progress bar back to zero
        self.progress_bar['value'] = 5  # Update Progress Bar to show User something's happening
        # Run Quick Scan to get available hosts before deeper OS Scan
        nm = nmap.PortScanner()
        try:
            quick_scan = nm.scan(hosts='192.168.0.1/24', arguments='-F')
            hosts = nm.all_hosts()
            progress_per_host = (95 / len(hosts))  # How far to increase progress bar after each hosts' OS Scan
        except nmap.PortScannerError:  # Error raised in not on a network, or having connectivity issues
            print("Port Scan Error")
            warning = tkinter.messagebox.showwarning("Port Scan Error",
                                                     "Unable to scan network, please check network connection")
            return  # Exit function if unable to scan
        for host in hosts:  # Carry out OS Scan on each found device
            os_scan = nm.scan(hosts=host, arguments='-O -F')
            try:  # Try Getting Mac
                mac = os_scan['scan'][host]['addresses']['mac']
            except KeyError:  # Error if the dictionary key is not available
                mac = "Mac Address not Available"
            try:  # Try Getting Manufacturer
                manu = os_scan['scan'][host]['vendor'][mac]
            except KeyError:
                manu = "Manufacturer not Available"

            try:  # Try Getting OS
                op_sys = os_scan['scan'][host]['osmatch'][0]['name']  # 'os' is already used by Python
            except KeyError:
                op_sys = "OS not Available"
            except IndexError:
                op_sys = "OS not Available"
            self.curr_device = Device.Device(host, mac, manu, op_sys)
            # Checking Trusted Device List
            if self.check_trusted_list():
                # Creating new Trusted Device
                self.add_progress(progress_per_host)
                self.found_trusted.append(self.curr_device)
            # If not in Trusted Device List, check Suspicious List
            elif self.check_suspect_list():
                self.add_progress(progress_per_host)
                self.found_suspicious.append(self.curr_device)
                tkinter.messagebox.showwarning("Suspicious Device Found",
                                               "A device previously flagged as suspicious has been found on the network")
            else:  # If neither check trusted or suspicious devices return true
                self.add_progress(progress_per_host)
                self.pop_up_new_device()
            # Adding Device to Device Frame
            self.create_device_frame(self.curr_device)
        tkinter.messagebox.showinfo("Scan Finished", "Scan Finished")  # Message to let User know scan loop has ended
        # End of Scan Loop - Write device arrays to files
        File_Handler.write_trust_file(self.trusted_devices)
        File_Handler.write_suspicious_file(self.suspicious_devices)
        # Send Email to User
        self.send_email()

    # Function checking whether given device is already recognised as trusted
    def check_trusted_list(self):
        for device in self.trusted_devices:
            if self.curr_device.get_mac() == device.get_mac():
                device.set_last_ip(self.curr_device.get_last_ip())  # Update last known IP in case it changes
                print(self.curr_device.get_mac() + " is trusted")
                # Sets Current Device equal to the current trusted device
                self.curr_device = device
                return True
        # If Device isn't known, end of loop
        return False

    # Function checking whether given device is already recognised as suspicious
    def check_suspect_list(self):
        for device in self.suspicious_devices:
            if self.curr_device.get_mac() == device.get_mac():
                device.set_last_ip(self.curr_device.get_last_ip())  # Update last known IP in case it changes
                # Sets Current Device equal to the current trusted device
                self.curr_device = device
                return True
        # If Device isn't known, end of loop
        return False

    # Function to increase the scan's progress - include whether a device is trusted, suspect or new
    def add_progress(self, progress):
        self.progress_bar['value'] = self.progress_bar['value'] + progress

    # Function that handles the pop-up box that appears when a new device is found
    def pop_up_new_device(self):
        pop_up_message = "Do you trust this device:\n" + \
                         "MAC Address: " + self.curr_device.get_mac() + "\n" + \
                         "IP Address: " + self.curr_device.get_last_ip() + "\n" + \
                         "Manufacturer: " + self.curr_device.get_manufacturer() + "\n" + \
                         "OS: " + self.curr_device.get_os()
        trust_input = tkinter.messagebox.askquestion("New Device Found", pop_up_message)
        # If User says "yes" to trusting the device
        if trust_input == "yes":
            name_question_input = tkinter.messagebox.askquestion("New Device Found",
                                                                 "Do you want to give the trusted device a name?")
            if name_question_input == "yes":
                device_name = tkinter.simpledialog.askstring(title="New Device Found",
                                                             prompt="Enter the name for the new device")
            elif name_question_input == "no":
                device_name = "Trusted Device"  # If User doesn't give a name, just assign default name
                print("User didn't enter name")
            # Add Trusted Device to Trusted Devices list
            self.curr_device = Trusted_Device.TrustedDevice(self.curr_device.get_last_ip(),
                                                            self.curr_device.get_mac(),
                                                            self.curr_device.get_manufacturer(),
                                                            self.curr_device.get_os(),
                                                            device_name)
            self.found_trusted.append(self.curr_device)  # List for Email
            self.trusted_devices.append(self.curr_device)  # List to be stored
        # If User says "no" to trusting the device
        elif trust_input == "no":
            self.curr_device = Suspicious_Device.SuspiciousDevice(self.curr_device.get_last_ip(),
                                                                  self.curr_device.get_mac(),
                                                                  self.curr_device.get_manufacturer(),
                                                                  self.curr_device.get_os())
            self.found_suspicious.append(self.curr_device)  # List for Email
            self.suspicious_devices.append(self.curr_device)  # List to be stored

    # Function for creating Frame and adding it into the Device Frame
    def create_device_frame(self, device):
        # If trusted device, create green background, if suspicious - red
        if device.get_type() == "trusted":
            frame_bg = '#adebad'  # Light Green
        elif device.get_type() == "suspicious":
            frame_bg = "#ffb3b3"  # Red
        # Create Frame
        frame = Frame(self.device_frame, bg=frame_bg, highlightbackground="black", highlightthickness=1)
        frame.grid(row=self.device_frame_row, sticky="WE")
        # Elements inside this frame
        # If trusted device, display name, else display "Suspicious Device label"
        if device.get_type() == "trusted":
            device_name = device.get_name()
        elif device.get_type() == "suspicious":
            device_name = "Suspicious Device"
        name_lbl = Label(frame, text=device_name, bg=frame_bg).grid(row=0, column=0, sticky="W")
        host_lbl = Label(frame, text=device.get_last_ip(), bg=frame_bg).grid(row=1, column=0, sticky="W")
        manu_lbl = Label(frame, text=device.get_os(), bg=frame_bg).grid(row=2, column=0, sticky="W")
        frame.grid_columnconfigure(0, weight=9)
        frame.grid_columnconfigure(1, weight=1)
        info_btn = Button(frame, text="Info",
                          command=lambda curr_device=device: self.open_info_window(curr_device))
        info_btn.grid(row=0, column=1, rowspan=3, padx=2, pady=5, sticky="NESW")
        self.device_frame_row += 1

    # Device Information Button
    def open_info_window(self, device):
        window = Device_Info_Window.InfoWindow(device)

    # Button press that opens Trusted Devices Window
    def open_trusted_window(self):
        window = Trusted_Window.TrustedWindow()

    # Button press that opens Suspicious Devices Window
    def open_suspicious_window(self):
        window = Suspicious_Window.SuspiciousWindow()

    # Email Function - Runs at the end of Scan
    def send_email(self):
        # Remember to ALLOW LESS SECURE APPS on Gmail account for program to work
        # Define Message Content
        recipient = self.email
        subject = "Scan Report"
        # Getting Email Credentials from Environment Variables
        try:
            email_user = os.environ['MVP_EMAIL']
            email_pass = os.environ['MVP_PASS']
        except KeyError:
            print("Unable to get OS Environ Credentials")
        # Creating Body Message
        body = "Trusted Devices Found<br>"
        # Adding Trusted Devices found
        for device in self.found_trusted:
            body = body + ">" + device.get_name() + ", " + device.get_last_ip() + ", " + device.get_mac() + \
                  ", " + device.get_manufacturer() + ", " + device.get_os() + "<br>"
        # Break between lists
        body = body + "<br>Suspicious Devices Found<br>"
        # Adding Suspicious Devices found
        for devicee in self.found_suspicious:
            body = body + ">" + device.get_last_ip() + ", " + device.get_mac() + \
                   ", " + device.get_manufacturer() + ", " + device.get_os() + "<br>"
        # Make Message
        msg = MIMEText(body, 'html') # Define the body content AND that it will be HTML
        msg['Subject'] = subject
        msg['From'] = email_user
        msg['To'] = recipient
        # Attempt to get email credentials from IDE - stored in this format to hide credentials when upload to Github

        # Sending
        try:
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            smtp.login(email_user, email_pass)
            send = smtp.sendmail(email_user, recipient, msg.as_string())
            smtp.quit()
            print("Email Sent")
        # Different Exceptions
        except smtplib.SMTPHeloError:  # The Server didn't reply properly to the Helo Greeting
            print("Server didn't respond")
        except smtplib.SMTPAuthenticationError:  # The server didn't accept the Username/Password
            print("The server didn't accept the Username/Password combination")
        except:  # Catches any Errors I have missed
            print("Email Failed")
