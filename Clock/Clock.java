/**
<P>
@author Ryan L Cook
*/

import java.util.*;
import java.awt.Dimension;
import java.awt.Color;
import GraphicsPackage.*;

public class Clock extends ApplicationFrame  {

  private Transformation2d myTrans = new Transformation2d();

  private CompoundGraphicObject2d dynGeom = new CompoundGraphicObject2d();

  /**
  The following instance variables store the geometric parameters of the clock. 
  These include the size and position of the face, and references to the six hands
  which must be updated independently of the clock's aesthetic appearance, which is
  calculated relative to the face and completed in the Clock object's initialization.
  Though moving parts are updated separately from the static parts, they share certain
  elements of the geometric state because they are drawn against the geometric
  specifications of the clock, that is, the static part. The instance variables are
  not defined as static because the vital statistics may change as and if the output
  window size changes (although this is not a problem for an applet, in which the
  canvas window is not affected by changes in the shape of the containing browser
  page, this Clock is designed to wrap the output window in an application frame,
  which would be resizable as a matter of convenience).

  Generally, static geometry is created in the constructor, while moving parts
  are calculated by the updatePicture() method.
  */


  private Point2d mainFaceCentre = new Point2d(200, 170);

  private int faceRadius = 150;

  private int chronoHandRadius = 0;

  private int numeralRadius = 0;

  private double handWidth = 0;

// All hands point straight upward by default.
  
  private int currentTimeMinutes = 0;

  private int currentTimeSeconds = 0;

  private int currentTimeHours = 0;

// The following variables store the state of the widgets used for direct maipulation.

  private boolean minuteHandSelect = false;

  private boolean hourHandSelect = false;

  private boolean secondHandSelect = false;  

  // The following store the state of the chronometer, in the time units used by its dials.
  
  private int sweepSecondValue = 0;

  private int hourTotaliserValue = 0;

  private int minuteTotaliserValue = 0;

  // The following provide state space for the centre of the totaliser dials.

  private Point2d minTotC = new Point2d(0.0, 0.0);

  private Point2d hourTotC = new Point2d(0.0, 0.0);

  private Point2d sweepSecC = new Point2d(0.0, 0.0);

  // The Gregorian Calendar's clock can be read as either 12 or 24 hours.
  // Either is permissible, but the 12-hour representation is easier.
  private static final int CLOCK_12 = 12;
  private static final int CLOCK_24 = 24;

  private final int CLOCK_TYPE = CLOCK_12;

//==============================================================================
  
  private String rtInf(){ // debugging convenience
    return (
           "mainFaceCentre: " + mainFaceCentre.x() + ", " + mainFaceCentre.y() + "\n"
           + "faceRadius: " + faceRadius
           + "numeralRadius: " + numeralRadius
           );
  }

//==============================================================================


/**
Read the current time and the position and use of the mouse.

With no mouse interaction, simply draw the hands of the clock as they are to appear
on the face of the clock, i.e. in the position corresponding to the present time.
Seconds are normally recorded more than twice per second, given a SLOW (= 4 fps) 
frame rate update, so the animation normally moves in correct rhythm, but always 
shows the correct second, minute and hour time.

With mouse interaction, we have to find the widget that has the mouse pointer,
if any, and get the owning object. If the mouse is then dragged, the object must move
across 2D space, over several frames of animation, in correspondence with the motion
of the mouse. This requires tracking the mouse motion, calculating the correct
bearing of the hand for the next frame of animation, accordingly updating the picture
and setting the Calendar time (GregorianCalendar.set..(..)) to the time that the
hand's new position corresponds to.
*/

    public void updatePicture(){

         /**
         Read the calendar for the current time.
         */
         GregorianCalendar timeNow = new GregorianCalendar();
         currentTimeSeconds = timeNow.get(timeNow.SECOND);
         currentTimeMinutes = timeNow.get(timeNow.MINUTE);
         switch (CLOCK_TYPE) {
           case CLOCK_12 :  currentTimeHours = timeNow.get(timeNow.HOUR); 
           case CLOCK_24 :  currentTimeHours = timeNow.get(timeNow.HOUR_OF_DAY);
           default : currentTimeHours = timeNow.get(timeNow.HOUR); // 12-hour clock
           }

         /** 
         Create components to build the clock's hands
         */
         CompoundGraphicObject2d secHand = new CompoundGraphicObject2d();
         CompoundGraphicObject2d minHand = new CompoundGraphicObject2d();
         CompoundGraphicObject2d hourHand = new CompoundGraphicObject2d();
         CompoundGraphicObject2d hourTotaliser = new CompoundGraphicObject2d();
         CompoundGraphicObject2d minuteTotaliser = new CompoundGraphicObject2d();
         CompoundGraphicObject2d sweepSecHand = new CompoundGraphicObject2d();


         /*
  Placing each time hand at the 1200 position, the position of the tip of the 
  hand is {x = mainHandCentre.x + theHandLength, y = mainHandCentre.y - theHandLength)
  where secondHandLength = numeralRadius, minuteHandLength = (4/5)numeralRadius, 
  hourHandLength = (3/5)numeralRadius, and the hand has its local origin aligned 
  with the mainFaceCentre. These facts allow a Hand to be defined by its centre and
  outer points, which may be rotated by the angle at which the hand would show the
  correct current time. 
  Current-time hands go to bearing: (2*PI)*value/nValues.
  For example, at 15 minutes past the hour, minute hand is at (2*PI)*(15/60) = PI/2
  Initially place hand at O(0, 0), rotate by X = PI/2, translate to mainFaceCentre.
  This results in the hand being drawn for the current time.
  */

         /** 
         Define the full length of each hand in terms of the dist. from the face's centre
         to the numerals (referred to as numeralRadius)
         */
         int secondHandLength = numeralRadius; 
         int minuteHandLength = (int)((0.8)*(double)numeralRadius);
         int hourHandLength = (int)((0.6)*(double)numeralRadius);

         /** 
         Create widgets for mouse-dragging the hands. Each widget is placed at
         the end of its respective hand, with a size of 20 pixels by 20 pixels, 
         initially visible and referring to its corresponding shape object as its owner -
         i.e. One of the widgets is pinned to the second hand, one to the minute
         hand and one to the hour hand.
         */
         Widget2d secondHandWidget = new Widget2d(           
             new Point2d(mainFaceCentre.x(), mainFaceCentre.y() - secondHandLength), 
             new Dimension(20, 20), true, secHand);
         Widget2d minuteHandWidget = new Widget2d(           
             new Point2d(mainFaceCentre.x(), mainFaceCentre.y() - minuteHandLength), 
             new Dimension(20, 20), true, minHand);
         Widget2d hourHandWidget = new Widget2d(
             new Point2d(mainFaceCentre.x(), mainFaceCentre.y() - hourHandLength), 
             new Dimension(20, 20), true, hourHand);

         /** 
         Remember the widget's state from the last cycle of updating 
         the picture. 
         */
         if(secondHandSelect)  secondHandWidget.select();
         if(minuteHandSelect)  minuteHandWidget.select();
         if(hourHandSelect)    hourHandWidget.select();

             
         // Build the moving parts in upward position
         secHand.add(new Line2d(mainFaceCentre.x(), mainFaceCentre.y(), mainFaceCentre.x(), mainFaceCentre.y() - (double)secondHandLength ) );

         secHand.add(secondHandWidget);

         minHand.add(new Line2d(mainFaceCentre.x(), mainFaceCentre.y(), mainFaceCentre.x(), mainFaceCentre.y() - (double)minuteHandLength ) );

         minHand.add(minuteHandWidget);
         hourHand.add(new Line2d(mainFaceCentre.x(), mainFaceCentre.y(), mainFaceCentre.x(), mainFaceCentre.y() - (double)hourHandLength ) );

         hourHand.add(hourHandWidget);
         hourTotaliser.add(new Line2d(hourTotC.x(), hourTotC.y(), hourTotC.x(), hourTotC.y() - (double)chronoHandRadius) );
         minuteTotaliser.add(new Line2d(minTotC.x(), minTotC.y(), minTotC.x(), minTotC.y() - (double)chronoHandRadius) );
         sweepSecHand.add(new Line2d(sweepSecC.x(), sweepSecC.y(), sweepSecC.x(), sweepSecC.y() - (double)chronoHandRadius) );
         // Bezier2d c1 = bCurve(...); secHand.add(c1);
         /**
         Build the body of each hand. Use two bezier curves per hand, set at two
         thirds of the length of the hand.
         Each curve includes the face centre as the primary control point;
         the secondary control point is calculated from this point and the end of the guiding
         line for each hand (at two thirds of the way from the centre to the outer point),
         */

         Point2d fc = new Point2d(mainFaceCentre.x(), mainFaceCentre.y());
         
         secHand.add(bezierPair(fc, new Point2d(fc.x(), fc.y() - ((2.0/3.0)*secondHandLength)), 0.20 * secondHandLength) );
         
         minHand.add(bezierPair(fc, new Point2d(fc.x(), fc.y() - ((2.0/3.0)*minuteHandLength)), 0.20 * minuteHandLength));
         
         hourHand.add(bezierPair(fc, new Point2d(fc.x(), fc.y() - ((2.0/3.0)*hourHandLength)), 0.20 * hourHandLength));
         

         /*
         Calculate where each hand is to be drawn, as an angle of rotation from
         the 12 o'clock position.
         If one of the widgets is currently being dragged, then its containing
         hand should be positioned according to the current drag position's angle
         of heading with respect to the centre of the main clock face. When animated,
         the hand then appears to move with the mouse. When the mouse is later released,
         the hand's angle of rotation is converted back to a time to be written
         back to the calendar.
         */



         double secondsAngle = -Math.PI*2*currentTimeSeconds/60;
         double minutesAngle = -Math.PI*2*currentTimeMinutes/60;
         double hoursAngle = -Math.PI*2*currentTimeHours/12; // draw a 12-hour clock
         
         if( myBuffer.dragging() ) 
         {
           Point2d selPoint = myBuffer.getSelectionPoint();
           selPoint = new Point2d(selPoint.x(), myBuffer.getHeight() - selPoint.y());
           if ( secondHandSelect ) {
             secondsAngle = -( secondHandWidget.angleOfRotation(new Point2d(mainFaceCentre.x(), myBuffer.getHeight() - mainFaceCentre.y()), selPoint) );
           }
           if ( minuteHandSelect ) {
             minutesAngle = -( minuteHandWidget.angleOfRotation(new Point2d(mainFaceCentre.x(), myBuffer.getHeight() - mainFaceCentre.y()), selPoint) );
           }
           if ( hourHandSelect ) {
             hoursAngle = -( hourHandWidget.angleOfRotation(new Point2d(mainFaceCentre.x(), myBuffer.getHeight() - mainFaceCentre.y()), selPoint) );
           }
         }



         /**
         Now build the new state of the moving parts... (previous state is dynGeom)
         */
         //- second hand
         Transformation2d secHT = new Transformation2d();
         Transformation2d secHTt = new Transformation2d();
         Transformation2d secHTr = new Transformation2d();
         Transformation2d secHTtt = new Transformation2d();
         secHTt.translate(-mainFaceCentre.x(), -mainFaceCentre.y());
         secHTr.rotate(secondsAngle);
         secHTtt.translate(mainFaceCentre.x(), mainFaceCentre.y());
         secHT.transform(secHTt);
         secHT.transform(secHTr);
         secHT.transform(secHTtt);
         secHand.transform(secHT);
         //- minute hand
         Transformation2d minHT = new Transformation2d();
         Transformation2d minHTt = new Transformation2d();
         Transformation2d minHTr = new Transformation2d();
         Transformation2d minHTtt = new Transformation2d();
         minHTt.translate(-mainFaceCentre.x(), -mainFaceCentre.y());
         minHTr.rotate(minutesAngle);
         minHTtt.translate(mainFaceCentre.x(), mainFaceCentre.y());
         minHT.transform(minHTt);
         minHT.transform(minHTr);
         minHT.transform(minHTtt);
         minHand.transform(minHT);
         //- hour hand
         Transformation2d hourHT = new Transformation2d();
         Transformation2d hourHTt = new Transformation2d();
         Transformation2d hourHTr = new Transformation2d();
         Transformation2d hourHTtt = new Transformation2d();
         hourHTt.translate(-mainFaceCentre.x(), -mainFaceCentre.y());
         hourHTr.rotate(hoursAngle); 
         hourHTtt.translate(mainFaceCentre.x(), mainFaceCentre.y());
         hourHT.transform(hourHTt);
         hourHT.transform(hourHTr);
         hourHT.transform(hourHTtt);
         hourHand.transform(hourHT);


         
         /**
         If the buffer's panel has been pressed, we check each widget to find
         out if it was pressed on. If the click occurred inside the widget's bounding
         box, change its colour to indicate that it holds a selection; otherwise, 
         deselect it. If the mouse is being dragged, and the widget was already 
         selected (press -> drag) then use the event location to work out where to
         draw the hand for this frame.
         */ 
         if( myBuffer.currentSelectionPointIsNew() && (!myBuffer.dragging()) ) 
         {
           Point2d selPoint = myBuffer.getSelectionPoint();
           if ( secondHandWidget.hasPoint((int)selPoint.x(), (int)selPoint.y()) ) {
             secondHandSelect = true;
           }
           else
           {
             secondHandSelect = false;
           }

           if ( minuteHandWidget.hasPoint((int)selPoint.x(), (int)selPoint.y()) ) {
             minuteHandSelect = true;
           }
           else
           {
             minuteHandSelect = false;
           }

           if ( hourHandWidget.hasPoint((int)selPoint.x(), (int)selPoint.y()) ) {
             hourHandSelect = true;
           }
           else
           {
             hourHandSelect = false;
           }
         }


         
         CompoundGraphicObject2d newHandState = new CompoundGraphicObject2d();
         newHandState.add(secHand);
         newHandState.add(minHand);
         newHandState.add(hourHand);
         newHandState.add(hourTotaliser);
         newHandState.add(minuteTotaliser);
         newHandState.add(sweepSecHand);

         /**
         Write the new state to the geometry hierarchy.
         */
         
         dynGeom.clear();
         dynGeom.add(newHandState);
    }


private Bezier2d bCurve(Point2d p1, Point2d p2, Point2d p3, Point2d p4) {

  Bezier2d curve = new Bezier2d();
  curve.add(p1);
  curve.add(p2);
  curve.add(p3);
  curve.add(p4);
  return curve;

}
    
/*(it might improve matters if the Clock is given a 'factory' for hands,
dials.)*/
  
//==============================================================================


public Clock(){

  // Initialize the moving part of the picture.
  dynGeom = new CompoundGraphicObject2d();

  setSize(new java.awt.Dimension(400, 400));

  /**
  The static state of the Clock is defined in the constructor, declaratively,
  along with any transformation matrices that need to be set up for
  recalculating the position of the hand at a given time.
  All operations on the clock that put these transfomations and other
  operations into effect are defined in the AnalogClock.Clock.run() method.
  */


  // The following statements describe the static part of the clock's geometry.


  /**
  Define some graphic parameters for the clock. All of the clock's geometries are
  defined in terms of one another, and in terms of central coordinates like the clock
  face position and centre, so that the geometry can be made to adapt dynamically to
  change in the horizontal and vertical size (but not position) of the window; this should only 
  have a direct influence on the centre and radius of the main face. 
  */

  // Centre of the clock = point of intersection of the hands.
  mainFaceCentre = new Point2d(getSize().getWidth()/2, getSize().getHeight()/2-30);
  // Face size determined by the radius of the inner rim.
  int irRadius = 150; // the numerals and scales appear just inside the inner rim.
  faceRadius = irRadius;
  // An outer rim is drawn at 4/5 of the radius of the inner rim.
  int orRadius = (int)(1.125*(double)irRadius);
  // numeral radius defines where numerals are drawn ( at intervals of PI/6 )
  numeralRadius = (int)(0.9*(double)irRadius);
  // Totaliser faces are positioned in terms of the main face.
  minTotC = new Point2d(mainFaceCentre.x()+(0.5*faceRadius), mainFaceCentre.y());
  hourTotC = new Point2d(mainFaceCentre.x()-(0.5*faceRadius), mainFaceCentre.y());
  sweepSecC = new Point2d(mainFaceCentre.x(), mainFaceCentre.y()+(0.5*faceRadius));
  int totaliserRadius = (int)(0.25*faceRadius);
  chronoHandRadius = (int)(0.8*totaliserRadius);
  
  CompoundGraphicObject2d clock = new CompoundGraphicObject2d();
  CompoundGraphicObject2d face = new CompoundGraphicObject2d();
  CompoundGraphicObject2d hub = new CompoundGraphicObject2d();
  CompoundGraphicObject2d rim = new CompoundGraphicObject2d();
  CompoundGraphicObject2d numerals = new CompoundGraphicObject2d();

  face.add(dynGeom);

  myDrawing.add(clock);
  clock.add(face);
  face.add(new BresenhamCircle(mainFaceCentre, faceRadius));
  rim.add(new BresenhamCircle(mainFaceCentre, orRadius));
  rim.add(new BresenhamCircle(mainFaceCentre, irRadius));
  face.add(rim);
  face.add(hub);
  hub.add(new BresenhamCircle(mainFaceCentre, numeralRadius/12));//ring at base of second hand
  hub.add(new BresenhamCircle(mainFaceCentre, numeralRadius/18));//ring at base of minute hand
  hub.add(new BresenhamCircle(mainFaceCentre, numeralRadius/24));//ring at base of hour hand
  //(note, the ring would move with the hand in a real clock, but static circles are fine for this simulation.
  face.add(new BresenhamCircle(minTotC, totaliserRadius));
  face.add(new BresenhamCircle(hourTotC, totaliserRadius));
  face.add(new BresenhamCircle(sweepSecC, totaliserRadius));
  

  /**
  To draw the numerals, originate an imaginary line at the centre of the main face,
  as long as the length numeralRadius, and rotate the line anti-clockwise by PI/6 12 
  times, drawing numeral x each time at the resultant position of the outer end of 
  the line.
  */
  Transformation2d toOrigin = new Transformation2d();//
  Transformation2d rotation = new Transformation2d();//
  Transformation2d toPos = new Transformation2d();//
  toOrigin.translate(-mainFaceCentre.x(), -mainFaceCentre.y());
  rotation.rotate(Math.PI/6);
  toPos.translate(mainFaceCentre.x(), mainFaceCentre.y());
  Transformation2d drawNumerals = new Transformation2d();
  drawNumerals.transform(toOrigin);
  drawNumerals.transform(rotation);
  drawNumerals.transform(toPos);

  Point2d centre = mainFaceCentre;
  Line2d line = new Line2d(centre.x(), centre.y(), centre.x(), centre.y() - numeralRadius);

  for (int i = 12; i > 0; i--) {
    /*
    Draw the numeral, using the revolving i-value, at a position derived from
    the position of the line.
    */
    Point2d pt = line.getDestinationPoint();
    numerals.add(new Numeral(toChar(i), pt));
    
    // Rotate our imaginary line to position for the next numeral.
    line.transform(drawNumerals);
  }
  face.add(numerals);
  
  /**
  For the final cosmetic addition to the clock face, the rim contains markings
  placed at equal angular spacing with respect to the main face, using the same
  technique as previously, only adding the actual template to the face at each
  position.
  */

}

//==============================================================================
//Some auxiliary functions that help to build the Clock geometry.
//

/**
Make character arrays to write the Clock's numerals.
*/

private char[] toChar(int i) {
  switch (i) {
  case 1: return new char[]{'1', ' '};
  case 2: return new char[]{'2', ' '};
  case 3: return new char[]{'3', ' '};
  case 4: return new char[]{'4', ' '};
  case 5: return new char[]{'5', ' '};
  case 6: return new char[]{'6', ' '};
  case 7: return new char[]{'7', ' '};
  case 8: return new char[]{'8', ' '};
  case 9: return new char[]{'9', ' '};
  case 10: return new char[]{'1', '0'};
  case 11: return new char[]{'1', '1'};
  case 12: return new char[]{'1', '2'};
  default: return null;
  }
}

/**
Calculate a point directly between two specified points, at the position
determined by the ratio of ( distance from src : distance between src and dest ).
*/

private Point2d mid(double splitRatio, Point2d src, Point2d dest) {
  Point2d pS = src;
  Point2d pD = dest;
  double x = src.x() + (splitRatio*(dest.x() - src.x()));
  double y = src.y() + (splitRatio*(dest.y() - src.y()));
  Point2d pR = new Point2d(x, y);
  return pR;
}

/**
Generate a pair of Bezier curves related by common endpoints and double symmetry,
primarily about their connecting line, so that the third and fourth control points
are created at the four points of intersection of two lines perpendicular, and two lines
parallel, to the primary line of symmetry, with the two parallel lines separated
by (a) units from this symmetry, and the two perpendicular lines cutting this
symmetry line at each side of the absolute midpoint, at a distance of one quarter
the separation of the end { src<----->dest } points. The function returns a packet
of two Bezier curves defined according to this specification, for the supplied
start point, end point and (a)-value. The intended benefit of performing these
calculations automatically is that the coordinates of all eight points in the two
curves never have to be hard-wired; it is much easier to describe the shape with
just a start point, end point and width parameter.
*/ 

private CompoundGraphicObject2d bezierPair(Point2d start, Point2d end, double a) {
  // Start with our two points and a constructive tree of two Bezier curves.
  Point2d p1 = start;
  Point2d p2 = end;
  double sep = a;
  Bezier2d b1 = new Bezier2d();
  Bezier2d b2 = new Bezier2d();
  CompoundGraphicObject2d ret = new CompoundGraphicObject2d();
  ret.add(b1);
  ret.add(b2);
  // Define the Bezier curves with the common end points.
  b1.add(p1);
  //b1.add(p2);
  b2.add(new Point2d(p1.x(), p1.y()));
  //b2.add(p2);
  // The following four lines are included for testing.
  b1.add(new Point2d(p1.x() - a, p1.y() - (3*a)));//upperleft
  b1.add(new Point2d(p1.x() - a, p1.y() - a)); //lower left above hub
  b2.add(new Point2d(p1.x() + a, p1.y() - (3*a)));//upper right
  b2.add(new Point2d(p1.x() + a, p1.y() - a));// lower right
  
  
  
  /* --ISOLATE
  The following working algorithm generalises the above code for any two points in 
  the coordinate system. The pair of curves will draw correctly, but the code may be
  left out of the build for testing.
  */
  /*
  // Find out the perpendicular bisectors of the main line.
  Point2d mainBisPt1 = mid(0.25, p1, p2);
  Point2d mainBisPt2 = mid(0.75, p1, p2);
  double gradAtPt1 = -1/((p2.y() - p1.y()) / (p2.x() - p1.x()));
  double gradAtPt2 = gradAtPt1;
  // (these pts and grads define the p/b's
  // The first, p3, of four control points (through p7) is found using simple trigonometry, then the
  // other four are found by adding to this point the vector to mainBisP2 and from
  // mainBisP2 to mainBisP1, in specific configurations.
  RadianSinLookup rsl = new RadianSinLookup(); // use .radianAngleOf() as inverse sine.
  // >> interested in cos of angle that perpendicular bisector makes with x-axis.
  double dx = a * Math.cos (Math.sqrt(Math.pow(rsl.radianAngleOf(gradAtPt2), 2)));
  double x = mainBisPt2.x() - dx;
  // From the line equation for two points. y - b = m ( x - a ) 
  double y = mainBisPt2.y() + ( gradAtPt2 * ( x - mainBisPt2.x() ) );
  
  Point2d p3 = new Point2d(x, y);
  b1.add(p3);
  // Use bisection points and p3 to calculate two basic vectors (Point2d for field convenience)
  Point2d vShort = new Point2d(mainBisPt2.x() - p3.x(), mainBisPt2.y() - p3.y());
  Point2d vLong = new Point2d(mainBisPt1.x() - mainBisPt2.x(), mainBisPt1.y() - mainBisPt2.y());
  // These vectors can be used constructively to obtain the three unknown control points:
  // First, double the short vector.
  Point2d vShort2 = new Point2d(vShort.x() * 2, vShort.y() * 2);
  // Now focus on vLong and vShort2.
  Point2d p4 = new Point2d(p3.x() + vLong.x(), p3.y() + vLong.y());
  b1.add(p4);
  Point2d p5 = new Point2d(p4.x() + vShort2.x(), p4.y() + vShort2.y());
  b2.add(p5);
  Point2d p6 = new Point2d(p3.x() + vShort2.x(), p3.y() + vShort2.y());
  b2.add(p6);

  ISOLATE-- */
  
  // Add the common end points of the pair of Bezier curves.
  b1.add(p2);
  // --Avoid rotating the end point twice by replicating it:
  b2.add(new Point2d(p2.x(), p2.y()));

  /*
  System.out.println("--");
  System.out.println(p1.x() + " " + p1.y());
  System.out.println(p2.x() + " " + p2.y());
  System.out.println(p3.x() + " " + p3.y());
  System.out.println(p4.x() + " " + p4.y());
  System.out.println(p5.x() + " " + p5.y());
  System.out.println(p6.x() + " " + p6.y());
  */
  
  // Deliver the final result; */
  return ret;
}

//==============================================================================


public static void main(String[] args) 	{

  try {
		Clock frame = new Clock();
    frame.setMainMenu(new MainMenu());
		frame.initComponents();
		}
	catch (Exception e) {
		e.printStackTrace();
		}
}//end main

//==============================================================================

public void initComponents() throws Exception {
    super.initComponents();

    setBackground(Color.white);
    // Location is in the screen's coordinate space.
		setLocation(new java.awt.Point(200, 150));
    // Title specifies a title for the frame
    setTitle("Analog Clock");
    //setResizable(false); // for now, restrict the app window dimensions.
    setVisible(true);

	}//end - initComponents

//==============================================================================

/**
The face is drawn every 0.25 seconds or so, at which time the face is 
constructed according to the current time. Only six parts move - three time hands
and three totaliser hands - whilst the rest of the watch is generic. By drawing the
clock each time it is to be displayed, we obtain a time display that is accurate
to the system time, within the time required to calculate and display the clock.
Factoring out the non-moving part of the clock saves processor time, thus improving
the millisecond accuracy of the display. 
*/

/** Time-dependant picture updates are done here, under control by the timer. 
The static parts, having been added during the init. of the clock, remain
visible throughout the animation. */

//==============================================================================



}//Clock class



/*
draw a family of 20 bezier curves, sharing starting
and ending points and with a maximum distance of 20 pixels
between adjacent curves.
*/

/*
  for(int i = 0; i < 20; i++){
    Bezier2d curve = new Bezier2d();
    curve.add(new Point2d(150, 150));
    curve.add(new Point2d(200 + (20 * i), 200));
    curve.add(new Point2d(200 + (20 * i), 250));
    curve.add(new Point2d(150, 300));
    shape.add(curve);
  }
*/

/* draw a square lattice of touching circles.

  for (int i = 0; i < 640; i = i + 40){
    for (int j = 0; j < 480; j = j + 40){
      shape.add(new BresenhamCircle(new Point2d(i, j), 20));
    }
  }
*/

	//Transformation2d trans1 = new Transformation2d();
	//trans1.rotate(100,100);

/*
	Transformation2d translation1 = new Transformation2d();
	Transformation2d translation2 = new Transformation2d();
	Transformation2d rotation = new Transformation2d();

	translation1.translate(-150,-225);
	rotation.rotate(-(double)(3.14159262/20)); // PI/2
	translation2.translate(150,225);

	myTrans.transform(translation1);
	myTrans.transform(rotation);
 	myTrans.transform(translation2);
*/

