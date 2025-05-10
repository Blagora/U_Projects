package sistemanotas.InterefacesGraficas.Admin;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import sistemanotas.Estructura.AdminService;

public class CrearCursoUI extends JFrame{
    
    private JTextField codigoField;
    private JTextField nombreField;
    private JButton crearButton;
    private AdminService adminService;
    
    public CrearCursoUI(AdminService adminService) {
        
        this.adminService = adminService;
        setTitle("Crear Curso");
        setSize(400, 200);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        // Crear componentes
        codigoField = new JTextField(20);
        nombreField = new JTextField(20);       
        crearButton = new JButton("Crear Curso");

        JPanel panel = new JPanel();
        panel.setLayout(null);

        // Posicionar componentes en el panel
        JLabel codigoLabel = new JLabel("Código:");
        codigoLabel.setBounds(30, 20, 80, 25);
        panel.add(codigoLabel);
        codigoField.setBounds(120, 20, 100, 25);
        panel.add(codigoField);

        JLabel nombreLabel = new JLabel("Nombre:");
        nombreLabel.setBounds(30, 60, 80, 25);
        panel.add(nombreLabel);
        nombreField.setBounds(120, 60, 100, 25);
        panel.add(nombreField);
        
        crearButton.setBounds(70, 100, 150, 30);
        panel.add(crearButton);
        
        crearButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                crearCurso();
            }
        });

        add(panel);
    }    
    
    private void crearCurso() {
        String codigo = codigoField.getText().trim();
        String nombre = nombreField.getText().trim();

        if (codigo.isEmpty() || nombre.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Por favor, complete todos los campos.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        boolean cursoCreado = adminService.crearCurso(codigo, nombre);
        if (cursoCreado) {
            JOptionPane.showMessageDialog(this, "Curso creado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
            dispose(); // Cierra la ventana tras crear el curso
        } else {
            JOptionPane.showMessageDialog(this, "Error al crear el curso. Intente nuevamente.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
   
