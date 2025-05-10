package sistemanotas.InterefacesGraficas.Admin;

import javax.swing.*;
import sistemanotas.Estructura.AdminService;
import sistemanotas.Estructura.Estudiante;

public class EditarEstudianteUI extends JFrame {
    
    private JTextField codigoField;
    private JTextField nombreField;
    private JTextField apellidoField;
    private JTextField correoField;
    private JButton guardarButton;
    private JButton cancelarButton;
    private AdminService adminService;

    public EditarEstudianteUI(String codigoEstudiante) {
        adminService = new AdminService();
        
        setTitle("Editar Estudiante");
        setSize(400, 400);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        // Crear componentes
        codigoField = new JTextField(20);
        nombreField = new JTextField(20);
        apellidoField = new JTextField(20);
        correoField = new JTextField(20);
        guardarButton = new JButton("Guardar Cambios");
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
        codigoField.setEditable(false); // Código no editable

        JLabel nombreLabel = new JLabel("Nombre:");
        nombreLabel.setBounds(30, 80, 80, 25);
        panel.add(nombreLabel);
        nombreField.setBounds(120, 80, 200, 25);
        panel.add(nombreField);

        JLabel apellidoLabel = new JLabel("Apellido:");
        apellidoLabel.setBounds(30, 130, 80, 25);
        panel.add(apellidoLabel);
        apellidoField.setBounds(120, 130, 200, 25);
        panel.add(apellidoField);

        JLabel correoLabel = new JLabel("Correo:");
        correoLabel.setBounds(30, 180, 80, 25);
        panel.add(correoLabel);
        correoField.setBounds(120, 180, 200, 25);
        panel.add(correoField);

        guardarButton.setBounds(30, 230, 150, 30);
        cancelarButton.setBounds(200, 230, 150, 30);

        panel.add(guardarButton);
        panel.add(cancelarButton);

        add(panel);

        // Cargar datos del estudiante automáticamente al inicio
        cargarEstudiante(codigoEstudiante);

        // Agregar acción al botón guardar
        guardarButton.addActionListener(e -> guardarCambios());

        // Agregar acción al botón cancelar
        cancelarButton.addActionListener(e -> dispose()); // Cierra la ventana
    }

    private void cargarEstudiante(String codigoEstudiante) {
        Estudiante estudiante = adminService.obtenerEstudiante(codigoEstudiante);

        if (estudiante != null) {
            codigoField.setText(estudiante.getCodigo());
            nombreField.setText(estudiante.getNombre());
            apellidoField.setText(estudiante.getApellido());
            correoField.setText(estudiante.getCorreo());
        } else {
            JOptionPane.showMessageDialog(this, "Estudiante no encontrado.", "Error", JOptionPane.ERROR_MESSAGE);
            dispose(); // Cierra la ventana si no se encuentra el estudiante
        }
    }

    private void guardarCambios() {
        String codigo = codigoField.getText().trim();
        String nombre = nombreField.getText().trim();
        String apellido = apellidoField.getText().trim();
        String correo = correoField.getText().trim();

        // Validar campos
        if (nombre.isEmpty() || apellido.isEmpty() || correo.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Todos los campos son obligatorios.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        // Llamar al método para actualizar el estudiante
        boolean actualizado = adminService.actualizarEstudiante(codigo, nombre, apellido, correo);

        if (actualizado) {
            JOptionPane.showMessageDialog(this, "Estudiante actualizado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
            dispose(); // Cerrar la ventana después de actualizar
        } else {
            JOptionPane.showMessageDialog(this, "Error al actualizar estudiante.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}

