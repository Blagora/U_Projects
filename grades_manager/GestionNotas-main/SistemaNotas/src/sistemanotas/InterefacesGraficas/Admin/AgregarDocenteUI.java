package sistemanotas.InterefacesGraficas.Admin;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import static javax.swing.WindowConstants.DISPOSE_ON_CLOSE;
import sistemanotas.Estructura.AdminService;

public class AgregarDocenteUI extends JFrame {
    
    private JTextField codigoField;
    private JTextField nombreField;
    private JTextField apellidoField;
    private JTextField correoField;
    private JTextField areaField;
    private JButton agregarButton;
    private JButton cancelarButton;
    private AdminService adminService;

    public AgregarDocenteUI() {
        adminService = new AdminService();
        
        setTitle("Agregar Docente");
        setSize(400, 350);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        // Crear componentes
        codigoField = new JTextField(20);
        nombreField = new JTextField(20);
        apellidoField = new JTextField(20);
        correoField = new JTextField(20);
        areaField = new JTextField(20);
        agregarButton = new JButton("Agregar Docente");
        cancelarButton = new JButton("Cancelar");

        // Crear panel
        JPanel panel = new JPanel();
        panel.setLayout(null);

        // Posicionar componentes en el panel
        JLabel codigoLabel = new JLabel("Código:");
        codigoLabel.setBounds(30, 30, 80, 25);
        panel.add(codigoLabel);
        codigoField.setBounds(120, 30, 200, 25);
        panel.add(codigoField);

        JLabel nombreLabel = new JLabel("Nombre:");
        nombreLabel.setBounds(30, 70, 80, 25);
        panel.add(nombreLabel);
        nombreField.setBounds(120, 70, 200, 25);
        panel.add(nombreField);

        JLabel apellidoLabel = new JLabel("Apellido:");
        apellidoLabel.setBounds(30, 110, 80, 25);
        panel.add(apellidoLabel);
        apellidoField.setBounds(120, 110, 200, 25);
        panel.add(apellidoField);

        JLabel correoLabel = new JLabel("Correo:");
        correoLabel.setBounds(30, 150, 80, 25);
        panel.add(correoLabel);
        correoField.setBounds(120, 150, 200, 25);
        panel.add(correoField);
        
        JLabel areaLabel = new JLabel("Area:");
        areaLabel.setBounds(30, 190, 80, 25);
        panel.add(areaLabel);
        areaField.setBounds(120, 190, 200, 25);
        panel.add(areaField);

        agregarButton.setBounds(90, 240, 150, 30);
        panel.add(agregarButton);
        cancelarButton.setBounds(250, 240, 100, 30);
        panel.add(cancelarButton);

        // Agregar acción al botón agregar
        agregarButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                agregarDocente();
            }
        });

        // Agregar acción al botón cancelar
        cancelarButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                dispose(); // Cierra la ventana
            }
        });

        add(panel);
    }

    private void agregarDocente() {
        String codigo = codigoField.getText().trim();
        String nombre = nombreField.getText().trim();
        String apellido = apellidoField.getText().trim();
        String correo = correoField.getText().trim();
        String area = areaField.getText().trim();

        // Validar campos
        if (codigo.isEmpty() || nombre.isEmpty() || apellido.isEmpty() || correo.isEmpty() || area.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Todos los campos son obligatorios.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        // Llamar al método de agregar estudiante
        boolean agregado = adminService.agregarDocente(codigo, nombre, apellido, correo, area);

        if (agregado) {
            JOptionPane.showMessageDialog(this, "Docente agregado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
            dispose(); // Cerrar la ventana después de agregar
        } else {
            JOptionPane.showMessageDialog(this, "Error al agregar docente.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
