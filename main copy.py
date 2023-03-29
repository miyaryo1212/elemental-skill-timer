import ctypes
import threading
import time
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk

from ttkbootstrap import Style


class Application:
    def __init__(self):
        self.current_slot = 3
        # (元素, 継続時間, クールタイム, 差分)
        self.slot1_property = ("Alhaitham", "dendro", 12, 18, 6)
        self.slot2_property = ("Fischl", "electro", 10, 25, 15)
        self.slot3_property = ("Xingqiu", "hydro", 15, 21, 6)
        self.slot4_property = ("Barbara", "hydro", 15, 32, 17)
        self.color = {
            "geo": ("#B2881A", "#E6B322"),
            "pyro": ("#CC4733", "#FF6F63"),
            "anemo": ("#2DB2A2", "#4CD9C8"),
            "cyro": ("#55B9F2", "#73CCFF"),
            "hydro": ("#1C80BA", "#4C92EA"),
            "electro": ("#AA50E5", "#C773FF"),
            "dendro": ("#39B100", "#7AD84C"),
        }
        self.icon = {}

        self.window()

    def window(self):
        def info(title, content):
            tkinter.messagebox.showinfo(title, content)

        def close(event):
            root.destroy()

        def slot1_pressed():
            style.configure(
                "slot1.Horizontal.TProgressbar",
                background=self.color[self.slot1_property[1]][0],
            )
            progressbar_slot1["maximum"] = self.slot1_property[2]
            progressbar_slot1["value"] = self.slot1_property[2]
            for i in range(60 * self.slot1_property[2]):
                progressbar_slot1["value"] -= 1 / 60
                time.sleep(1 / 60)
            progressbar_slot1["value"] = 0
            style.configure(
                "slot1.Horizontal.TProgressbar",
                background=self.color[self.slot1_property[1]][1],
            )
            progressbar_slot1["maximum"] = self.slot1_property[4]
            for i in range(60 * self.slot1_property[4]):
                progressbar_slot1["value"] += 1 / 60
                time.sleep(1 / 60)
            progressbar_slot1["value"] = self.slot1_property[4]
            style.configure(
                "slot1.Horizontal.TProgressbar",
                background=self.color[self.slot1_property[1]][0],
            )

        def func1():
            threading.Thread(target=slot1_pressed).start()

        def slot2_pressed():
            style.configure(
                "slot2.Horizontal.TProgressbar",
                background=self.color[self.slot2_property[1]][0],
            )
            progressbar_slot2["maximum"] = self.slot2_property[2]
            progressbar_slot2["value"] = self.slot2_property[2]
            for i in range(60 * self.slot2_property[2]):
                progressbar_slot2["value"] -= 1 / 60
                time.sleep(1 / 60)
            progressbar_slot2["value"] = 0
            style.configure(
                "slot2.Horizontal.TProgressbar",
                background=self.color[self.slot2_property[1]][1],
            )
            progressbar_slot2["maximum"] = self.slot2_property[4]
            for i in range(60 * self.slot2_property[4]):
                progressbar_slot2["value"] += 1 / 60
                time.sleep(1 / 60)
            progressbar_slot2["value"] = self.slot2_property[4]
            style.configure(
                "slot2.Horizontal.TProgressbar",
                background=self.color[self.slot2_property[1]][0],
            )

        def func2():
            threading.Thread(target=slot2_pressed).start()

        def slot3_pressed():
            style.configure(
                "slot3.Horizontal.TProgressbar",
                background=self.color[self.slot3_property[1]][0],
            )
            progressbar_slot3["maximum"] = self.slot3_property[2]
            progressbar_slot3["value"] = self.slot3_property[2]
            for i in range(60 * self.slot3_property[2]):
                progressbar_slot3["value"] -= 1 / 60
                time.sleep(1 / 60)
            progressbar_slot3["value"] = 0
            style.configure(
                "slot3.Horizontal.TProgressbar",
                background=self.color[self.slot3_property[1]][1],
            )
            progressbar_slot3["maximum"] = self.slot3_property[4]
            for i in range(60 * self.slot3_property[4]):
                progressbar_slot3["value"] += 1 / 60
                time.sleep(1 / 60)
            progressbar_slot3["value"] = self.slot3_property[4]
            style.configure(
                "slot3.Horizontal.TProgressbar",
                background=self.color[self.slot3_property[1]][0],
            )

        def func3():
            threading.Thread(target=slot3_pressed).start()

        def slot4_pressed():
            style.configure(
                "slot4.Horizontal.TProgressbar",
                background=self.color[self.slot4_property[1]][0],
            )
            progressbar_slot4["maximum"] = self.slot4_property[2]
            progressbar_slot4["value"] = self.slot4_property[2]
            for i in range(60 * self.slot4_property[2]):
                progressbar_slot4["value"] -= 1 / 60
                time.sleep(1 / 60)
            progressbar_slot4["value"] = 0
            style.configure(
                "slot4.Horizontal.TProgressbar",
                background=self.color[self.slot4_property[1]][1],
            )
            progressbar_slot4["maximum"] = self.slot4_property[4]
            for i in range(60 * self.slot4_property[4]):
                progressbar_slot4["value"] += 1 / 60
                time.sleep(1 / 60)
            progressbar_slot4["value"] = self.slot4_property[4]
            style.configure(
                "slot4.Horizontal.TProgressbar",
                background=self.color[self.slot4_property[1]][0],
            )

        def func4():
            threading.Thread(target=slot4_pressed).start()

        style = Style()
        style.configure("slot1.Horizontal.TProgressbar", troughcolor="#C3C3C3")
        style.configure("slot2.Horizontal.TProgressbar", troughcolor="#C3C3C3")
        style.configure("slot3.Horizontal.TProgressbar", troughcolor="#C3C3C3")
        style.configure("slot4.Horizontal.TProgressbar", troughcolor="#C3C3C3")

        root = style.master
        root.title("Elemental Skill Timer")
        root.geometry("+1655+245")
        root.resizable(False, False)
        root.attributes("-topmost", True)
        root.wm_attributes("-transparentcolor", "white")
        root.overrideredirect(True)

        """
        icondata =
        root.tk.call(
            "wm", "iconphoto", root._w, tkinter.PhotoImage(data=icondata)
        )
        """

        inner = ttk.Frame(root)
        inner.grid(column=0, row=0, ipadx=0, ipady=0, padx=20, pady=20)

        column0 = tkinter.Canvas(inner, width=30, height=0)
        column0.grid(column=0, row=0, ipadx=0, ipady=0, padx=0, pady=0)
        column1 = tkinter.Canvas(inner, width=200, height=0)
        column1.grid(column=1, row=0, ipadx=0, ipady=0, padx=0, pady=0)

        progressbar_slot1 = ttk.Progressbar(
            inner,
            length=0,
            mode="determinate",
            style="slot1.Horizontal.TProgressbar",
        )
        progressbar_slot1.grid(
            column=1,
            row=1,
            columnspan=1,
            sticky=tkinter.NSEW,
            ipadx=0,
            ipady=0,
            padx=10,
            pady=42,
        )
        progressbar_slot1["maximum"] = 1
        progressbar_slot1["value"] = 1
        style.configure(
            "slot1.Horizontal.TProgressbar",
            background=self.color[self.slot1_property[1]][0],
        )

        progressbar_slot2 = ttk.Progressbar(
            inner,
            length=0,
            mode="determinate",
            style="slot2.Horizontal.TProgressbar",
        )
        progressbar_slot2.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky=tkinter.NSEW,
            ipadx=0,
            ipady=0,
            padx=10,
            pady=42,
        )
        progressbar_slot2["maximum"] = 1
        progressbar_slot2["value"] = 1
        style.configure(
            "slot2.Horizontal.TProgressbar",
            background=self.color[self.slot2_property[1]][0],
        )

        progressbar_slot3 = ttk.Progressbar(
            inner,
            length=0,
            mode="determinate",
            style="slot3.Horizontal.TProgressbar",
        )
        progressbar_slot3.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky=tkinter.NSEW,
            ipadx=0,
            ipady=0,
            padx=10,
            pady=42,
        )
        style.configure(
            "slot3.Horizontal.TProgressbar",
            background=self.color[self.slot3_property[1]][0],
        )
        progressbar_slot3["maximum"] = 1
        progressbar_slot3["value"] = 1

        progressbar_slot4 = ttk.Progressbar(
            inner,
            length=0,
            mode="determinate",
            style="slot4.Horizontal.TProgressbar",
        )
        progressbar_slot4.grid(
            column=1,
            row=4,
            columnspan=1,
            sticky=tkinter.NSEW,
            ipadx=0,
            ipady=0,
            padx=10,
            pady=42,
        )
        progressbar_slot4["maximum"] = 1
        progressbar_slot4["value"] = 1
        style.configure(
            "slot4.Horizontal.TProgressbar",
            background=self.color[self.slot4_property[1]][0],
        )

        root.bind("<Escape>", close)
        root.mainloop()


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    Application()
