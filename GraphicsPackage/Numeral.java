package GraphicsPackage;

/**
* <P>
* @author Ryan L Cook
*/

import java.awt.*;
import java.util.*;
/**
 * Class to add a numeral of 2 characters at the
 specified position in the graphics context.
 * <P>
 * @author 
 */
public class Numeral extends GraphicObject2d {

  char[] character = {'-', '-'};
  int length = 2;
  int x;
  int y;
  // Set a default font.
  Font font = new Font("Arial", Font.BOLD, 14);

  /**
   * Constructor
   */
  public Numeral(char[] chars, Point2d pos) {
    character = chars;
    x = (int)pos.x();
    y = (int)pos.y();

  }

  public Numeral(char[] chars, int nChars, Point2d pos) {
    character = chars;
    length = nChars;
    x = (int)pos.x();
    y = (int)pos.y();
  }

  public Font getFont() {
    return font;
  }

  public void setFont(Font f) {
    font = f;
  }
  
  public void draw(Graphics g) {
    g.setColor(cDraw);
    paint(g);
  }

  public void erase(Graphics g) {
    g.setColor(cErase);
    paint(g);
  }

  private void paint(Graphics g){
    g.setFont(font);
    g.drawChars(character, 0, length, x, y);
  }
}

 