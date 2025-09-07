package GraphicsPackage;

import java.awt.*;

interface IGraphicObject{

/** Low-level terminal interface for imparting graphics capabilities to a class.*/

	public void draw(Graphics g);

	public void erase(Graphics g);
}