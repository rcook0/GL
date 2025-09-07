package AnalogClock;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

/**
 * Applet
 * <P>
 * @author 
 */
public class AnalogClockApplet extends JApplet {
  boolean isStandalone = false;
  int appletStartingHour;
  int appletStartingMinute;
  int appletStartingSecond;

  /**
   * Constructs a new instance.
   */
  /**
   * getParameter
   * @param key
   * @param def
   * @return java.lang.String
   */
  public String getParameter(String key, String def) {
    if (isStandalone) {
      return System.getProperty(key, def);
    }
    if (getParameter(key) != null) {
      return getParameter(key);
    }
    return def;
  }

  public AnalogClockApplet() {
  }

  /**
   * Initializes the state of this instance.
   */
  /**
   * init
   */
  public void init() {
    try  {
      appletStartingHour = Integer.valueOf(this.getParameter("Hour", "0")).intValue();
    }
    catch (NumberFormatException e) {
      e.printStackTrace();
    }
    try  {
      appletStartingMinute = Integer.valueOf(this.getParameter("Minute", "0")).intValue();
    }
    catch (NumberFormatException e) {
      e.printStackTrace();
    }
    try  {
      appletStartingSecond = Integer.valueOf(this.getParameter("Second", "0")).intValue();
    }
    catch (NumberFormatException e) {
      e.printStackTrace();
    }
    try  {
      jbInit();
    }
    catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void jbInit() throws Exception {
    this.setSize(new Dimension(300, 300));
  }

  /**
   * start
   */
  public void start() {
  }

  /**
   * stop
   */
  public void stop() {
  }

  /**
   * destroy
   */
  public void destroy() {
  }

  /**
   * getAppletInfo
   * @return java.lang.String
   */
  public String getAppletInfo() {
    return "Hello and Welcome, This is your Analog Clock applet.";
  }

  /**
   * getParameterInfo
   * @return java.lang.String[][]
   */
  public String[][] getParameterInfo() {
    String[][] pinfo = 
    {
      {"Hour", "int", "Hour of the current time."},
      {"Minute", "int", "Minute of the current time"},
      {"Second", "int", "Second of the current time."},
    };
    return pinfo;
  }

  /**
   * main
   * @param args
   */
  public static void main(String[] args) {
    AnalogClockApplet applet = new AnalogClockApplet();
    applet.isStandalone = true; // panel
    JFrame frame = new JFrame();
    frame.setTitle("Applet Frame");

    Clock clock = new Clock();
    String[] myArgs = new String[]{};
    clock.main(myArgs);
    
    //frame.getContentPane().add(clock, BorderLayout.CENTER);
    applet.init();
    applet.start();
    frame.setSize(300, 300);
    Dimension d = Toolkit.getDefaultToolkit().getScreenSize();
    frame.setLocation((d.width - frame.getSize().width) / 2, (d.height - frame.getSize().height) / 2);
    frame.setVisible(true);
    frame.addWindowListener(
      new WindowAdapter() { 
        public void windowClosing(WindowEvent e) { 
          System.exit(0); 
          } 
      }
    );//addWindowListener
  }

  static {
    try {
      UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
    }
    catch(Exception e) {
      e.printStackTrace();
    }
  }
}
