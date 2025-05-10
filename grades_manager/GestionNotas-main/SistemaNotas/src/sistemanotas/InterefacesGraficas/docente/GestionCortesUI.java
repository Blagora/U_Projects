package sistemanotas.InterefacesGraficas.docente;

import sistemanotas.ConexionBD.ConexionDB;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class GestionCortesUI extends JFrame {
    private String docenteId;
    private JTextField[] porcentajeFields; // Campos para los porcentajes de cada corte
    private JPanel porcentajePanel;

    public GestionCortesUI(String docenteId) {
        this.docenteId = docenteId;
        setTitle("Gestionar Cortes");
        setSize(600, 400);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        // Diseño
        JPanel panel = new JPanel();
        JLabel cursoLabel = new JLabel("Curso:");
        JComboBox<String> cursoComboBox = new JComboBox<>(getCursos()); // Cargar cursos del docente
        JLabel corteLabel = new JLabel("Número de cortes:");
        JComboBox<Integer> corteComboBox = new JComboBox<>(new Integer[]{3, 4}); // Opciones de cortes
        JButton guardarButton = new JButton("Guardar");

        // Panel para los porcentajes de cada corte
        porcentajePanel = new JPanel();
        porcentajeFields = new JTextField[4]; // Máximo de 4 cortes
        for (int i = 0; i < 4; i++) {
            JLabel label = new JLabel("Corte " + (i + 1) + ":");
            porcentajeFields[i] = new JTextField(5);
            porcentajePanel.add(label);
            porcentajePanel.add(porcentajeFields[i]);
        }

        // Mostrar u ocultar campos según el número de cortes
        corteComboBox.addActionListener(e -> actualizarCamposPorcentaje((Integer) corteComboBox.getSelectedItem()));

        panel.add(cursoLabel);
        panel.add(cursoComboBox);
        panel.add(corteLabel);
        panel.add(corteComboBox);
        panel.add(porcentajePanel);
        panel.add(guardarButton);

        add(panel);

        // Evento para guardar cortes
        guardarButton.addActionListener(e -> {
            String curso = (String) cursoComboBox.getSelectedItem();
            int numCortes = (Integer) corteComboBox.getSelectedItem();

            // Leer los porcentajes de cada corte
            double[] porcentajes = new double[numCortes];
            double sumaPorcentajes = 0;

            for (int i = 0; i < numCortes; i++) {
                try {
                    porcentajes[i] = Double.parseDouble(porcentajeFields[i].getText());
                    sumaPorcentajes += porcentajes[i];
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(this, "Por favor ingrese un porcentaje válido para todos los cortes.", "Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }
            }

            // Validar que la suma de los porcentajes sea 100
            if (sumaPorcentajes != 100) {
                JOptionPane.showMessageDialog(this, "Los porcentajes no suman 100%.", "Error", JOptionPane.ERROR_MESSAGE);
            } else {
                definirCortes(curso, numCortes, porcentajes);
            }
        });
    }

    private void actualizarCamposPorcentaje(int numCortes) {
        for (int i = 0; i < porcentajeFields.length; i++) {
            porcentajeFields[i].setVisible(i < numCortes); // Mostrar solo los campos necesarios
        }
        porcentajePanel.revalidate();
        porcentajePanel.repaint();
    }

    public String[] getCursos() {
        List<String> cursos = new ArrayList<>();
        try (Connection conn = ConexionDB.getConnection()) {
            String query = "SELECT codigo, nombre FROM cursos WHERE docente_id = ?";
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setString(1, docenteId); // Usa el ID del docente
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                String curso = rs.getString("codigo") + " - " + rs.getString("nombre");
                cursos.add(curso);
            }
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al cargar los cursos.", "Error", JOptionPane.ERROR_MESSAGE);
        }

        return cursos.toArray(new String[0]); // Convierte la lista a un arreglo
    }

    private void definirCortes(String curso, int numCortes, double[] porcentajes) {
        // Extraer el código del curso seleccionado
        String codigoCurso = curso.split(" - ")[0]; // Asume que el formato es "Código - Nombre"

        try (Connection conn = ConexionDB.getConnection()) {
            conn.setAutoCommit(false); // Inicio de transacción

            // Eliminar cortes anteriores para el curso
            String deleteQuery = "DELETE FROM cortes WHERE curso_id = (SELECT id FROM cursos WHERE codigo = ?)";
            try (PreparedStatement deleteStmt = conn.prepareStatement(deleteQuery)) {
                deleteStmt.setString(1, codigoCurso);
                deleteStmt.executeUpdate();
            }

            // Insertar los nuevos cortes con los porcentajes
            String insertQuery = "INSERT INTO cortes (curso_id, nombre, porcentaje) VALUES ((SELECT id FROM cursos WHERE codigo = ?), ?, ?)";
            try (PreparedStatement insertStmt = conn.prepareStatement(insertQuery)) {
                for (int i = 0; i < numCortes; i++) {
                    insertStmt.setString(1, codigoCurso);
                    insertStmt.setString(2, "Corte " + (i + 1)); // Nombrar los cortes "Corte 1", "Corte 2", ...
                    insertStmt.setDouble(3, porcentajes[i]); // Asignar porcentaje específico
                    insertStmt.addBatch(); // Agregar al batch
                }
                insertStmt.executeBatch(); // Ejecutar en lote
            }

            conn.commit(); // Confirmar la transacción
            JOptionPane.showMessageDialog(this, "Cortes definidos para el curso: " + curso);
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error al definir los cortes.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}


