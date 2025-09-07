package GraphicsPackage;

import java.util.Vector;

/**
* <P> 
* @author Ryan L Cook
*/
 
public class RadianSinLookup {

/** This inverse-sine calculator is designed as a form of compensation for the lack
of a function to carry out this task. It could easily be extended to cover the
inverse cosine and tangent, if needed. */

  Vector radianAngles = new Vector(360);
  Vector sines = new Vector(360);
  
  int mapGranularity = 360; // number of entries in the table
  double increment = 1.0; // degrees difference between adjacent positions in the table

  public static final double RSL_VALUE_NOT_FOUND = 0.0;

  public void dump() {
    for (int i = 0; i < 360; i ++) {
      double val1 = ((DoubleObject)(radianAngles.get(i))).getValue();
      double val2 = ((DoubleObject)(sines.get(i))).getValue();
      System.out.println(i + " " + val1 + " " + val2);
      System.out.println(Math.PI);
    }
  }
  
/* May use 720 * .5-degree changes for proper estimation of sin. */
/* Constructor must make an index to speed up searching. */
/* Order sines for binary search? */
  
  /**
   * main
   * @param args
   */

  /** Construct a table mapping radian angles to their trigonometric
  sine equivalent. The index of an entry in the sin table gives its equivalent
  value in degrees. 360 entries are created, covering the 360 integer angles in
  a circle. */
  public RadianSinLookup() {
  // Loop increment default of 1.0 and mapGranularity of 360 are left unchanged.
    for (int i = 0; i < 360; i = i + 1) {
      radianAngles.add(new DoubleObject(radians(i)));
      sines.add(new DoubleObject(Math.sin(radians(i))));
      }
  }

  /** For greater accuracy in estimating the sin function, the user may request that
  the table be built with a larger number of entries, with finer spacing between them. */
  public RadianSinLookup(int customGranularity) {
    mapGranularity = customGranularity;
    increment = 360/customGranularity;
    
    for (int i = 0; i < mapGranularity; i++) {
      // Scale the table to 2PI.
      double tableIndex = (double)i * 360/mapGranularity;
      radianAngles.add(new DoubleObject(radians(tableIndex)));
      sines.add(new DoubleObject(Math.sin(radians(tableIndex))));
      }
  }

  /** Look up the closest entry in the trig-sine table to the specified
  double-precision number and return the corresponding radian angle. */
  public double radianAngleOf(double trigSinNumber) {
    for (int i = 0; i < (mapGranularity - 1); i++) {
      /* Return if trigSinNumber is between the value in adjacent positions in
      the search. */
      double i0 = ((DoubleObject)sines.get(i)).getValue();
      double i1 = ((DoubleObject)sines.get(i + 1)).getValue();

      if ( (i0 <= trigSinNumber) && (trigSinNumber <= i1) ) {
        // Check which of i0 and i1 provides the closer approximation (by being closer to trigSinNumber).
        if ( (trigSinNumber - i0) < (i1 - trigSinNumber) )  {
          return ((DoubleObject)(radianAngles.get(i))).getValue();
        }
        else 
        {
          return ((DoubleObject)(radianAngles.get(i + 1))).getValue();
        }
      }
    }
    return this.RSL_VALUE_NOT_FOUND;
  }

  /**  Convert a double-precision degree angle to radians. */
  public double radians(double degreeAngle) {
    return 2*Math.PI*(degreeAngle/360);
  }

  /** Compute the degree measure of an angle specified in radians. */
  public double radiansToDegrees(double radianAngle) {
    return 360.0*(radianAngle/(2*Math.PI));
  }

  /** Compute the trigonometric sine of an integer degree angle. */
  public double trigSin(int degreeAngle) {
    return Math.sin(radians(degreeAngle));
  }

  /** Compute the trigonometric sine of a double-precision degree angle. */
  public double trigSin(double degreeAngle) {
    return Math.sin(radians(degreeAngle));
  }


  
  /** Test stub. */
  public static void main(String[] args) {
    RadianSinLookup table1 = new RadianSinLookup();
/*    double myNegAng = -0.156434465; // 189 deg.
    double myNegAng1 = 0.94573;
    double myRadianAng = table1.radianAngleOf(myNegAng);
    System.out.println("Inverse sine of " + myNegAng + " is: " + myRadianAng + " PI radians or " + table1.radiansToDegrees(myRadianAng));
    System.out.println("Inverse sine of " + myNegAng1 + " is: " + table1.radianAngleOf(myNegAng1) + " PI radians or " + table1.radiansToDegrees(table1.radianAngleOf(myNegAng1)));
*/
    System.out.println("Conversion table: ");
    table1.dump();
    System.out.println("===========");
    System.out.println("Testing radianAngleOf() on the 360 degrees of the Sine function: ");
    for (int i = 0; i < 360; i++) {
      System.out.println(i + " " + table1.radiansToDegrees(table1.radianAngleOf(Math.sin(table1.radians(i)))));
    }
    System.out.println("===========");
    System.out.println("Sign function is as follows (n degrees -> radians -> Math.sin() for n=0 to 359) :  ");
    for (int i = 0; i < 360; i++) 
      System.out.println(Math.sin(table1.radians(i)));

  }
    
}


