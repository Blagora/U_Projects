package sistemanotas.InterefacesGraficas;

import sistemanotas.InterefacesGraficas.Admin.AdminUI;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.*;
import sistemanotas.ConexionBD.ConexionDB;
import sistemanotas.Estructura.Docente;
import sistemanotas.Estructura.Estudiante;
import sistemanotas.InterefacesGraficas.Estudiante.EstudianteUI;
import sistemanotas.InterefacesGraficas.docente.DocenteUI;

public class Login extends JFrame {
    private JTextField usuarioField;
    private JPasswordField contrasenaField;

    public Login() {
        setTitle("Login - Sistema de Notas");
        setSize(300, 150);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        usuarioField = new JTextField(15);
        contrasenaField = new JPasswordField(15);
        JButton loginButton = new JButton("Ingresar");

        panel.add(new JLabel("Usuario:"));
        panel.add(usuarioField);
        panel.add(new JLabel("Contraseña:"));
        panel.add(contrasenaField);
        panel.add(loginButton);

        loginButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                autenticarUsuario();
            }
        });

        add(panel);
    }

    private void autenticarUsuario() {
        String usuario = usuarioField.getText();
        String contrasena = new String(contrasenaField.getPassword());

        try (Connection conn = ConexionDB.getConnection()) {
            String query = "SELECT id, usuario, contrasena, rol_id FROM usuarios WHERE usuario = ? AND contrasena = ?";
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setString(1, usuario);
            stmt.setString(2, contrasena);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                int userId = rs.getInt("id");
                int rolId = rs.getInt("rol_id");

                switch (rolId) {
                    case 1: // Admin
                        JOptionPane.showMessageDialog(this, "Ingreso como Admin");
                        new AdminUI().setVisible(true);
                        break;

                    case 2: // Docente
                        Docente docente = obtenerDocente(conn, userId);
                        if (docente != null) {
                            JOptionPane.showMessageDialog(this, "Ingreso como Docente");
                            new DocenteUI(contrasena).setVisible(true);
                        } else {
                            JOptionPane.showMessageDialog(this, "No se encontraron datos del docente.");
                        }
                        break;

                    case 3: // Estudiante
                        Estudiante estudiante = obtenerEstudiante(conn, userId);
                        if (estudiante != null) {
                            JOptionPane.showMessageDialog(this, "Ingreso como Estudiante");
                            new EstudianteUI(contrasena).setVisible(true); // Pasar el objeto Estudiante
                        } else {
                            JOptionPane.showMessageDialog(this, "No se encontraron datos del estudiante.");
                        }
                        break;

                    default:
                        JOptionPane.showMessageDialog(this, "Rol desconocido");
                        break;
                }
                this.dispose();
            } else {
                JOptionPane.showMessageDialog(this, "Credenciales incorrectas");
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al conectar con la base de datos.", "Error", JOptionPane.ERROR_MESSAGE);
        }

    }
    
    private Docente obtenerDocente(Connection conn, int userId) {
        String query = "SELECT d.codigo, d.nombre, d.apellido, d.correo, d.area " +
                       "FROM docentes d " +
                       "JOIN usuarios u ON d.usuario_id = u.id " +
                       "WHERE u.id = ?";
        try (PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setInt(1, userId);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                String codigo = rs.getString("codigo");
                String nombre = rs.getString("nombre");
                String apellido = rs.getString("apellido");
                String correo = rs.getString("correo");
                String area = rs.getString("area");

                return new Docente(userId, null, null, 2, codigo, nombre, apellido, correo, area);
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error al obtener datos del docente.", "Error", JOptionPane.ERROR_MESSAGE);
    }
    return null;
    
    
    }
    private Estudiante obtenerEstudiante(Connection conn, int userId) {
        String query = "SELECT e.codigo, e.nombre, e.apellido, e.correo " +
                       "FROM estudiantes e " +
                       "JOIN usuarios u ON e.usuario_id = u.id " +
                       "WHERE u.id = ?";
        try (PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setInt(1, userId);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                String codigo = rs.getString("codigo");
                String nombre = rs.getString("nombre");
                String apellido = rs.getString("apellido");
                String correo = rs.getString("correo");

                return new Estudiante(userId, null, null, 3, codigo, nombre, apellido, correo);
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error al obtener datos del estudiante.", "Error", JOptionPane.ERROR_MESSAGE);
        }
        return null;
    }



}
