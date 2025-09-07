package View3dTest;
// Copyright (c) 2001

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import GraphicsPackage.*;

/**
 * A Swing-based dialog class.
 * <P>
 * @author Ryan Lovbjerg Cook.
 */
public class EditViewParamsDlg extends JDialog {
  //View3dTest parentFrame = new View3dTest();
  BorderLayout borderLayout1 = new BorderLayout();
  JPanel mainPanel = new JPanel();
  JPanel northPanel = new JPanel();
  JPanel southPanel = new JPanel();
  JRadioButton rbPerspective = new JRadioButton();
  JRadioButton rbParallel = new JRadioButton();
  JLabel vrp = new JLabel();
  JTextField VRPX = new JTextField();
  JTextField VRPY = new JTextField();
  JTextField VRPZ = new JTextField();
  JPanel centerPanel = new JPanel();
  JLabel vpn = new JLabel();
  JTextField VPNX = new JTextField();
  JTextField VPNY = new JTextField();
  JTextField VPNZ = new JTextField();
  JLabel vup = new JLabel();
  JTextField VUPY = new JTextField();
  JTextField VUPX = new JTextField();
  JTextField VUPZ = new JTextField();
  JPanel vrpPanel = new JPanel();
  JPanel vupPanel = new JPanel();
  JPanel vpnPanel = new JPanel();
  JPanel vrcPanel = new JPanel();
  JLabel prp = new JLabel();
  JTextField PRPY = new JTextField();
  JTextField PRPX = new JTextField();
  JTextField PRPZ = new JTextField();
  JPanel prpPanel = new JPanel();
  JLabel window = new JLabel();
  JTextField umin = new JTextField();
  JTextField umax = new JTextField();
  JTextField vmin = new JTextField();
  JTextField vmax = new JTextField();
  JLabel w1 = new JLabel();
  JLabel w2 = new JLabel();
  JLabel w3 = new JLabel();
  JLabel w4 = new JLabel();
  JButton bOK = new JButton();
  JButton bCANCEL = new JButton();
  JPanel jPanel1 = new JPanel();

  View3dTest parentFrm;
  View3dParameters v3dp;

  /**
   * 
   * @param parent
   * @param title
   * @param modal
   */
  public EditViewParamsDlg(View3dTest parent, String title, boolean modal) {
    super(parent, title, modal);
    jbSetup();
    parentFrm = parent;
  }

  public EditViewParamsDlg(){
    //super(null, "EditViewParamsDlg ...", false);
    //jbSetup();
  }

  private void jbSetup() {
    try  {
      jbInit();
      pack();
    }
    catch (Exception e) {
      e.printStackTrace();
    }
  }

  /**
   * Initializes the state of this instance.
   */
  private void jbInit() throws Exception {
    mainPanel.setLayout(borderLayout1);
    mainPanel.setPreferredSize(new Dimension(400, 250));
    mainPanel.setBackground(Color.lightGray);
    mainPanel.setMinimumSize(new Dimension(340, 110));
    northPanel.setBackground(new Color(247, 238, 230));
    southPanel.setBackground(SystemColor.scrollbar);
    rbPerspective.setSelected(true);
    rbPerspective.setBorderPainted(true);
    rbPerspective.setText("rbPerspective");
    rbPerspective.setLabel("Perspective");
    rbPerspective.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(ActionEvent e) {
        if (rbPerspective.isSelected())
          rbParallel.setSelected(false);
        else
          rbParallel.setSelected(true);
      }
    });
    rbParallel.setBorderPainted(true);
    rbParallel.setText("rbParallel");
    rbParallel.setLabel("Parallel");
    rbParallel.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(ActionEvent e) {
        if (rbParallel.isSelected())
          rbPerspective.setSelected(false);
        else
          rbPerspective.setSelected(true);
      }
    });
    vrp.setText("VRP");
    VRPX.setText("0");
    VRPX.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        VRPX_actionPerformed(e);
      }
    });
    VRPY.setPreferredSize(new Dimension(30, 20));
    VRPY.setHorizontalAlignment(JTextField.RIGHT);
    VRPY.setText("0");
    VRPY.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        VRPY_actionPerformed(e);
      }
    });
    VRPZ.setPreferredSize(new Dimension(30, 20));
    VRPZ.setHorizontalAlignment(JTextField.RIGHT);
    VRPZ.setText("0");
    VRPZ.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        jTextField3_actionPerformed(e);
      }
    });
    centerPanel.setBackground(Color.gray);
    vpn.setText("VPN");
    vup.setText("VUP");
    VUPY.setPreferredSize(new Dimension(30, 20));
    VUPY.setHorizontalAlignment(JTextField.RIGHT);
    VUPY.setText("0");
    VUPY.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        VUPY_actionPerformed(e);
      }
    });
    VUPX.setText("0");
    VUPX.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        VUPX_actionPerformed(e);
      }
    });
    VUPZ.setText("0");
    VUPZ.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        VUPZ_actionPerformed(e);
      }
    });
    vrpPanel.setPreferredSize(new Dimension(375, 30));
    vupPanel.setPreferredSize(new Dimension(375, 30));
    vpnPanel.setPreferredSize(new Dimension(375, 30));
    vrcPanel.setPreferredSize(new Dimension(375, 30));
    vrcPanel.setMinimumSize(new Dimension(65, 31));
    prp.setText("PRP");
    PRPY.setHorizontalAlignment(JTextField.RIGHT);
    PRPY.setPreferredSize(new Dimension(30, 20));
    PRPY.setText("0");
    PRPY.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        PRPY_actionPerformed(e);
      }
    });
    PRPX.setHorizontalAlignment(JTextField.RIGHT);
    PRPX.setText("0");
    PRPX.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        PRPX_actionPerformed(e);
      }
    });
    PRPZ.setHorizontalAlignment(JTextField.RIGHT);
    PRPZ.setText("0");
    PRPZ.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        PRPZ_actionPerformed(e);
      }
    });
    prpPanel.setPreferredSize(new Dimension(375, 30));
    window.setText("Window (VRC) : ");
    umin.setPreferredSize(new Dimension(30, 20));
    umin.setHorizontalAlignment(JTextField.RIGHT);
    umin.setText("0");
    umin.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        umin_actionPerformed(e);
      }
    });
    umax.setPreferredSize(new Dimension(30, 20));
    umax.setHorizontalAlignment(JTextField.RIGHT);
    umax.setText("0");
    umax.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        umax_actionPerformed(e);
      }
    });
    vmin.setPreferredSize(new Dimension(30, 20));
    vmin.setHorizontalAlignment(JTextField.RIGHT);
    vmin.setText("0");
    vmin.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        vmin_actionPerformed(e);
      }
    });
    vmax.setPreferredSize(new Dimension(30, 20));
    vmax.setHorizontalAlignment(JTextField.RIGHT);
    vmax.setText("0");
    vmax.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        vmax_actionPerformed(e);
      }
    });
    w1.setText("umin");
    w2.setText("umax");
    w3.setText("vmin");
    w4.setText("vmax");
    bOK.setText("OK");
    bOK.addActionListener(new java.awt.event.ActionListener() {
      /* Response to the user pressing the OK button :
        1. Load the newly defined viewing parameters.
        2. Calculate viewing op, based on these parameters, for the object.
        3. Display new perspective projection of the object.
      */
      public void actionPerformed(ActionEvent e) {
        setVisible(false);
        /*v3dp = new View3dParameters();
        if(rbPerspective.isSelected()) v3dp.projectionType(1);
        if(rbParallel.isSelected()) v3dp.projectionType(0);
        v3dp.vrp(new Point3d(
          Double.parseDouble(VRPX.getText()),
          Double.parseDouble(VRPY.getText()),
          Double.parseDouble(VRPZ.getText())
          ) );
        v3dp.prp(new Point3d(
          Double.parseDouble(PRPX.getText()),
          Double.parseDouble(PRPY.getText()),
          Double.parseDouble(PRPZ.getText())
          ) );
        v3dp.vup(new Vector4d(
          Double.parseDouble(VUPX.getText()),
          Double.parseDouble(VUPY.getText()),
          Double.parseDouble(VUPZ.getText())
          ) );
        v3dp.vpn(new Vector4d(
          Double.parseDouble(VPNX.getText()),
          Double.parseDouble(VPNY.getText()),
          Double.parseDouble(VPNZ.getText())
          ) );
        v3dp.VRC_umin(Double.parseDouble(umin.getText()));
        v3dp.VRC_umax(Double.parseDouble(umax.getText()));
        v3dp.VRC_vmin(Double.parseDouble(vmin.getText()));
        v3dp.VRC_vmax(Double.parseDouble(vmax.getText()));

        System.out.println("v3dp catalogue : " + v3dp.catalogue());
*/
        parentFrm.processNewView();
        //dispose();
      }
    });
    bCANCEL.setText("CANCEL");
    bCANCEL.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(ActionEvent e) {
        parentFrm.processNewView();
        setVisible(false);
        dispose();
      }
    });
    PRPZ.setPreferredSize(new Dimension(30, 20));
    PRPX.setPreferredSize(new Dimension(30, 20));
    VUPZ.setPreferredSize(new Dimension(30, 20));
    VUPZ.setHorizontalAlignment(JTextField.RIGHT);
    VUPX.setPreferredSize(new Dimension(30, 20));
    VUPX.setHorizontalAlignment(JTextField.RIGHT);
    VPNX.setPreferredSize(new Dimension(30, 20));
    VPNX.setHorizontalAlignment(JTextField.RIGHT);
    VPNX.setText("0");
    VPNX.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        VPNX_actionPerformed(e);
      }
    });
    VPNY.setText("0");
    VPNY.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        VPNY_actionPerformed(e);
      }
    });
    VPNZ.setText("0");
    VPNZ.addActionListener(new java.awt.event.ActionListener() {

      public void actionPerformed(ActionEvent e) {
        VPNZ_actionPerformed(e);
      }
    });
    VPNZ.setPreferredSize(new Dimension(30, 20));
    VPNZ.setHorizontalAlignment(JTextField.RIGHT);
    VPNY.setPreferredSize(new Dimension(30, 20));
    VPNY.setHorizontalAlignment(JTextField.RIGHT);
    VRPX.setPreferredSize(new Dimension(30, 20));
    VRPX.setHorizontalAlignment(JTextField.RIGHT);
    getContentPane().add(mainPanel);
    mainPanel.add(southPanel, BorderLayout.SOUTH);
    southPanel.add(bOK, null);
    southPanel.add(bCANCEL, null);
    mainPanel.add(northPanel, BorderLayout.NORTH);
    northPanel.add(jPanel1, null);
    jPanel1.add(rbPerspective, null);
    jPanel1.add(rbParallel, null);
    mainPanel.add(centerPanel, BorderLayout.CENTER);
    centerPanel.add(vupPanel, null);
    vupPanel.add(vup, null);
    vupPanel.add(VUPX, null);
    vupPanel.add(VUPY, null);
    vupPanel.add(VUPZ, null);
    centerPanel.add(vrpPanel, null);
    vrpPanel.add(vrp, null);
    vrpPanel.add(VRPX, null);
    vrpPanel.add(VRPY, null);
    vrpPanel.add(VRPZ, null);
    centerPanel.add(vpnPanel, null);
    vpnPanel.add(vpn, null);
    vpnPanel.add(VPNX, null);
    vpnPanel.add(VPNY, null);
    vpnPanel.add(VPNZ, null);
    centerPanel.add(vrcPanel, null);
    vrcPanel.add(window, null);
    vrcPanel.add(w1, null);
    vrcPanel.add(umin, null);
    vrcPanel.add(w2, null);
    vrcPanel.add(umax, null);
    vrcPanel.add(w3, null);
    vrcPanel.add(vmin, null);
    vrcPanel.add(w4, null);
    vrcPanel.add(vmax, null);
    centerPanel.add(prpPanel, null);
    prpPanel.add(prp, null);
    prpPanel.add(PRPX, null);
    prpPanel.add(PRPY, null);
    prpPanel.add(PRPZ, null);
  }

  void jTextField3_actionPerformed(ActionEvent e) {

  }

  public static void main(String args[]) {
    EditViewParamsDlg vp = new EditViewParamsDlg();
    vp.setVisible(true);
  }

  void VUPX_actionPerformed(ActionEvent e) {
    
  }

  void VUPY_actionPerformed(ActionEvent e) {
    
  }

  void VUPZ_actionPerformed(ActionEvent e) {
    
  }

  void VRPX_actionPerformed(ActionEvent e) {
    
  }

  void VRPY_actionPerformed(ActionEvent e) {
    
  }

  void VPNX_actionPerformed(ActionEvent e) {
    
  }

  void VPNY_actionPerformed(ActionEvent e) {
    
  }

  void VPNZ_actionPerformed(ActionEvent e) {
    
  }

  void umin_actionPerformed(ActionEvent e) {
    
  }

  void umax_actionPerformed(ActionEvent e) {
    
  }

  void vmin_actionPerformed(ActionEvent e) {
    
  }

  void vmax_actionPerformed(ActionEvent e) {
    
  }

  void PRPX_actionPerformed(ActionEvent e) {
    
  }

  void PRPY_actionPerformed(ActionEvent e) {
    
  }

  void PRPZ_actionPerformed(ActionEvent e) {

  }

}

