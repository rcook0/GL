package GraphicsPackage;

/**
* <P> 
* @author Ryan L Cook
*/

public class Point3d extends Matrix{

	public Point3d(double in_x, double in_y, double in_z) {
		super(4, 1, 1);
		m[0][0]=in_x;
		m[1][0]=in_y;
    m[2][0]=in_z;
		}// end constructor

  public Point3d(Vector4d v) {
    super(4, 1, 1);
		m[0][0]=v.x();
		m[1][0]=v.y();
    m[2][0]=v.z();
  }

	public double x() {
		return (m[0][0]);
		}

  public void x(double val) {
    m[0][0] = val;
  }

	public double y() {
		return (m[1][0]);
		}

  public void y(double val) {
    m[1][0] = val;
  }

  public double z() {
    return (m[2][0]);
    }

  public void z(double val) {
    m[2][0] = val;
  }

  public String toString(){
    return new String(m[0][0] + " " + m[1][0] + " " + m[2][0]);
    }
  
}//end class Point3d