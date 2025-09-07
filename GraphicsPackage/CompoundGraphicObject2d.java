package GraphicsPackage;

/**
* <P> 
* @author Ryan L Cook
*/

import java.util.*;
import java.awt.*;

public class CompoundGraphicObject2d extends GraphicObject2d implements ICompoundGraphicObject2d{

	protected Point2d		localOrigin =			new Point2d(0,0);
	protected Vector		parts =					  new Vector();
	protected int			  numberOfParts=		0;

  //Auxiliary instances for type determination in isCGO2d() and isGO2d().
	private static		CompoundGraphicObject2d sCGO2d = new CompoundGraphicObject2d();
  private static    GraphicObject2d sGO2d = new GraphicObject2d();

	private static final	String classCGO2d = "CompoundGraphicObject2d";
	private static final	String classGO2d =  "GraphicObject2d";

  /**
  A shape has many 'parts'. Each part can, itself, be a shape, or any object that
  implements IGraphicObject2d. This can be achieved using the abstract base class
  CompoundGraphicObject2d.
  Any ICompound... implementation can include multiple sub-objects.
  The Shape2d is designed to accept any object that implements the interface IGraphicObject2D.
  */


  

	public CompoundGraphicObject2d(){
		localOrigin = new Point2d(0, 0);
		}


    

	public CompoundGraphicObject2d(Point2d point){
		localOrigin = point;
		}


    

	public CompoundGraphicObject2d CompoundGraphicObject2d(CompoundGraphicObject2d cgo2d){
		//recycle
		return cgo2d;
		}



    
	protected GraphicObjectIdentifier getGraphicObject(Object o) throws ForeignObjectException{
		/**
    Return a reference to an object of the general type supported by the interface,
    and targetting the specified Object, so that we can obtain access to its methods.

    --notes:
      GoF Visitor pattern may be used if the mechanism, as used here, becomes too
      restrictive.
      GoF Flyweight may be used if the object hierarchy turns out to be
      too expensive in memory.
      Support Java container/component framework.
    */

    /*
      Distinction of Compound object, below, because the generic IGraphicObject
      is not implemented.
    */

    if(isGO2d(o))
			return new GraphicObjectIdentifier("GraphicObject2d", (GraphicObject2d)o);
		else if (isCGO2d(o))
			return new GraphicObjectIdentifier("CompoundGraphicObject2d", (CompoundGraphicObject2d)o);
		else
			throw new ForeignObjectException();
	}



  
  protected boolean isGO2d(Object o){
    return(sGO2d.getClass().isAssignableFrom(o.getClass()));
  }



  
  protected boolean isCGO2d(Object o){
    return(sCGO2d.getClass().isAssignableFrom(o.getClass()));
  }


  

  public void clear(){
    numberOfParts = 0;
    parts.clear();
    };


  

	public void add(GraphicObject2d obj){
    numberOfParts++;
		parts.add(obj);
		};



    
	public void draw(Graphics g){

		for (int i=0; i < numberOfParts; i = i+1) {

			Object o = parts.get(i);
      GraphicObject2d go2d = new GraphicObject2d();
			try{
				GraphicObjectIdentifier id = getGraphicObject(o);
        String on = id.getObjectName();
        if (on == classCGO2d)
          go2d = (CompoundGraphicObject2d)id.getObject();
        if (on == classGO2d)
          go2d = (GraphicObject2d)id.getObject();
        // now we know that we can draw() the object
				go2d.draw(g);
      }
			catch(ForeignObjectException e){
				/* This base class skips objects that it cannot recognize. Therefore, this
        only deals with subclasses of the GraphicObject base. */
			}
		}
	}




	public void erase(Graphics g){

		for (int i=0; i < numberOfParts; i = i+1) {

			Object o = parts.get(i);
      GraphicObject2d go2d = new GraphicObject2d();
			try{
				GraphicObjectIdentifier id = getGraphicObject(o);
        String on = id.getObjectName();
        if (on == classCGO2d)
          go2d = (CompoundGraphicObject2d)id.getObject();
        if (on == classGO2d)
          go2d = (GraphicObject2d)id.getObject();
        // now erase the object
				go2d.erase(g);
      }
			catch(ForeignObjectException e){
				/* This base class skips objects that it cannot recognize. Therefore, this
        only deals with subclasses of the GraphicObject base. */
			}
		}
	}

  /** Pass each transformation object on to the component objects of this container.
  */

  public void transform(Transformation2d trans){

		for (int i=0; i < numberOfParts; i = i+1) {

			Object o = parts.get(i);
      GraphicObject2d go2d = new GraphicObject2d();
			try{
				GraphicObjectIdentifier id = getGraphicObject(o);
        String on = id.getObjectName();
        if (on == classCGO2d)
          go2d = (CompoundGraphicObject2d)id.getObject();
        if (on == classGO2d)
          go2d = (GraphicObject2d)id.getObject();
        // now transform the object
				go2d.transform(trans);
      }
			catch(ForeignObjectException e){
				/* This base class skips objects that it cannot recognize. Therefore, this
        only deals with subclasses of the GraphicObject base. This exception must
        be handled by the user of the container. */
			}
		}
    localOrigin.transform(trans);
	}

}//end class Shape2d


