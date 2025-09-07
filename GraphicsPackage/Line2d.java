package GraphicsPackage;

/**
* <P>
* @author Ryan L Cook.
*/

import java.awt.*;

public class Line2d extends GraphicObject2d {

	private Point2d src;
	private Point2d dest;

	public Line2d (double x1, double y1, double x2, double y2) {
		src = new Point2d(x1,y1);
		dest = new Point2d(x2,y2);
		}//end constructor 

  /**
  Return a Point2d representing the position of the originating end of this Line2d. 
  */
  public Point2d getSourcePoint() {
    return src;
  }

  /**
  Return a Point2d representing the position of the destination end of this Line2d. 
  */
  public Point2d getDestinationPoint() {
    return dest;
  }

  public double gradient() {
    double grad = (dest.y() - src.y()) / (dest.x() - src.x());
    return grad;  
  }

  /*
  Does the specified line intersect this line?
  
  public boolean intersects(Point2d otherPoint) {
    return false;
  }
  */
	public void draw(Graphics g){
		super.draw(g);
		g.drawLine((int)src.x(), (int)src.y(), (int)dest.x(), (int)dest.y());
		}//end draw


	public void erase(Graphics g) {
		super.draw(g);
		g.drawLine((int)src.x(), (int)src.y(), (int)dest.x(), (int)dest.y());
		}//end erase


	public void transform(Transformation2d trans) {
		src.transform(trans);
		dest.transform(trans);
		}//end transform


}//end class Line2d
