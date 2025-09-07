package View3dTest;
import GraphicsPackage.*;
import java.awt.Color;

/**
 View3dTest. Low-level test code.

 Performs the steps of a perspective projection on a cube defined by eight
 points and 12 lines connecting them. Aim is to test the mathematical operation
 of the perspective projection.
 
 * <P>
 * @author
 */

public class View3dTest extends ApplicationFrame {

  /* Array holding geometric information. */
  private Line3d[] lines;

  /* Aggregate holding the 2D representation of the picture. */
  private CompoundGraphicObject2d picture;

  /* Data and procedures used to calculate the view.
  Constructed with default viewing parameters (see View3d documentation). */
  private View3d view = new View3d();

  /* Number of objects used by this application. */
  private static final int APP_N_OBJECTS = 12;

  /* Screen position of the application window. */
  private static final int winLocX = 200;
  private static final int winLocY = 150;

  public View3dTest() {
    super();
    // construct simple (flatfile) geometry DB
    geom();
  }

  public void initComponents() throws Exception {

    /* Important : Creating the menu object and attaching it to the current
    instance of View3dTest _before_ the call to initComponents() attempts to
    install the menu in the frame. */

    // menu.setParentFrame(this);
    setMainMenu(new ViewTest_Menu1(this));
    super.initComponents();
    setLocation(new java.awt.Point(winLocX, winLocY));
    setSize(view.integerWidth(), view.integerHeight());
    setTitle("Test :  Cube");
    setBackground(Color.white);
    setVisible(true);
  }

  public static void main(String[] args){

  try {
		View3dTest frame = new View3dTest();
    frame.initComponents();
    //frame.add();
		}
	catch (Exception e) {
		e.printStackTrace();
		}
  }

    /*
  public void add() {
    picture = new CompoundGraphicObject2d();
    myDrawing.add(picture);
    picture.add(new Line2d(0, 0, 100, 100));
  }
    */

  /* Get the viewing parameters entered from the dialog box and load the
  parameters into the new 3D view. */
  public void loadViewParams(View3dParameters v3dp) {
    view = new View3d();
    view.setOrientation(v3dp.vrp(), v3dp.vpn(), v3dp.vup());
    view.setPRP(v3dp.prp());
    view.setWindow(v3dp.VRC_umin(), v3dp.VRC_umax(), v3dp.VRC_vmin(), v3dp.VRC_vmax());
  }

  /* Given a set of endpoints defining a set of lines, perform the viewing
  operation on the lines. The procedure below carries out the PERSPECTIVE
  projection. */
  public Line3d[] processViewingOp_PER(Line3d[] ourLines, int nLines) {

    boolean[] accept = {false, false, false, false, false, false, false, false, false, false, false, false};
    Vector4d[] hlines = new Vector4d[]{new Vector4d(), new Vector4d(), new Vector4d(), new Vector4d(),
               new Vector4d(), new Vector4d(), new Vector4d(), new Vector4d(),
               new Vector4d(), new Vector4d(), new Vector4d(), new Vector4d(),
               new Vector4d(), new Vector4d(), new Vector4d(), new Vector4d(),
               new Vector4d(), new Vector4d(), new Vector4d(), new Vector4d(),
               new Vector4d(), new Vector4d(), new Vector4d(), new Vector4d()};

    /* Construct the perspective projection matrix */

    BasicProjection Mper = new BasicProjection();
    Mper.perspective(-1);

    /* Clip against the canonical perspective view volume. */

    for(int i = 0; i < nLines ; i++){
      accept[i] = view.clip3d(ourLines[i], 1.333333); //zmin = -1
      if(!accept[i]) {
        System.out.println("Decline " + i);
        ourLines[i] = null; /* */
      }
      else {
        Point3d l1 = (Point3d)(ourLines[i].getSourcePoint());
        Point3d l2 = (Point3d)(ourLines[i].getDestinationPoint());
        System.out.println("Accept " + i + " : " + l1.x() + " " + l1.y() + " " + l1.z() + " " + l2.x() + " " + l2.y() + " " + l2.z() );
        hlines[2*i] = new Vector4d(ourLines[i].getSourcePoint());
        hlines[(2*i)+1] = new Vector4d(ourLines[i].getDestinationPoint());
        hlines[2*i].homogenize();
        hlines[(2*i)+1].homogenize();

        /* Perform the perspective projection. */

        hlines[2*i].transform(Mper);
        hlines[(2*i)+1].transform(Mper);

        /* 3D viewport transformations:
        1. Conversion from perspective to parallel canonical view volume.
        2. Transformation to the 3D viewport. */

        Transformation3d t = new Transformation3d();
        t.tPerspectiveToParallelCVV(view.f(), view.b(), new Vector4d(view.prp()));
        hlines[2*i].transform(t);
        hlines[(2*i)+1].transform(t);

        hlines[2*i].homogenize();
        hlines[(2*i)+1].homogenize();

        hlines[2*i].transform(view.mVV3DV());
        hlines[(2*i)+1].transform(view.mVV3DV());
        System.out.println(hlines[2*i].y());
        ourLines[i] = new Line3d(
          new Point3d( hlines[2*i].x(), hlines[2*i].y(), hlines[2*i].z() ),
          new Point3d( hlines[(2*i)+1].x(), hlines[(2*i)+1].y(), hlines[(2*i)+1].z() )
          );

        //lines[i] = new Point3d(hlines[i].x(), hlines[i].y(), hlines[i].z());
        //lines[i] = new Point3d(hlines[(2*i)+1].x(), hlines[(2*i)+1].y(), hlines[(2*i)+1].z());
      }
    }
    return ourLines;
  }

  public void geom() {

    Vector4d a = new Vector4d(0, 0, 1);
    Vector4d b = new Vector4d(0, 1, 0);
    Vector4d c = new Vector4d(0, 1, 1);
    Vector4d d = new Vector4d(1, 0, 0);
    Vector4d e = new Vector4d(1, 0, 1);
    Vector4d f = new Vector4d(1, 1, 0);
    Vector4d g = new Vector4d(1, 1, 1);
    Vector4d h = new Vector4d(0, 0, 0);

    Vector4d[] cube = {a, b, c, d, e, f, g, h};
    /* Convert each point of the cube to the canonical perspective projection
    view volume.*/
    for (int i = 0; i < 8; i++){
        Transformation3d shift = new Transformation3d();
        shift.translate(-0.5, -0.5, -0.5);
        Transformation3d scaleOp = new Transformation3d();
        scaleOp.scale(2, 2, 2);
        cube[i].transform(shift);
        cube[i].transform(scaleOp);
        cube[i].homogenize();
        cube[i].transform(view.nPer());
        //cube[i].homogenize();
    }

    Line3d la = new Line3d(a, c);
    Line3d lb = new Line3d(c, g);
    Line3d lc = new Line3d(g, e);
    Line3d ld = new Line3d(e, a);
    Line3d le = new Line3d(h, d);
    Line3d lf = new Line3d(d, f);
    Line3d lg = new Line3d(f, b);
    Line3d lh = new Line3d(b, h);
    Line3d li = new Line3d(f, g);
    Line3d lj = new Line3d(b, c);
    Line3d lk = new Line3d(d, e);
    Line3d ll = new Line3d(h, a);

    lines = new Line3d[]{la, lb, lc, ld, le, lf, lg, lh, li, lj, lk, ll};
  }

  /** Add newly recalculated objects to the picture. */
  public void updatePicture(Line3d[] objects, int nObjects) {
    picture = new CompoundGraphicObject2d();
    myDrawing.clear();
    myDrawing.add(picture);
    for (int i = 0; i < nObjects; i++) {
      if (objects[i] != null) {
        picture.add(objects[i].line2d());//
      }
    }

  }

  /**
  Reprocess the view for a new set of viewing parameters.
  */

  public void processNewView(View3dParameters v3dp) {
    loadViewParams(v3dp);
    processNewView();
  }

  /**
  Reprocess the view, using known existing viewing parameters.
  */

  public void processNewView() {
    geom(); /* ensure that geometry info is correct */
    Line3d[] _lines = lines;
    _lines = processViewingOp_PER(_lines, APP_N_OBJECTS);/**/
    updatePicture(_lines, APP_N_OBJECTS);
  }

}

