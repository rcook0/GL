package GraphicsPackage;

/**
* <P> 
* @author Ryan L Cook
*/

public class Transformation2d extends Matrix{

	public Transformation2d(){
		super(3, 3,0);
		m[0][0]=1;
		m[1][1]=1;
		m[2][2]=1;
		}//constructor

	public void translate(double x, double y) {
		m[0][2]=x;
		m[1][2]=y;
		}//translate

	public void rotate(double angle) {
		m[0][0] = (double)Math.cos(angle);
		m[1][0] = -(double)Math.sin(angle);
		m[0][1] = (double)Math.sin(angle);
		m[1][1] = (double)Math.cos(angle);
		}//rotate

}//end class Transformation2d
