package GraphicsPackage;

/**
Transformation3d provides procedures to set up transformation matrices for 
translation, rotation, shearing and scaling in the x, y and z axes.
* <P> 
* @author Ryan L Cook
*/

public class Transformation3d extends Matrix{

	public Transformation3d(){
		super(4, 4, 0);
		m[0][0]=1;
		m[1][1]=1;
		m[2][2]=1;
    m[3][3]=1;
		}

  /** Initialize a matrix for performing a translation */
	public void translate(double dx, double dy, double dz) {
		m[0][3]=dx;
		m[1][3]=dy;
    m[2][3]=dz;
    }

  /** Rotate about the Z axis */
	public void rotateZ(double theta) {
		m[0][0] = (double)Math.cos(theta);
		m[1][0] = (double)Math.sin(theta);
		m[0][1] = -(double)Math.sin(theta);
		m[1][1] = (double)Math.cos(theta);
  }

  /** Rotate about the X axis */
  public void rotateX(double theta) {
    m[1][1] = (double)Math.cos(theta);
    m[1][2] = (double)Math.sin(theta);
    m[1][2] = -(double)Math.sin(theta);
    m[2][2] = (double)Math.cos(theta);
  }

  /** Rotate about the Y axis */
  public void rotateY(double theta) {
    m[0][0] = (double)Math.cos(theta);
    m[2][0] = -(double)Math.sin(theta);
    m[0][2] = (double)Math.sin(theta);
    m[2][2] = (double)Math.cos(theta);
  }

  /** Scale */
  public void scale(double sx, double sy, double sz) {
    m[0][0] = sx;
    m[1][1] = sy;
    m[2][2] = sz;
  }

  /** Depth shear */
  public void shearZ(double shx, double shy) {
    m[0][2] = shx;
    m[1][2] = shy;
  }

  /** Shear along the x axis */
  public void shearX(double shy, double shz) {
    m[1][0] = shy;
    m[2][0] = shz;
  }

  /** Shear along the y axis */
  public void shearY(double shx, double shz) {
    m[0][1] = shx;
    m[2][1] = shz;
  }

  /**
  Construct the component vectors, Rx, Ry and Rz, of the rotation matrix and
  populate the transformation matrix with them such that the resulting matrix may
  be employed in the normalizing transformations of the parallel and perspective
  projections.
  */
  public void viewingRotation(Vector4d vpn, Vector4d vup) {

    Vector4d rz = vpn;
    rz.divide(vpn.length());

    Vector4d rx = Vector4d.product(vup, rz);
    rx.divide(rx.length());
    
    Vector4d ry = Vector4d.product(rz, rx);
    
    m[0][0] = rx.x();
    m[0][1] = rx.y();
    m[0][2] = rx.z();
    m[1][0] = ry.x();
    m[1][1] = ry.y();
    m[1][2] = ry.z();
    m[2][0] = rz.x();
    m[2][1] = rz.y();
    m[2][2] = rz.z();
    
  }

  /**
  Construct the transformation from the perspective-projection canonical view volume 
  to the parallel-projection canonical view volume.
  */
  public void tPerspectiveToParallelCVV(double F, double B, Vector4d prp){
    double vrpzz = -prp.z();
    double zmin = -(vrpzz + F)/(vrpzz + B);

    double m22 = 1/(1 + zmin);
    m[3][2] = -1;
    m[2][2] = m22;
    m[2][3] = -zmin * m22;
  }


  
}//end class Transformation3d

