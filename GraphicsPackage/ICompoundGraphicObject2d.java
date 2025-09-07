package GraphicsPackage;

import java.util.*;
import java.awt.*;

interface ICompoundGraphicObject2d extends IGraphicObject2d{

	int numberOfParts = 0;

	Vector parts = new Vector();

	public void add(GraphicObject2d o);

}
