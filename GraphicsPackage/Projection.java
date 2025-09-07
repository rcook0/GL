package AnalogClock;

import AnalogClock.*;

/**
 * Mathematical description of the basic planar geometric projection,
 assuming that the projection plane is normal, perpendicular, to the z axis at z=d for 
 perspective projection, and, for a parallel projection, the projection plane
 is z=o.

 
 * <P>
 * @author Ryan L Cook.
 */
public class Projection extends Matrix {

  /**
   * Allocate and initialize a matrix for the projection. The following methods
   make the matrix into a perspective or orthographic projection.
   */
  public Projection() {
    super(4, 4, 0);
    m[0][0] = 1;
    m[1][1] = 1;
    
  }

  /**
  Perspective projection - when centre of projection is at the origin.
  */
  public void perspective(double d) {
    m[2][2] = 1;
    m[3][2] = 1/d;
  }


  /**
  Alternative perspective projection - 
  */
  public void perspectiveII(double d) {
    m[3][2] = 1/d;
    m[3][3] = 1;
  }


  /**
  Orthographic projection - when dir. of projection parallel to z axis.
  */
  public void orthographic() {
    m[3][3] = 0;
  
  }

  /**
Generalized projection matrix - removes the restrictions of perspective
and orthographic projections, and integrates parallel and perspective projections
into a single formulation.
When Q is finite, the following matrix defines a one-point perspective projection.

The general matrix is specialized for the following projections:

               Zp     Q        [dx, dy, dz]
             ==================================================
Orthographic | 0      Inf.     [0, 0, -1]
Persective   | d      d        [0, 0, -1]
Persective'  | 0      d        [0, 0, -1]
Cavalier     | 0      Inf.     [cos(alpha), sin(alpha), -1]
Cabinet      | 0,     Inf.     [cos(alpha)/2, sin(alpha)/2, -1]

*/

  public void general(
    double Q, // distance, Q, to the center of projection
    Point3d p, // projected point
    Matrix[3][1] d // normalized direction vector
    )
  {
    m[0][2] = -(d[0]/d[2]);
    m[0][3] = p.z() * (d[0]/d[2]);
    m[1][2] = -(d[1]/d[2]);
    m[1][3] = p.z() * (d[1]/d[2]);
    m[2][2] = -(p.z() / (Q * d[2]));
    m[2][3] = ( (Math.exp(p.x(), 2)) / (Q * d[2]) ) + p.z();
    m[3][2] = - 1 / (Q * d[z]);
    m[3][3] = 1 + ( p.z() / (Q * d[2]) );
  }
    



}



 