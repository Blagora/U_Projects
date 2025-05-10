package sistemanotas.InterefacesGraficas.Admin;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.SQLException;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import sistemanotas.ConexionBD.ConexionDB;
import java.sql.*;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

public class ValidarEstudianteUI extends JFrame{
    private JTextField usernameField;
    private JButton validateButton;
    private JLabel resultLabel;

    // Constructor para configurar el JFrame
    public ValidarEstudianteUI() {
         setTitle("Validación de Estudiante");
        setSize(300, 150);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        // Crear el panel con FlowLayout (centrado)
        JPanel panel = new JPanel();
        usernameField = new JTextField(15);
        validateButton = new JButton("Validar Usuario");
        resultLabel = new JLabel("", SwingConstants.CENTER);

        // Agregar componentes al panel
        panel.add(new JLabel("Usuario:"));
        panel.add(usernameField);
        panel.add(validateButton);
        panel.add(resultLabel);

        // Añadir el panel al JFrame
        add(panel);

        // Agregar un evento al botón de validar
        validateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                validateUser();
            }
        });
    }

    // Método para validar el usuario en la base de datos
    private void validateUser() {
        String codigo = usernameField.getText();
        String searchEstudianteQuery = "SELECT * FROM estudiantes WHERE codigo = ?";
        try (Connection conn = ConexionDB.getConnection()) {
            PreparedStatement stmtSearchUsuario = conn.prepareStatement(searchEstudianteQuery);
            stmtSearchUsuario.setString(1, codigo);
            ResultSet rs = stmtSearchUsuario.executeQuery();
            if (rs.next()) {
                new GestionEstudianteUI(codigo).setVisible(true);
            }
            else{
                JOptionPane.showMessageDialog(this, "Código inválido");
            }
        }catch (SQLException e) {
            e.printStackTrace();
        }
    }
    
}
