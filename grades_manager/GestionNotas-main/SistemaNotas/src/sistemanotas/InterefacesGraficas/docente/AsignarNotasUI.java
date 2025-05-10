package sistemanotas.InterefacesGraficas.docente;

import sistemanotas.ConexionBD.ConexionDB;
import javax.swing.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class AsignarNotasUI extends JFrame {
    private String docenteId;

    public AsignarNotasUI(String docenteId) {
        this.docenteId = docenteId;
        setTitle("Asignar Notas");
        setSize(600, 400);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        // Diseño de la interfaz
        JPanel panel = new JPanel();
        JLabel cursoLabel = new JLabel("Curso:");
        JComboBox<String> cursoComboBox = new JComboBox<>(getCursos()); // Cargar cursos del docente
        JLabel grupoLabel = new JLabel("Grupo:");
        JComboBox<String> grupoComboBox = new JComboBox<>(getGrupos(cursoComboBox.getItemAt(0))); // Cargar grupos
        JLabel tareaLabel = new JLabel("Tarea:");
        JTextField tareaField = new JTextField(20); // Campo para ingresar nombre de la tarea
        JLabel estudianteLabel = new JLabel("Estudiante:");
        JComboBox<String> estudianteComboBox = new JComboBox<>(getEstudiantes(cursoComboBox.getItemAt(0))); // Cargar estudiantes
        JLabel notaLabel = new JLabel("Nota:");
        JTextField notaField = new JTextField(5);
        JButton guardarButton = new JButton("Guardar Nota");

        panel.add(cursoLabel);
        panel.add(cursoComboBox);
        panel.add(grupoLabel);
        panel.add(grupoComboBox);
        panel.add(tareaLabel);
        panel.add(tareaField);
        panel.add(estudianteLabel);
        panel.add(estudianteComboBox);
        panel.add(notaLabel);
        panel.add(notaField);
        panel.add(guardarButton);

        add(panel);

        cursoComboBox.addActionListener(e -> {
            String selectedCurso = (String) cursoComboBox.getSelectedItem();
            grupoComboBox.setModel(new DefaultComboBoxModel<>(getGrupos(selectedCurso)));

            // Guardar la selección actual del estudiante
            String selectedEstudiante = (String) estudianteComboBox.getSelectedItem();
            estudianteComboBox.setModel(new DefaultComboBoxModel<>(getEstudiantes(selectedCurso)));

            // Restaurar la selección del estudiante si sigue disponible
            if (selectedEstudiante != null) {
                estudianteComboBox.setSelectedItem(selectedEstudiante);
            }
        });

        grupoComboBox.addActionListener(e -> {
            String selectedGrupo = (String) grupoComboBox.getSelectedItem();
            // Aquí necesitamos obtener los estudiantes solo del grupo seleccionado
            String selectedCurso = (String) cursoComboBox.getSelectedItem();
            estudianteComboBox.setModel(new DefaultComboBoxModel<>(getEstudiantesPorGrupo(selectedCurso, selectedGrupo)));
        });


        // Evento para guardar la nota
        guardarButton.addActionListener(e -> {
            String curso = (String) cursoComboBox.getSelectedItem();
            String grupo = (String) grupoComboBox.getSelectedItem();
            String tarea = tareaField.getText().trim();
            String estudiante = (String) estudianteComboBox.getSelectedItem();
            String notaStr = notaField.getText().trim();

            if (notaStr.isEmpty() || tarea.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Por favor ingrese la tarea y la nota.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            try {
                int nota = Integer.parseInt(notaStr);
                if (nota < 0 || nota > 50) {
                    JOptionPane.showMessageDialog(this, "La nota debe estar entre 0 y 50.", "Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                asignarNota(curso, grupo, tarea, estudiante, nota);
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Por favor ingrese una nota válida.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        });
    }

    // Obtener los cursos para el docente
    private String[] getCursos() {
        List<String> cursos = new ArrayList<>();
        try (Connection conn = ConexionDB.getConnection()) {
            String query = "SELECT codigo, nombre FROM cursos WHERE docente_id = ?";
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setString(1, docenteId); // Usa el ID del docente
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                cursos.add(rs.getString("codigo") + " - " + rs.getString("nombre"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al cargar los cursos.", "Error", JOptionPane.ERROR_MESSAGE);
        }

        return cursos.toArray(new String[0]);
    }

    // Obtener los grupos asociados a un curso
    private String[] getGrupos(String curso) {
        List<String> grupos = new ArrayList<>();
        String codigoCurso = curso.split(" - ")[0]; // Asume que el formato es "Código - Nombre"

        try (Connection conn = ConexionDB.getConnection()) {
            String query = "SELECT g.nombre FROM grupos_notas g " +
                    "JOIN cortes c ON g.corte_id = c.id " +
                    "WHERE c.curso_id = (SELECT id FROM cursos WHERE codigo = ?)";
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setString(1, codigoCurso);
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                grupos.add(rs.getString("nombre"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al cargar los grupos.", "Error", JOptionPane.ERROR_MESSAGE);
        }

        return grupos.toArray(new String[0]);
    }

    // Obtener los estudiantes de un grupo
    private String[] getEstudiantes(String curso) {
        List<String> estudiantes = new ArrayList<>();
        String codigoCurso = curso.split(" - ")[0]; // Asume que el formato es "Código - Nombre"

        try (Connection conn = ConexionDB.getConnection()) {
            // Consultamos los estudiantes que están en el curso
            String query = "SELECT e.nombre FROM estudiantes e " +
                    "JOIN estudiantes_cursos ec ON e.id = ec.estudiante_id " +
                    "JOIN cursos c ON ec.curso_id = c.id " +
                    "WHERE c.codigo = ?";  // Filtramos por código del curso
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setString(1, codigoCurso);
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                estudiantes.add(rs.getString("nombre"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al cargar los estudiantes.", "Error", JOptionPane.ERROR_MESSAGE);
        }

        return estudiantes.toArray(new String[0]);
    }
    
    // Obtener los estudiantes de un curso y grupo
    private String[] getEstudiantesPorGrupo(String curso, String grupo) {
        List<String> estudiantes = new ArrayList<>();
        String codigoCurso = curso.split(" - ")[0]; // Asume que el formato es "Código - Nombre"

        try (Connection conn = ConexionDB.getConnection()) {
            // Consultamos los estudiantes que están en el curso y en el grupo seleccionado
            String query = "SELECT e.nombre FROM estudiantes e " +
                    "JOIN estudiantes_cursos ec ON e.id = ec.estudiante_id " +
                    "JOIN cursos c ON ec.curso_id = c.id " +
                    "JOIN grupos_notas g ON g.corte_id = c.id " +
                    "WHERE c.codigo = ? AND g.nombre = ?";
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setString(1, codigoCurso);
            stmt.setString(2, grupo);
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                estudiantes.add(rs.getString("nombre"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al cargar los estudiantes.", "Error", JOptionPane.ERROR_MESSAGE);
        }

        return estudiantes.toArray(new String[0]);
    }

    // Asignar la nota a un estudiante para una tarea en un grupo
    private void asignarNota(String curso, String grupo, String tarea, String estudiante, int nota) {
        try (Connection conn = ConexionDB.getConnection()) {
            // Obtener el ID del estudiante
            String estudianteIdQuery = "SELECT id FROM estudiantes WHERE nombre = ?";
            PreparedStatement stmtEstudiante = conn.prepareStatement(estudianteIdQuery);
            stmtEstudiante.setString(1, estudiante);
            ResultSet rsEstudiante = stmtEstudiante.executeQuery();
            if (rsEstudiante.next()) {
                int estudianteId = rsEstudiante.getInt("id");

                // Obtener el ID del grupo
                String grupoIdQuery = "SELECT id FROM grupos_notas WHERE nombre = ?";
                PreparedStatement stmtGrupo = conn.prepareStatement(grupoIdQuery);
                stmtGrupo.setString(1, grupo);
                ResultSet rsGrupo = stmtGrupo.executeQuery();
                if (rsGrupo.next()) {
                    int grupoId = rsGrupo.getInt("id");

                    // Verificar si ya existe una nota para el estudiante en la misma tarea y grupo
                    String verificarNotaQuery = "SELECT COUNT(*) FROM notas_tareas WHERE grupo_id = ? AND estudiante_id = ? AND nombre_tarea = ?";
                    PreparedStatement stmtVerificarNota = conn.prepareStatement(verificarNotaQuery);
                    stmtVerificarNota.setInt(1, grupoId);
                    stmtVerificarNota.setInt(2, estudianteId);
                    stmtVerificarNota.setString(3, tarea);
                    ResultSet rsVerificarNota = stmtVerificarNota.executeQuery();

                    if (rsVerificarNota.next() && rsVerificarNota.getInt(1) > 0) {
                        JOptionPane.showMessageDialog(this, "Ya se ha asignado una nota para esta tarea en este grupo al estudiante.", "Error", JOptionPane.ERROR_MESSAGE);
                        return; // No insertar la nota si ya existe
                    }

                    // Insertar la nota en la base de datos
                    String insertQuery = "INSERT INTO notas_tareas (grupo_id, estudiante_id, nombre_tarea, nota) " +
                            "VALUES (?, ?, ?, ?)";
                    PreparedStatement stmtInsert = conn.prepareStatement(insertQuery);
                    stmtInsert.setInt(1, grupoId);
                    stmtInsert.setInt(2, estudianteId);
                    stmtInsert.setString(3, tarea);
                    stmtInsert.setInt(4, nota);
                    stmtInsert.executeUpdate();

                    JOptionPane.showMessageDialog(this, "Nota asignada correctamente.");
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al asignar la nota.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

}
