# example_usage.py
import tkinter as tk
from graphics_package.View3dTest import View3dTest
from graphics_package.View3dParameters import View3dParameters
from graphics_package.EditViewParamsDlg import EditViewParamsDlg

def run_with_dialog():
    params = View3dParameters()
    root = tk.Tk()
    root.withdraw()  # Hide main window
    dlg = EditViewParamsDlg(root, params)
    print("User chose parameters:", params.catalogue())

    # Run test with chosen params
    test = View3dTest()
    test.view.setOrientation(params.vrp, params.vpn, params.vup)
    test.view.setPRP(params.prp)
    test.view.setWindow(params.VRCumin, params.VRCumax, params.VRCvmin, params.VRCvmax)
    test.run(plot=True)

if __name__ == "__main__":
    run_with_dialog()
