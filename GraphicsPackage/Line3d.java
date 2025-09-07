package GraphicsPackage;

/**
* <P>
* @author Ryan L Cook.
*/

import java.awt.*;

public class Line3d {

	private Point3d src;
	private Point3d dest;

	public Line3d (double x1, double y1, double x2, double y2, double z1, double z2) {
		src = new Point3d(x1, y1, z1);
		dest = new Point3d(x2, y2, z2);
		}

  public Line3d (Point3d pSrc, Point3d pDest) {
    src = pSrc;
    dest = pDest;
  }

  public Line3d (Vector4d a, Vector4d b) {
    src = new Point3d(a.x(), a.y(), a.z());
    dest = new Point3d(b.x(), b.y(), b.z());
  }

  /**
  Return a Point3d representing the position of the originating end of this Line3d. 
  */
  public Point3d getSourcePoint() {
    return src;
  }

  /**
  Return a Point3d representing the position of the destination end of this Line3d. 
  */
  public Point3d getDestinationPoint() {
    return dest;
  }

  /**
  Return a Line2d by stripping the z-coordinate of each endpoint of this Line3d.
  */
  public Line2d line2d() {
    Point3d src = getSourcePoint();
    Point3d dest = getDestinationPoint();
    return new Line2d(src.x(), src.y(), dest.x(), dest.y());
  }

  public void transform(Transformation3d matrix) {
    src.transform(matrix);
    dest.transform(matrix);
  }
  
  /*

  public double gradient() {
    //throw new MethodNotImplementedException("AnalogClock.Line3d.gradient()");
  }*/

  /*
  Does the specified line intersect this line?
  
  public boolean intersects(Point3d otherPoint) {
    return false;
  }
  */


  }
