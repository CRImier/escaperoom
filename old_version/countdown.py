#!/usr/bin/env python
from string import zfill
from datetime import datetime, timedelta
from modbus import LaserAlarm

import Tkinter as tk

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes("-fullscreen", True)
        self.label = tk.Label(self, text="", width=10, font=("Segment7", 200))
        self.label.pack(anchor=tk.CENTER, expand=True)
        #self.button = tk.Button(self, text="FAIL", command=self.decrease)
        #self.button.pack()
        self.remaining = 0
        self.laser = LaserAlarm()
        self.laser.reset_state()
        self.countdown(40*60)
        self.check_laser()

    def decrease(self, amount=300):
        self.remaining -= amount

    def countdown(self, remaining = None):
        if remaining:
            self.remaining = remaining
        if self.remaining <= 0:
            self.label.configure(text="STOP")
            #self.quit()
        else:
            delta = timedelta(seconds=self.remaining)
            t = datetime(1,1,1)+delta
            self.label.configure(text="%s:%s" % (zfill(t.minute,2), zfill(t.second,2)))
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

    def check_laser(self):
        if self.laser.get_state()[0]:
            self.decrease()
            self.after(5000, self.laser.reset_state)
            self.after(5000, self.check_laser)
        else:
            self.after(1000, self.check_laser)


if __name__ == "__main__":
    app = ExampleApp()
    
    app.mainloop()

