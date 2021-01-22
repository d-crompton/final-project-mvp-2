# final-project-mvp-2
This project is the code for my Final Year Project's second Minimum Viable Product. 
The purpose of this product is to allow the User to scan their home network for connected device. The User is then able to determine whether a device is Trusted and give it a name or whether it is a Suspicious device. After the scan the User can see previously saved Devices. This iteration builds on the first MVP but requiring Users to enter an email address. After a network scan the User will be emailed a scan report including any devices found in that scan.

To run this program, launch the **Main.py** Python file.To run this program, launch the **Main.py** Python file.

In order for this program to work, you need to have **Nmap** installed (and added to the *Windows PATH variable*) as it is used for the network scanning functionality.
Nmap can be found here - https://nmap.org/download.html

This code was written in Python 3 and uses the following libraries/modules:
* email.mime - https://docs.python.org/3/library/email.mime.html
* python-nmap - http://xael.org/pages/python-nmap-en.html
* smtplib - https://docs.python.org/3/library/smtplib.html
* tkinter - https://docs.python.org/3/library/tkinter.html
* tkinter.messagebox - https://docs.python.org/3.9/library/tkinter.messagebox.html
* tkinter.simpledialog - https://docs.python.org/3.9/library/dialog.html
* tkinter.ttk - https://docs.python.org/3/library/tkinter.ttk.html

