# graphics_package/View3dParameters.py
from .Point3d import Point3d

class View3dParameters:
    """
    Container for 3D view parameters:
    - projectionType: parallel or perspective
    - vrp: View Reference Point (camera position)
    - vup: View Up Vector (as tuple)
    - vpn: View Plane Normal (as tuple)
    - prp: Projection Reference Point
    - window: (umin, umax, vmin, vmax)
    """

    PT_PARALLEL = 0
    PT_PERSPECTIVE = 1
    PT_DEFAULT = PT_PERSPECTIVE

    def __init__(self):
        self.projectionType = View3dParameters.PT_DEFAULT
        self.vrp: Point3d | None = None
        self.vup: tuple[float,float,float] = (0, 1, 0)
        self.vpn: tuple[float,float,float] = (0, 0, -1)
        self.prp: Point3d | None = None
        self.VRCumin: float = 0.0
        self.VRCumax: float = 0.0
        self.VRCvmin: float = 0.0
        self.VRCvmax: float = 0.0

    def catalogue(self) -> str:
        return (f"vrp={self.vrp}, vup={self.vup}, vpn={self.vpn}, "
                f"prp={self.prp}, "
                f"VRCumin={self.VRCumin}, VRCumax={self.VRCumax}, "
                f"VRCvmin={self.VRCvmin}, VRCvmax={self.VRCvmax}")

    def getParameters(self) -> "View3dParameters":
        return self

    def setParameters(self, parm: "View3dParameters") -> None:
        self.projectionType = parm.projectionType
        self.vrp = parm.vrp
        self.vup = parm.vup
        self.vpn = parm.vpn
        self.prp = parm.prp
        self.VRCumin = parm.VRCumin
        self.VRCumax = parm.VRCumax
        self.VRCvmin = parm.VRCvmin
        self.VRCvmax = parm.VRCvmax

    # Getters / setters
    def vrp_get(self): return self.vrp
    def vrp_set(self, new_vrp: Point3d): self.vrp = new_vrp

    def vup_get(self): return self.vup
    def vup_set(self, new_vup: tuple[float,float,float]): self.vup = new_vup

    def vpn_get(self): return self.vpn
    def vpn_set(self, new_vpn: tuple[float,float,float]): self.vpn = new_vpn

    def prp_get(self): return self.prp
    def prp_set(self, new_prp: Point3d): self.prp = new_prp

    def projectionType_get(self): return self.projectionType
    def projectionType_set(self, t: int): self.projectionType = t

    def VRC_umin(self): return self.VRCumin
    def VRC_umax(self): return self.VRCumax
    def VRC_vmin(self): return self.VRCvmin
    def VRC_vmax(self): return self.VRCvmax

    def VRC_umin_set(self, v: float): self.VRCumin = v
    def VRC_umax_set(self, v: float): self.VRCumax = v
    def VRC_vmin_set(self, v: float): self.VRCvmin = v
    def VRC_vmax_set(self, v: float): self.VRCvmax = v
