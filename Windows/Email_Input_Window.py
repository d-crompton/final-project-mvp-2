# Window that appears when the program is first launched
# Takes User's email address to send alerts to later
from tkinter import *
import tkinter.messagebox
from Windows import Scanner_Window


class EmailInputWindow:
    # Constructor
    def __init__(self):
        # Creating Window
        self.root = Tk()
        self.root.title("Please Enter Your Email")
        self.root.geometry("300x100")
        self.root.resizable(0, 0)  # Disables Maximum Button
        self.root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        frame = Frame(self.root)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky="NSEW")
        lbl1 = Label(frame, text="Please enter an Email").grid(row=0, sticky="WE")
        lbl2 = Label(frame, text="Scanner alerts will be sent to this address").grid(row=1, sticky="WE")
        self.input_txt = Text(frame, height=1)  # Set to self to be used by button function
        self.input_txt.grid(row=2, padx=10, sticky="WE")
        submit_btn = Button(frame, text="Submit", command=self.submit_button)
        submit_btn.grid(row=3, pady=10)
        # Main Loop - No Code after this
        self.root.mainloop()

    # Function runs when submit button is pressed
    def submit_button(self):
        # Retrieve value from text field
        email = self.input_txt.get("1.0", END)
        # Check if User has entered a value
        if email.strip() == "":
            warning = tkinter.messagebox.showwarning("No Email", "Please enter an email address")
        else:
            # Closing current window, opening the other
            self.root.destroy()  # Close Input Window - Include before creating scanner window
            scanner_window = Scanner_Window.ScannerWindow(email)
