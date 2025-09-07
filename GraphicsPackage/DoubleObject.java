package GraphicsPackage;

/**
 * The DoubleObject class provides a very simple encapsulation of double.
 * <P>
 * @author Ryan L Cook.
 */
public class DoubleObject extends Object {
  public double value;

  /**
   * Constructor
   */
  public DoubleObject(double newValue) {
    value = newValue;
  }

  public double getValue() {
    return value;
  }

  public void setValue(double newValue) {
    value = newValue;
  }
}

