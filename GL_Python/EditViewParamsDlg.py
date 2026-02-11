# graphics_package/EditViewParamsDlg.py
import tkinter as tk
from tkinter import simpledialog
from .Point3d import Point3d
from .View3dParameters import View3dParameters

class EditViewParamsDlg(simpledialog.Dialog):
    """
    Lightweight dialog for editing 3D viewing parameters.
    Mimics the Java Swing EditViewParamsDlg.
    """

    def __init__(self, parent, params: View3dParameters):
        self.params = params
        super().__init__(parent, title="Edit Viewing Parameters")

    def body(self, master):
        row = 0
        # Projection type radio buttons
        tk.Label(master, text="Projection:").grid(row=row, column=0, sticky="w")
        self.proj_var = tk.IntVar(value=self.params.projectionType)
        tk.Radiobutton(master, text="Perspective", variable=self.proj_var,
                       value=View3dParameters.PT_PERSPECTIVE).grid(row=row, column=1)
        tk.Radiobutton(master, text="Parallel", variable=self.proj_var,
                       value=View3dParameters.PT_PARALLEL).grid(row=row, column=2)
        row += 1

        # VRP
        tk.Label(master, text="VRP (x,y,z):").grid(row=row, column=0, sticky="w")
        self.vrp_x = tk.Entry(master, width=6); self.vrp_x.insert(0, str(self.params.vrp.x() if self.params.vrp else 0))
        self.vrp_y = tk.Entry(master, width=6); self.vrp_y.insert(0, str(self.params.vrp.y() if self.params.vrp else 0))
        self.vrp_z = tk.Entry(master, width=6); self.vrp_z.insert(0, str(self.params.vrp.z() if self.params.vrp else 0))
        self.vrp_x.grid(row=row, column=1); self.vrp_y.grid(row=row, column=2); self.vrp_z.grid(row=row, column=3)
        row += 1

        # PRP
        tk.Label(master, text="PRP (x,y,z):").grid(row=row, column=0, sticky="w")
        self.prp_x = tk.Entry(master, width=6); self.prp_x.insert(0, str(self.params.prp.x() if self.params.prp else 0))
        self.prp_y = tk.Entry(master, width=6); self.prp_y.insert(0, str(self.params.prp.y() if self.params.prp else 0))
        self.prp_z = tk.Entry(master, width=6); self.prp_z.insert(0, str(self.params.prp.z() if self.params.prp else 0))
        self.prp_x.grid(row=row, column=1); self.prp_y.grid(row=row, column=2); self.prp_z.grid(row=row, column=3)
        row += 1

        # Window
        tk.Label(master, text="Window (umin,umax,vmin,vmax):").grid(row=row, column=0, sticky="w")
        self.umin = tk.Entry(master, width=6); self.umin.insert(0, str(self.params.VRCumin))
        self.umax = tk.Entry(master, width=6); self.umax.insert(0, str(self.params.VRCumax))
        self.vmin = tk.Entry(master, width=6); self.vmin.insert(0, str(self.params.VRCvmin))
        self.vmax = tk.Entry(master, width=6); self.vmax.insert(0, str(self.params.VRCvmax))
        self.umin.grid(row=row, column=1); self.umax.grid(row=row, column=2)
        self.vmin.grid(row=row, column=3); self.vmax.grid(row=row, column=4)
        return self.vrp_x  # initial focus

    def apply(self):
        # Update params from entries
        self.params.projectionType = self.proj_var.get()
        self.params.vrp = Point3d(float(self.vrp_x.get()), float(self.vrp_y.get()), float(self.vrp_z.get()))
        self.params.prp = Point3d(float(self.prp_x.get()), float(self.prp_y.get()), float(self.prp_z.get()))
        self.params.VRCumin = float(self.umin.get())
        self.params.VRCumax = float(self.umax.get())
        self.params.VRCvmin = float(self.vmin.get())
        self.params.VRCvmax = float(self.vmax.get())
