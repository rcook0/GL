package GraphicsPackage;

/**
<P>
@author Ryan L Cook
*/

import javax.swing.*;
import java.awt.image.*;
import java.awt.event.*;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Dimension;

public class Buffer extends JPanel implements Runnable{

	Thread thr = new Thread(this);

/*
  // The buffer is linked to the external Drawing object by setDrawing()
  // i.e. it represents the Drawing2d created by the Clock class.

  // The double-buffer thread does not create the shared drawing itself; rather, it
  // reads a drawing created by another source. 

  // Once created and initialized, the animation loop may be started by calling
  // animateStart(), and stopped by calling animateStop().
*/
	Drawing2d myDrawing;
  
	Image bufferImage;
	Graphics bufferGraphics;
	Dimension d;

  /* When the mouse is clicked, the graphic feedback is incorporated into the next
  available frame of animation after the App finds that a selection has been made. 
  It is the responsibility of the application to define this feedback and perform
  any searches on the drawing. */

  // Record the status of important interactive events.
  boolean click = false; // Mouse is/is not pressed.
  boolean drag = false;  // Mouse is/is not currently being dragged.
  // Record the location of the interactivity.
  Point2d selectionPoint = new Point2d(0.0, 0.0); 
  
	public void setDrawing(Drawing2d externalDrawing) {
		myDrawing = externalDrawing;
		}

  public Point2d getSelectionPoint() {
    click = false;
    return selectionPoint;
  }
    
	public void animateStart(){
		thr.start();
		}

	public void run() {
  
    while(true){
      repaint(); 
      try{
        Thread.sleep(50);
      }
      catch (InterruptedException e) {
        System.out.println("InterruptedException@Buffer.run()");
        e.printStackTrace();
      }
    }
  }

	public void animateStop() {
    System.out.println("Buffer.animateStop");
		thr = null;
		}
	
	public void paintComponent(Graphics g){
    
  try {
		//capture current state to buffer
		d = getSize();	
		bufferImage = this.createImage(d.width,d.height);
		bufferGraphics = bufferImage.getGraphics();

    myDrawing.draw(bufferGraphics);

		//put buffer on screen
		g.drawImage(bufferImage,0,0,null);

		//clear the buffer in preparation for the next frame
    myDrawing.erase(bufferGraphics);
  }
  catch (NullPointerException e) {
  
    // This is thrown by references to a null myDrawing object; it is critical that
    // the setDrawing() be called by the Application to initialize the drawing. 
    // Here, we initialize the
    // Drawing as a new Blank. This paintComponent() method is the final call in an
    // event loop initiated by the AWT Repaint Manager, so an uncaught exception will
    // cause the repaint() loop to collapse, probably crashing the application. The
    // following increases the stability.
    
    myDrawing = new Drawing2d();

    // No further picture updates would occur at this point, because the external copy of
    // the shared Drawing2d is no longer associated with this.
    }
  }

  public Buffer() {
    try  {
      jbInit();
    }
    catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void jbInit() throws Exception {
  
   /* this.addKeyListener(new java.awt.event.KeyAdapter() {

      public void keyPressed(KeyEvent e) {
        this_keyPressed(e);
      }
    });*/  
    this.addMouseMotionListener(new java.awt.event.MouseMotionAdapter() {

      public void mouseDragged(MouseEvent e) {
        this_mouseDragged(e);
      }
    });
    this.addMouseListener(new java.awt.event.MouseAdapter() {

      public void mouseClicked(MouseEvent e) {
        this_mouseClicked(e);
      }

      public void mousePressed(MouseEvent e) {
        this_mousePressed(e);
      }

      public void mouseReleased(MouseEvent e) {
        this_mouseReleased(e);
      }
      
    });
  }

  void this_mouseClicked(MouseEvent e) {
    
  }

  /* App uses this method to acknowledge processing of the selection.*/
  public void click(boolean ck) {
    click = ck;
  }

  /* Check if the currently stored selection point is new (has not yet been read and acknowledged) or false.
  The click instance var avoids reading the point twice. */
  public boolean currentSelectionPointIsNew() {
    return (click == true);
  }

  public boolean dragging() {
    return (drag == true);
  }
  
  void this_mouseDragged(MouseEvent e) {

    drag = true;

    selectionPoint = new Point2d((double)e.getX(), (double)e.getY());
  }
  
  void this_mousePressed(MouseEvent e) {
    //System.out.println("Mouse pressed, Panel AnalogClock.Buffer, " + e.getX() + " " + e.getY());

    if (click == false) {
      selectionPoint = new Point2d((double)e.getX(), (double)e.getY());
    }
    // This is a new event. Don't wait for old ones to be picked up. 
    click = true;
    drag = false;
  }

  void this_mouseReleased(MouseEvent e) {
    //System.out.println("Mouse released, Panel AnalogClock.Buffer, " + e.getX() + " " + e.getY());

    drag = false;
  }


}
