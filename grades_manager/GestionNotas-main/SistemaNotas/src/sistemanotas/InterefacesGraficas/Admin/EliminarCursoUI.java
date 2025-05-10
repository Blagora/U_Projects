package sistemanotas.InterefacesGraficas.Admin;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;
import sistemanotas.Estructura.AdminService;

public class EliminarCursoUI extends JFrame {
    private AdminService adminService;

    public EliminarCursoUI(AdminService adminService) {
        this.adminService = adminService;
        
        setTitle("Eliminar Curso");
        setSize(400, 300);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel(new BorderLayout());
        JLabel label = new JLabel("Seleccione un curso para eliminar:");
        panel.add(label, BorderLayout.NORTH);

        // Obtener lista de cursos
        List<String> cursos = adminService.obtenerTodosLosCursos();
        String[] cursosArray = cursos.toArray(new String[0]);

        JList<String> listaCursos = new JList<>(cursosArray);
        JScrollPane scrollPane = new JScrollPane(listaCursos);
        panel.add(scrollPane, BorderLayout.CENTER);

        JButton eliminarButton = new JButton("Eliminar");
        eliminarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String cursoSeleccionado = listaCursos.getSelectedValue();

                if (cursoSeleccionado != null) {
                    // Obtener el código del curso por su nombre
                    String codigoCurso = adminService.obtenerCodigoCursoPorNombre(cursoSeleccionado);

                    // Eliminar el curso
                    boolean eliminado = adminService.eliminarCurso(codigoCurso);

                    if (eliminado) {
                        JOptionPane.showMessageDialog(null, "Curso eliminado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                        dispose();  // Cierra la ventana después de eliminar
                    } else {
                        JOptionPane.showMessageDialog(null, "Error al eliminar el curso. Intente nuevamente.", "Error", JOptionPane.ERROR_MESSAGE);
                    }
                } else {
                    JOptionPane.showMessageDialog(null, "Por favor, seleccione un curso.", "Advertencia", JOptionPane.WARNING_MESSAGE);
                }
            }
        });

        panel.add(eliminarButton, BorderLayout.SOUTH);
        add(panel);
    }
}

