package GraphicsPackage;

/**
* <P>
* @author Ryan L Cook
*/

public class GraphicObjectIdentifier{

/** Encapsulator for a Graphic Object. Packages the object with identification
of its type (by a String) and provides access to the object through an instance
variable. Overcomes the problem of identifying the class.
In practice, most such objects are of type GraphicObject2d or
CompoundGraphicObject2d, but are only assumed to be of the basic type,
GraphicObject */

	public String gObjectName;
	public GraphicObject2d /*GraphicObject*/ gObject;

	public GraphicObjectIdentifier(String name, GraphicObject2d /*GraphicObject*/ obj){
		gObjectName = name;
		gObject = obj;
	}

  /** Retrieve the type of the object */
  String getObjectName(){
    return gObjectName;
    }

  /** Retrieve the object. Caller can use getObjectName() to tell whether
  to cast to a Compound or basic GraphicObject2d. */
  GraphicObject2d /*GraphicObject*/ getObject(){
    return gObject;
    }
}