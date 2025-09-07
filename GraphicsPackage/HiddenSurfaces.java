//package AnalogClock;
import java.util.*;
/**
 * A Class class.
 * <P>
 * @author 
 */
public class HiddenSurfaces {

  // Size of the frame buffer (with default values)
  private static final int XMAX = 100;
  private static final int YMAX = 100;
  private static final int BACKGROUND_VALUE = 64;

  /* Size of the depth buffer, equal to
  the maximum and minimum values of the clipping plane (with default values) */
  private static final int ZMIN = 0;
  private static final int ZMAX = 50;

  // Matrices holding the depth buffer and frame buffer
  /*private Matrix depthBuffer = new Matrix(YMAX + 1, XMAX + 1, BACKGROUND_VALUE);
  private Matrix frameBuffer = new Matrix(YMAX + 1, XMAX + 1, 0);*/

  
  /*
  Scan line algorithm fills out a list of intersections. 
  For each scan-line, the x-coordinate of each intersection is stored in a vector,
  which is then added to the vector of scans in the position corresponding to the
  y-coordinate of the scan line.
  */
  
  private Vector scans = new Vector();
  private Vector intersections = new Vector();
  
  /**
   * Constructor
   */
  public HiddenSurfaces() {
    
  }
/*
  void zBuffer(){
    int x, y;

    for (each polygon){
      for (each pixel in polygon's projection){
        double pz = polygon's z-value at pixel coords (x, y);
        if (pz >= ReadZ(x, y)) {
          WriteZ(x, y, pz);
          WritePixel(x, y, polygon's color at pixel coords (x, y));
        }
      }
    }
    
  }
*/
  // Scan-line algorithm for the projected polygon 
  private void scan(Polygon3d polygon) {
    //sort edges by increasing y-extent

    //repeat for scanline = minimum y-extent to maximum y-extent

    //    
  }

  public void WritePixel(int x, int y, int value){
    frameBuffer[y][x] = value;
  }

  public int ReadPixel(int x, int y){
    return frameBuffer[x][y];
  }

  public void WriteZ(int x, int y, int value){
    depthBuffer[y][x] = value;
  }

  public int ReadZ(int x, int y){
    return depthBuffer[y][x];
  }
}


