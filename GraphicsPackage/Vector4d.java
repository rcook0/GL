package GraphicsPackage;

/**
 * Basic vector calculations.
 * <P>
 * @author Ryan L Cook
 */
public class Vector4d extends Matrix {

  /**
   * Constructor
   */
  public Vector4d() {
    super(4, 1, 0);
  }

  public Vector4d(double x, double y, double z, double h) {
    super(4, 1, 0);
    m[0][0] = x;
    m[1][0] = y;
    m[2][0] = z;
    m[3][0] = h;
  }

  public Vector4d(double x, double y, double z) {
    super(4, 1, 0);
    m[0][0] = x;
    m[1][0] = y;
    m[2][0] = z;
    m[3][0] = 1.0;
  }

  public Vector4d(Point3d p){
    super(4, 1, 0);
    m[0][0] = p.x();
    m[1][0] = p.y();
    m[2][0] = p.z();
    m[3][0] = 1.0;
  }

  /**
  Create the vector between the source and destination points.
  */
  public Vector4d(Point3d a, Point3d b){
    super(4, 1, 0);
    m[0][0] = b.x() - a.x();
    m[1][0] = b.y() - a.y();
    m[2][0] = b.z() - a.z();
    m[3][0] = 0.0;
  }

  public double x() { return m[0][0]; }
  public double y() { return m[1][0]; }
  public double z() { return m[2][0]; }
  public double h() { return m[3][0]; }
    
  /**
  Add the specified vector to this vector.
  */
  public void add(Vector4d v) {
    m[0][0] = m[0][0] + v.x();
    m[1][0] = m[1][0] + v.y();
    m[2][0] = m[2][0] + v.z();
    m[3][0] = m[3][0] + v.h();
  }

  /**
  Divide each component of this vector by the specified double-precision number.
  */
  public void divide(double n) {
    m[0][0] = m[0][0] / n;
    m[1][0] = m[1][0] / n;
    m[2][0] = m[2][0] / n;
    m[3][0] = m[3][0] / n;
  }

  public void multiply(double n) {
    m[0][0] = m[0][0] * n;
    m[1][0] = m[1][0] * n;
    m[2][0] = m[2][0] * n;
    m[3][0] = m[3][0] * n;
  }

  /**
  Calculate the length of this vector.
  */
  public double length() {
    return Math.sqrt(Math.pow(x(), 2) + Math.pow(y(), 2) + Math.pow(z(), 2) + Math.pow(h(), 2));
  }

  /**
  Rescale so that the fourth element of this vector is one, i.e. homogenous.
  */
  public void homogenize() {
    double w = m[3][0];
    if(w != 1.0) {
      m[0][0] = m[0][0] / w;
      m[1][0] = m[1][0] / w;
      m[2][0] = m[2][0] / w;
      m[3][0] = 1.0;
    }
  }
  
  /**
  Return a Vector that is the sum of the specified vectors.
  */
  static Vector4d sum(Vector4d v1, Vector4d v2) {
    return new Vector4d(v1.x() + v2.x(), v1.y() + v2.y(), v1.z() + v2.z(), v1.h() + v2.h());
  }

  /**
  Return a Vector that is the quotient of the specified vectors.
  */
  static Vector4d quotient(Vector4d v1, Vector4d v2) {
    return new Vector4d(v1.x() / v2.x(), v1.y() / v2.y(), v1.z() / v2.z(), v1.h() / v2.h());
  }

  /**
  Return a Vector that is the dot product of the specified vectors.
  */
  static Vector4d dotProduct(Vector4d u, Vector4d v) {
    double multI = u.x() * v.x();
    double multJ = u.y() * v.y();
    double multK = u.z() * v.z();
    return new Vector4d( multI, multJ, multK );
  }
  
  /**
  Return a Vector that is the product of the specified vectors.
  */
  static Vector4d product(Vector4d u, Vector4d v) {
    double multI = (u.y() * v.z()) - (u.z() * v.y());
    double multJ = (u.z() * v.x()) - (u.x() * v.z());
    double multK = (u.x() * v.y()) - (u.y() * v.x());
    return new Vector4d( multI, multJ, multK );
  }

  /**
  Return a Point3d that is the result of interpreting this vector as a 3d direction
  vector, ignoring homogeneity.
  */
  Point3d Point3d() {
    return new Point3d(m[0][0], m[1][0], m[2][0]);
  }

}

// ??Dynamically link vectors and points so that changes automatically follow through
// - if we calculate a vector between two points, and points hence move, the Vector
// should be dynamically recalculated.


