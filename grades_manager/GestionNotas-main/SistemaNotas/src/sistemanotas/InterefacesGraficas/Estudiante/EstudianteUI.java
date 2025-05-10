package sistemanotas.InterefacesGraficas.Estudiante;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import sistemanotas.ConexionBD.ConexionDB;
import sistemanotas.Estructura.Estudiante;
import sistemanotas.InterefacesGraficas.Login;

public class EstudianteUI extends JFrame {
    private final Estudiante estudiante;

    public EstudianteUI(String codigoEstudiante) {
        // Obtención de los datos del estudiante utilizando su código
        this.estudiante = obtenerEstudiante(codigoEstudiante);
        if (estudiante == null) {
            JOptionPane.showMessageDialog(this, "Estudiante no encontrado.");
            return;
        }

        setTitle("Panel de Estudiante - " + estudiante.getNombre());
        setSize(400, 200);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        JButton verCursosButton = new JButton("Ver Cursos");
        JButton verNotasButton = new JButton("Ver Notas");
        JButton salirButton = new JButton("Salir");

        JPanel botonesPanel = new JPanel();
        botonesPanel.setLayout(new FlowLayout());
        botonesPanel.add(verCursosButton);
        botonesPanel.add(verNotasButton);
        panel.add(salirButton);

        panel.add(botonesPanel, BorderLayout.SOUTH);
        add(panel);

        verCursosButton.addActionListener((ActionEvent e) -> {
            List<String> cursos = obtenerCursos(estudiante.getId());
            if (cursos.isEmpty()) {
                JOptionPane.showMessageDialog(this, "No estás inscrito en ningún curso.");
            } else {
                StringBuilder mensaje = new StringBuilder("Cursos inscritos:\n");
                for (String curso : cursos) {
                    mensaje.append("- ").append(curso).append("\n");
                }
                JOptionPane.showMessageDialog(this, mensaje.toString());
            }
        });

        verNotasButton.addActionListener((ActionEvent e) -> {
            List<String> notas = obtenerNotas(estudiante.getId());
            if (notas.isEmpty()) {
                JOptionPane.showMessageDialog(this, "No tienes notas registradas.");
            } else {
                StringBuilder mensaje = new StringBuilder("Notas:\n");
                for (String nota : notas) {
                    mensaje.append(nota).append("\n");
                }
                JOptionPane.showMessageDialog(this, mensaje.toString());
            }
        });
        
        salirButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                dispose();
                new Login().setVisible(true);
            }
        });
    }

    private Estudiante obtenerEstudiante(String codigoEstudiante) {
        Estudiante estudiante = null;
        String query = """
                SELECT e.id, e.codigo, e.nombre, e.apellido, e.correo, u.usuario, u.contrasena, u.rol_id
                FROM estudiantes e
                JOIN usuarios u ON e.usuario_id = u.id
                WHERE e.codigo = ?
                """;

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setString(1, codigoEstudiante);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                int id = rs.getInt("id");
                String nombre = rs.getString("nombre");
                String apellido = rs.getString("apellido");
                String correo = rs.getString("correo");
                String usuario = rs.getString("usuario");
                String contrasena = rs.getString("contrasena");
                int rolId = rs.getInt("rol_id");

                estudiante = new Estudiante(id, usuario, contrasena, rolId, codigoEstudiante, nombre, apellido, correo);
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al obtener los datos del estudiante: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
        return estudiante;
    }

    private List<String> obtenerCursos(int estudianteId) {
        List<String> cursos = new ArrayList<>();
        String query = """
                SELECT c.nombre
                FROM cursos c
                JOIN estudiantes_cursos ec ON c.id = ec.curso_id
                WHERE ec.estudiante_id = ?
                """;

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setInt(1, estudianteId);
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                String nombreCurso = rs.getString("nombre");
                cursos.add(nombreCurso);
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al obtener los cursos: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
        return cursos;
    }

    private List<String> obtenerNotas(int estudianteId) {
        List<String> notas = new ArrayList<>();
        String query = """
                SELECT c.nombre AS curso, g.nombre AS grupo, n.nombre_tarea, n.nota
                FROM notas_tareas n
                JOIN grupos_notas g ON n.grupo_id = g.id
                JOIN cortes co ON g.corte_id = co.id
                JOIN cursos c ON co.curso_id = c.id
                WHERE n.estudiante_id = ?
                """;

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setInt(1, estudianteId);
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                String curso = rs.getString("curso");
                String grupo = rs.getString("grupo");
                String tarea = rs.getString("nombre_tarea");
                int nota = rs.getInt("nota");

                notas.add(String.format("Curso: %s | Grupo: %s | Tarea: %s | Nota: %d", curso, grupo, tarea, nota));
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al obtener las notas: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
        return notas;
    }
}
