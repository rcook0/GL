# graphics_package/View3d.py
from .Point3d import Point3d
from .Transformation3d import Transformation3d

class View3d:
    # Projection types
    PT_PARALLEL = 0
    PT_PERSPECTIVE = 1
    PT_DEFAULT = PT_PERSPECTIVE

    def __init__(self, vrp_in: Point3d = None, vpn_in=None, vup_in=None,
                 prp_in: Point3d = None, vv_in=None, PROJECTION_TYPE: int = None):
        # Flags
        self.CLIP_HITHER = True
        self.CLIP_YON = True

        # (1) View orientation (WC -> VRC)
        self.vrp = vrp_in if vrp_in else Point3d(0.5, 0.5, 2.0)
        # vpn, vup accept tuple or object with x(),y(),z()
        self.vpn = vpn_in if vpn_in else (0.0, 0.0, 1.0)
        self.vup = vup_in if vup_in else (0.0, 1.0, 0.0)

        # (2) View mapping (VRC)
        if vv_in is not None:
            # In Java vv was a Vector4d: (umin, umax, vmin, vmax)
            self.umin, self.umax, self.vmin, self.vmax = vv_in.x(), vv_in.y(), vv_in.z(), vv_in.h()
        else:
            self.umin, self.umax = -0.67, 2.25
            self.vmin, self.vmax = -0.5, 1.5

        self.prp = prp_in if prp_in else Point3d(0.0, 0.0, 10.0)

        self.backDistance = -5.0  # B (behind PRP, negative in VRC)
        self.frontDistance = 2.0  # F (in front of PRP)
        # 3D viewport (NPC → device)
        self.Xvmin, self.Xvmax = 0.0, 300.0
        self.Yvmin, self.Yvmax = 0.0, 300.0
        self.Zvmin, self.Zvmax = 0.0, (self.Xvmax + self.Yvmax)/2.0

        self.projectionType = (PROJECTION_TYPE
                               if PROJECTION_TYPE is not None
                               else View3d.PT_DEFAULT)

    # --- API parity with Java ---

    def prp_get(self) -> Point3d:
        return self.prp

    def setOrientation(self, vrp_in: Point3d, vpn_in, vup_in) -> None:
        self.vrp = vrp_in
        self.vpn = vpn_in
        self.vup = vup_in

    def setWindow(self, new_umin: float, new_umax: float, new_vmin: float, new_vmax: float) -> None:
        self.umin = new_umin
        self.umax = new_umax
        # NOTE: your Java had a small bug (vmin assigned from new_vmax). Fixed here:
        self.vmin = new_vmin
        self.vmax = new_vmax

    def width(self) -> float:
        return self.Xvmax - self.Xvmin

    def height(self) -> float:
        return self.Yvmax - self.Yvmin

    def integerWidth(self) -> int:
        return int(self.width())

    def integerHeight(self) -> int:
        return int(self.height())

    def setPRP(self, prp_in: Point3d) -> None:
        self.prp = prp_in

    def setViewport(self, xmin: float, xmax: float, ymin: float, ymax: float, zmin: float, zmax: float) -> None:
        self.Xvmin, self.Xvmax = xmin, xmax
        self.Yvmin, self.Yvmax = ymin, ymax
        self.Zvmin, self.Zvmax = zmin, zmax

    def f(self) -> float:
        return self.frontDistance

    def b(self) -> float:
        return self.backDistance

    # --- Core math from your Java ---

    def nPer(self) -> Transformation3d:
        """
        Normalizing transformation for perspective projection.
        Mirrors your Java steps:
         1) Translate to center of window and frontDistance
         2) Rotate to align VPN->z, VUP->y, (u->x)
         3) Translate PRP to origin
         4) Shear centre line of view volume to z axis
         5) Scale to canonical perspective view volume
        """
        # 1) Translate VRP to origin: in your Java, this translation used window centre and frontDistance
        T_vrp = Transformation3d()
        T_vrp.translate(-(self.umax + self.umin)/2.0,
                        -(self.vmax + self.vmin)/2.0,
                        -self.frontDistance)

        # 2) Rotate using vpn/vup
        R = Transformation3d()
        R.viewingRotation(self.vpn, self.vup)

        # 3) Translate PRP to origin
        T_prp = Transformation3d()
        T_prp.translate(-self.prp.x(), -self.prp.y(), -self.prp.z())

        # 4) Shear so DOP aligns with z
        # DOP = CW - PRP, where CW is the window centre at z=0 in VRC
        DOPx = ((self.umax + self.umin)/2.0) - self.prp.x()
        DOPy = ((self.vmax + self.vmin)/2.0) - self.prp.y()
        DOPz = -self.prp.z()

        SHpar = Transformation3d()
        # Handle DOPz≈0 safely
        if abs(DOPz) < 1e-9:
            shx = 0.0
            shy = 0.0
        else:
            shx = -(DOPx / DOPz)
            shy = -(DOPy / DOPz)
        SHpar.shearZ(shx, shy)

        # 5) Scale to canonical perspective view volume
        Sper = Transformation3d()
        vrp_z = -self.prp.z()
        # Guard denominators
        denom_x = (self.umax - self.umin) * (vrp_z + self.backDistance)
        denom_y = (self.vmax - self.vmin) * (vrp_z + self.backDistance)
        denom_z = (vrp_z + self.backDistance)
        sx = (2.0 * vrp_z / denom_x) if abs(denom_x) > 1e-9 else 1.0
        sy = (2.0 * vrp_z / denom_y) if abs(denom_y) > 1e-9 else 1.0
        sz = (-1.0 / denom_z) if abs(denom_z) > 1e-9 else -1.0
        Sper.scale(sx, sy, sz)

        nper = Transformation3d()
        nper.transform(T_vrp)
        nper.transform(R)
        nper.transform(T_prp)
        nper.transform(SHpar)
        nper.transform(Sper)
        return nper

    def clip3d(self, line, zmin: float) -> bool:
        """
        Liang–Barsky-style clip against perspective canonical view volume.
        Port of your Java with the same parameter flow.
        """
        tmin = 0.0
        tmax = 1.0

        p0 = line.getSourcePoint()
        p1 = line.getDestinationPoint()

        dx = p1.x() - p0.x()
        dy = p1.y() - p0.y()
        dz = p1.z() - p0.z()

        # We use locals so we can update them if endpoints get clipped
        x0, y0, z0 = p0.x(), p0.y(), p0.z()
        x1, y1, z1 = p1.x(), p1.y(), p1.z()

        def CLIPt(denom: float, num: float) -> bool:
            nonlocal tmin, tmax
            if denom > 0:
                t = num / denom
                if t > tmax:
                    return False
                elif t > tmin:
                    tmin = t
            elif denom < 0:
                t = num / denom
                if t < tmin:
                    return False
                else:
                    tmax = min(tmax, t)
            else:
                if num > 0:
                    return False
            return True

        # Right:  -dx - dz,   x0 + z0
        if CLIPt(-dx - dz,  x0 + z0):
            # Left:    dx - dz,  -x0 + z0
            if CLIPt( dx - dz, -x0 + z0):
                # Bottom:  dy - dz,  -y0 + z0
                if CLIPt( dy - dz, -y0 + z0):
                    # Top:   -dy - dz,  y0 + z0
                    if CLIPt(-dy - dz,  y0 + z0):
                        # Near:   -dz,    z0 - zmin
                        if CLIPt(-dz,      z0 - zmin):
                            # Far:     dz,   -z0 - 1
                            if CLIPt( dz,   -z0 - 1):
                                # Visible
                                if tmax < 1.0:
                                    x1 = x0 + tmax * dx
                                    y1 = y0 + tmax * dy
                                    z1 = z0 + tmax * dz
                                if tmin > 0.0:
                                    x0 = x0 + tmin * dx
                                    y0 = y0 + tmin * dy
                                    z0 = z0 + tmin * dz

                                p0.set_x(x0); p0.set_y(y0); p0.set_z(z0)
                                p1.set_x(x1); p1.set_y(y1); p1.set_z(z1)
                                # Update the line in-place; return True == accepted
                                return True
        return False

    def mVV3DV(self) -> Transformation3d:
        """
        Map from canonical parallel view volume (-1..1, -1..1, -1..0)
        into 3D viewport box [Xvmin..Xvmax] x [Yvmin..Yvmax] x [Zvmin..Zvmax].
        """
        M = Transformation3d()

        align = Transformation3d()
        align.translate(1.0, 1.0, 1.0)
        M.transform(align)

        scale = Transformation3d()
        scale.scale((self.Xvmax - self.Xvmin)/2.0,
                    (self.Yvmax - self.Yvmin)/2.0,
                    (self.Zvmax - self.Zvmin))
        M.transform(scale)

        align2 = Transformation3d()
        align2.translate(self.Xvmin, self.Yvmin, self.Zvmin)
        M.transform(align2)

        return M

    # Stubs to mirror Java API (no-ops here; your pipeline drives from outside):
    def perspectiveProject(self) -> None:
        pass  # Use your external pipeline steps as in View3dTest
