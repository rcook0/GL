package GraphicsPackage;

/** 
 * Encapsulation of view specification data for both parallel and perspective
 projections. A number of preset views can be constructed by using this View3d.

 The default projection type is Parallel, but this is variable across different
 instances of this class.

 The default viewing parameters are as follows:

 Viewing parameter   Value
 VRP(WC)             (0, 0, 0)  (origin)
 VPN(WC)             (0, 0, 1)  (z axis)
 VUP(WC)             (0, 1, 0)  (y axis)
 PRP(VRC)            (0.5, 0.5, 1.0)
 window(VRC)         (0, 1, 0, 1)
 projection type     Perspective

 Changing the view (e.g. making a perspective projection) is as easy as 
 redefining the above parameters.

 note Strategy pattern for pluggable viewing operations - choosing between
 Parallel and Perspective projections, and interchangeable rendering pipelines
 for different rendering models.

 * <P>
 * @author Ryan L Cook
 */

public class View3d {

  // DOP is from PRP to Centre of Window (CW)
  private static final int PT_PARALLEL = 0;
  // PRP is centre of projection
  private static final int PT_PERSPECTIVE = 1;
  
  private static int PT_DEFAULT = PT_PERSPECTIVE;

  private int projectionType = PT_DEFAULT;
  
  private boolean CLIP_HITHER = true; // specify use of the front plane.
  private boolean CLIP_YON = true; // specify use of the back plane.

  /* (1) View Plane (VP) - components of view orientation matrix, WCuvn -> VRCxyz */
  private Point3d vrp = new Point3d(0.5, 0.5, 2.0); // View reference point, world coordinates
  private Vector4d vpn = new Vector4d(0.0, 0.0, 1.0); // View plane normal, WC
  private Vector4d vup = new Vector4d(0.0, 1.0, 0.0); // View-up vector, WC

  /* (2) View Mapping Matrix (VMM) - ( VRC -> NPC ) */

  // Specification of view volume (VRC)

  // window (view reference coordinates)
  private double umin = -0.67; private double umax = 2.25;
  private double vmin = -0.5; private double vmax = 1.5;

  // Centre of Projection (COP) in Viewing Reference Coordinate system (VRC)
  private Point3d prp = new Point3d(0.0, 0.0, 10); // (projection reference point)

  private double backDistance = -5; //B = distance from PRP to rear clipping plane
  private double frontDistance = 2; //F = distance from PRP to front clipping plane
  /* assert f > b to avoid negative view volume */

  // 3d viewport - Normalized Projection Coordinates (NPC, 3D screen coordinates)
  private double Xvmin = 0; private double Xvmax = 300;
  private double Yvmin = 0; private double Yvmax = 300;
  private double Zvmin = 0; private double Zvmax = (Xvmax + Yvmax)/2;

  public Point3d prp() { return prp; }

  /**
   * Constructor - initialize the perspective type, clipping and projection
   matrices.
   */
  public View3d(Point3d vrp_in, Vector4d vpn_in, Vector4d vup_in, Point3d prp_in, Vector4d vv_in, int PROJECTION_TYPE) {
    projectionType = PROJECTION_TYPE;

    vrp = vrp_in;
    vpn = vpn_in;
    vup = vup_in;
    
    prp = prp_in;

    umin = vv_in.x();
    umax = vv_in.y();
    vmin = vv_in.z();
    vmax = vv_in.h();
/*
    switch (PROJECTION_TYPE) {
         PT_PARALLEL : setParallelViewport();
         PT_PERSPECTIVE : setPerspectiveViewport();
         }
*/    
  }

  /** Constructor - accept the defaults. */
  public View3d() {}

  private void setParallelViewport(){};

  private void setPerspectiveViewport(){};

  public void setOrientation(Point3d vrp_in, Vector4d vpn_in, Vector4d vup_in) {
    vrp = vrp_in;
    vpn = vpn_in;
    vup = vup_in;
  }

  public void setWindow(double new_umin, double new_umax, double new_vmin, double new_vmax) {
    umin = new_umin;
    umax = new_umax;
    vmin = new_vmax;
    vmax = new_vmax;
  }

  /* Width of projected image. */
  public double width() {
    return Xvmax - Xvmin;
  }
  /* Height of projected image. */
  public double height() {
    return Yvmax - Yvmin;
  }
  public int integerWidth() {
    return (int)width();
  }
  public int integerHeight() {
    return (int)height();
  }

  /* Set the projection reference point for perspective projection.
  (For parallel projection, it is at an infinite distance from the view plane.)
  */
  public void setPRP(Point3d prp_in) {
    prp = prp_in;
  }

  public void setViewport(double xmin, double xmax, double ymin, double ymax, double zmin, double zmax) {
    Xvmin = xmin;
    Xvmax = xmax;
    Yvmin = ymin;
    Yvmax = ymax;
    Zvmin = zmin;
    Zvmax = zmax;
  }

  public double f(){
    return frontDistance;
  }

  public double b(){
    return backDistance;
  }

  /**
  Perform a Perspective Projection
  */
  void perspectiveProject() {
    /* Translate world coordinates to the canonical view.
    Homogeneity remains intact for linear primitives, but may not for nonlinear
    entities such as parametric surfaces. */
    nPer();

    /*if (W < 0)
      homogenize;*/
    
    /*
    Clip against perspective-project canonical view.
    It may be unnecessary to clip at all, because this is done by the window system.
    */
    
    //clip3d();
      
    /*
    Apply the perspectice projection.
    */
    project2D();

    
  }

  /** Normalizing transformation for parallel projection.

    // 1. Translate the VRP to the origin


    // 2. Rotate VRC: (nuv)~>(xyz)


    // 3. Shear so that the direction of projection becomes parallel to the z axis


    // 4. Translate and scale into the parallel-projection canonical view volume
  
   */
  void nPar() {

  }

  /** Normalizing transformation for perspective projection. */
  public Transformation3d nPer() {
    // 1. Translate VRP (world coordinates) to Origin
    Transformation3d T_vrp = new Transformation3d();
    T_vrp.translate(-(umax+umin)/2, -(vmax+vmin)/2, -frontDistance);

    // 2. Rotate VRC: VPN(n-axis) to z axis, u axis to x axis, v axis to y axis
    Transformation3d R = new Transformation3d();
    R.viewingRotation(vpn, vup);

    // 3. Translate PRP to origin
    Transformation3d T_prp = new Transformation3d();
    T_prp.translate(-prp.x(), -prp.y(), -prp.z());

    // 4. Shear centre line of view volume to z axis
    Transformation3d SHpar = new Transformation3d();

    // DOP = CW - PRP
    double DOPx = ((umax + umin)/2) - prp.x();
    double DOPy = ((vmax + vmin)/2) - prp.y();
    double DOPz = -prp.z();
    double DOPw = 0;

    /* N.B. For the orthographic projection, a special case occurs in which the 
    projection reference point is at the centre of the view volume and the shear
    matrix coefficients evaluate to zero. The shear matrix is then equivalent to
    the identity matrix. */
    
    double SHXpar = -(DOPx/DOPz);
    double SHYpar = -(DOPy/DOPz);
    SHpar.shearZ(SHXpar, SHYpar);
    
    // 5. Scale view volume to canonical perspective view volume
    Transformation3d Sper = new Transformation3d();
    
    double vrp_z = -prp.z();
    double sx = 2 * vrp_z / ((umax - umin) * (vrp_z + backDistance));
    double sy = 2 * vrp_z / ((vmax - vmin) * (vrp_z + backDistance));
    double sz = -1 / (vrp_z + backDistance);
    Sper.scale(sx, sy, sz);

    Transformation3d nper = new Transformation3d();
    nper.transform(T_vrp);
    nper.transform(R);
    nper.transform(T_prp);
    nper.transform(SHpar);
    nper.transform(Sper);

    return nper;    
  }

  /**
  Clip a line against the 3D canonical perspective-projection view volume.  
  N.B L-B3d, P274, Foley et al, 2/e
  */
  
  public boolean clip3d(Line3d line, double zmin) {
    double tmin = 0.0, tmax = 1.0;
    Point3d p0 = line.getSourcePoint();
    Point3d p1 = line.getDestinationPoint();
    double dx = p1.x() - p0.x();
    double dz = p1.z() - p0.z();
    
    boolean accept;
    
    accept = false;

    if (CLIPt (-dx-dz, p0.x() + p0.z(), tmin, tmax))         /* Right side */
       if (CLIPt (dx - dz, -p0.x() + p0.z(), tmin, tmax)) {  /* Left side */
           /* Now, part of line is in -z <= x <= z */
           double dy = p1.y() - p0.y();
           if (CLIPt(dy - dz, -p0.y() + p0.z(), tmin, tmax)) /* Bottom */
               if (CLIPt(-dy - dz, p0.y() + p0.z(), tmin, tmax))       /* Top */
                  /* Now, part of line is in -z <= x <= z, -z <= y <= z */
                  if (CLIPt(-dz, p0.z() - zmin, tmin, tmax))
                     if (CLIPt (dz, -p0.z() - 1, tmin, tmax)) {
                        /* If get here, part of line is visible in -z <= x <= z */
                        /* -z <= y <= z, -1 <= z <= zmin */
                        accept = true;                         /* Part of line is visible. */
                        /* If endpoint 1 (t = 1) is not in the region, compute
                        intersection */
                        if (tmax < 1.0) {
                           p1.x(p0.x() + (tmax * dx));
                           p1.y(p0.y() + (tmax * dy));
                           p1.z(p0.z() + (tmax * dz));
                        }

                        /* If endpoint 0 (t = 0) is not in the region, compute intersection */
                        if (tmin > 0.0) {
                           p0.x(p0.x() + (tmax * dx));
                           p0.y(p0.y() + (tmax * dy));
                           p0.z(p0.z() + (tmax * dz));
                        }
                     }
       }
       
       if(accept){
         line = new Line3d(p0, p1);
         return true;
         }
       else
         return false;
  } /* clip3d */

  /** Parametric line clipper by Liang and Barsky */
  private boolean CLIPt(double denom, double num, double tE, double tL) {
    double t;

    if (denom > 0) {
        t = num / denom;
        if (t > tL)
            return false;
        else if (t > tE)
            tE = t;
    } else if (denom < 0) {
        t = num / denom;
        if (t < tE)
            return false;
        else
            tL = t;
    } else if (num > 0)
        return false;
    return true;
  } /* CLIPt */
  
  /**
  Transformation to map the contents of the parallel view volume at the boundaries
  -1<=x<=1, -1<=y<=1, -1<=z<=0 to 3D viewport contained in the unit cube:
  0<=x<=1, 0<=y<=1, 0<=z<=1.
  Coordinates output after this stage are applied to a visible-surface algorithm
  which uses the z coordinate to determine which primitives are visible.
  */
  public Transformation3d mVV3DV(){
    Transformation3d mVV3DV = new Transformation3d();

    Transformation3d align = new Transformation3d();
    align.translate(1, 1, 1);
    mVV3DV.transform(align);

    Transformation3d scale = new Transformation3d();
    scale.scale((Xvmax - Xvmin)/2, (Yvmax - Yvmin)/2, Zvmax - Zvmin);
    mVV3DV.transform(scale);

    Transformation3d align2 = new Transformation3d();
    align2.translate(Xvmin, Yvmin, Zvmin);
    mVV3DV.transform(align2);

    return mVV3DV;
  }

  /** Project to 2D device coordinates
  (transformed to the output window by the windowing system). */

  void project2D() {

  }

  /**
  A numerical test of the viewing operation can be found in View3dTest.java. */
  public static void main(String[] args){

    }
}


