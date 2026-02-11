# graphics_package/View3dTestApp.py
import tkinter as tk
from tkinter import messagebox
from graphics_package.View3dTest import View3dTest
from graphics_package.View3dParameters import View3dParameters
from graphics_package.EditViewParamsDlg import EditViewParamsDlg

class View3dTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("3D Test : Cube")
        self.geometry("400x300")

        # View + params
        self.params = View3dParameters()
        self.test = View3dTest()

        # Menu bar
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load new geometry...", command=self.load_geom)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Set viewing parameters...", command=self.edit_params)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About 3dTest", command=lambda: self.show_about("3dTest"))
        help_menu.add_command(label="About GraphicsPackage", command=lambda: self.show_about("GraphicsPackage"))
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

        # Add a "Run" button for quick plotting
        self.run_button = tk.Button(self, text="Run Projection", command=self.run_projection)
        self.run_button.pack(pady=50)

    def load_geom(self):
        messagebox.showinfo("Load Geometry", "Stub: geometry loader not implemented")

    def quit_app(self):
        self.destroy()

    def edit_params(self):
        dlg = EditViewParamsDlg(self, self.params)
        # Update View3d with new params
        self.test.view.setOrientation(self.params.vrp, self.params.vpn, self.params.vup)
        self.test.view.setPRP(self.params.prp)
        self.test.view.setWindow(self.params.VRCumin, self.params.VRCumax,
                                 self.params.VRCvmin, self.params.VRCvmax)

    def show_about(self, topic):
        if topic == "3dTest":
            messagebox.showinfo("About 3dTest", "Python port of View3dTest: perspective cube demo.")
        else:
            messagebox.showinfo("About GraphicsPackage", "GraphicsPackage: 2D/3D geometry + projection utilities.")

    def run_projection(self):
        self.test.run(plot=True)

if __name__ == "__main__":
    app = View3dTestApp()
    app.mainloop()
