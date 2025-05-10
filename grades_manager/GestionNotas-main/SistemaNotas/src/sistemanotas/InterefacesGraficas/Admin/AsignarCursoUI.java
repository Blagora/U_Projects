package sistemanotas.InterefacesGraficas.Admin;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
import java.util.List;
import static javax.swing.WindowConstants.DISPOSE_ON_CLOSE;
import sistemanotas.Estructura.AdminService;

public class AsignarCursoUI extends JFrame {

    private String codigoDocente;
    private AdminService adminService;
    private JComboBox<String> cursosComboBox;
    private JButton asignarButton;

    public AsignarCursoUI(String codigoDocente) {
        this.codigoDocente = codigoDocente;
        adminService = new AdminService();
        
        setTitle("Asignar Curso al Docente");
        setSize(400, 200);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        // Crear componentes
        cursosComboBox = new JComboBox<>();
        asignarButton = new JButton("Asignar Curso");

        // Cargar los cursos disponibles en el combo box
        cargarCursos();

        JPanel panel = new JPanel();
        panel.add(new JLabel("Selecciona un curso:"));
        panel.add(cursosComboBox);
        panel.add(asignarButton);

        add(panel);

        // Acción para asignar el curso
        asignarButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                asignarCurso();
            }
        });
    }

    // Cargar los cursos disponibles en el combo box
    private void cargarCursos() {
        List<String> cursos = adminService.obtenerCursosDisponibles(); // Método que recupera los cursos
        for (String curso : cursos) {
            cursosComboBox.addItem(curso);
        }
    }

    // Asignar el curso seleccionado al docente
    private void asignarCurso() {
        String cursoSeleccionado = (String) cursosComboBox.getSelectedItem();

        if (cursoSeleccionado != null && !cursoSeleccionado.isEmpty()) {
            // Obtén el código del curso para asignarlo al docente
            String codigoCurso = obtenerCodigoCurso(cursoSeleccionado);

            // Verificar si el docente ya tiene asignado el curso
            boolean cursoAsignado = adminService.verificarCursoAsignado(codigoDocente, codigoCurso);

            if (cursoAsignado) {
                JOptionPane.showMessageDialog(this, "Este curso ya ha sido asignado al docente.", "Error", JOptionPane.ERROR_MESSAGE);
            } else {
                // Asigna el curso al docente
                boolean asignado = adminService.asignarCursoADocente(codigoCurso, codigoDocente);

                if (asignado) {
                    JOptionPane.showMessageDialog(this, "Curso asignado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                    dispose(); // Cierra la ventana tras asignar el curso
                } else {
                    JOptionPane.showMessageDialog(this, "Error al asignar el curso. Intente nuevamente.", "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        } else {
            JOptionPane.showMessageDialog(this, "Por favor, seleccione un curso.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    // Método para obtener el código del curso basado en su nombre
    private String obtenerCodigoCurso(String nombreCurso) {
        // Aquí deberías implementar un método que recupere el código de un curso dado su nombre
        return adminService.obtenerCodigoCursoPorNombre(nombreCurso);
    }
}
