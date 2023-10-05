from tkinter import *
import customtkinter

#while there is no Conpot communications, we import Tank directly
import scada.gastank

class HMI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("GasTank HMI")

        customtkinter.set_appearance_mode("dark")

        self.geometry('500x400')

        for c in range(2): self.columnconfigure(index=c, weight=1)
        for r in range(3): self.rowconfigure(index=r, weight=1)

        # progressbar as tank level display

        self.tank = customtkinter.CTkProgressBar(self, orientation=VERTICAL, width=100, height=350, corner_radius=0, progress_color="green")
        self.tank.grid(row=0, column=0, rowspan=3, padx=10)

        # textfield with values

        self.label_frame = customtkinter.CTkFrame(self, width=10)
        self.label_frame.grid(row=0, column=1, sticky="s")

        self.title = customtkinter.CTkLabel(self.label_frame, text="Values", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, sticky="nwe")

        self.level = customtkinter.CTkLabel(self.label_frame, text="Level: 50/100")
        self.level.grid(row=1, column=0)
        self.temp = customtkinter.CTkLabel(self.label_frame, text="Temperature: 28 °C", padx=10)
        self.temp.grid(row=2, column=0)
        self.pressure = customtkinter.CTkLabel(self.label_frame, text="Pressure: 28 Pa")
        self.pressure.grid(row=3, column=0)

        # buttons

        self.fillButton = customtkinter.CTkButton(self, text='Fill', height=50, command=fillTank)
        self.fillButton.grid(row=1, column=1) 
        self.drainButton = customtkinter.CTkButton(self, text='Drain', height=50, command=drainTank)
        self.drainButton.grid(row=2, column=1, sticky="n") 

        self.hmi_update()

    def hmi_update(self):
        gasTank.update()
        self.level.configure(text=f"Level: {gasTank.level}/100")
        self.temp.configure(text=f"Temperature: {gasTank.temp} °C")
        self.pressure.configure(text=f"Pressure: {gasTank.pressure} Pa")
        self.tank.set(gasTank.level/100)
        self.after(1000, self.hmi_update)

gasTank = gastank.GasTank()

def fillTank():
    gasTank.fill(10)
    
def drainTank():
    gasTank.drain(10)

hmi = HMI()

hmi.mainloop()