package sistemanotas.InterefacesGraficas.Admin;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import sistemanotas.Estructura.AdminService;

public class GestionEstudianteUI extends JFrame {

    private String codigoEstudiante;
    private AdminService adminService;

    public GestionEstudianteUI(String codigoEstudiante) {
        
        this.adminService = new AdminService();
        this.codigoEstudiante = codigoEstudiante;

        setTitle("Gestión de Estudiantes");
        setSize(500, 400);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        JButton editarEstudianteButton = new JButton("Editar Estudiante");
        JButton eliminarEstudianteButton = new JButton("Eliminar Estudiante");
        JButton asignarCursoButton = new JButton("Asignar Curso");
        JButton eliminarCursoButton = new JButton("Eliminar Curso");

        panel.add(editarEstudianteButton);
        panel.add(eliminarEstudianteButton);
        panel.add(asignarCursoButton);
        panel.add(eliminarCursoButton);
        add(panel);

        asignarCursoButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                asignarCurso();
            }
        });
        
        eliminarCursoButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                eliminarCurso();
            }
        });


        editarEstudianteButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                abrirEditarEstudiante();
            }
        });

        eliminarEstudianteButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                int confirm = JOptionPane.showConfirmDialog(null,
                        "¿Está seguro de que desea eliminar este estudiante?",
                        "Confirmar Eliminación", JOptionPane.YES_NO_OPTION);

                if (confirm == JOptionPane.YES_OPTION) {
                    boolean eliminado = adminService.eliminarEstudiante(codigoEstudiante);

                    if (eliminado) {
                        JOptionPane.showMessageDialog(null, "Estudiante eliminado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                    } else {
                        JOptionPane.showMessageDialog(null, "Error al eliminar estudiante.", "Error", JOptionPane.ERROR_MESSAGE);
                    }
                }
            }
        });
    }

    private void asignarCurso() {
     // Mostrar un cuadro de diálogo para seleccionar un curso
        List<String> cursos = adminService.obtenerCursosDisponibles();  // Método que devuelve los cursos disponibles

        String[] cursosArray = cursos.toArray(new String[0]);
        String cursoSeleccionado = (String) JOptionPane.showInputDialog(this, 
         "Selecciona un curso", 
         "Asignar Curso", 
         JOptionPane.PLAIN_MESSAGE, 
         null, 
         cursosArray, 
         cursosArray[0]);

     if (cursoSeleccionado != null && !cursoSeleccionado.isEmpty()) {
         // Obtener el código del curso a partir del nombre
         String codigoCurso = adminService.obtenerCodigoCursoPorNombre(cursoSeleccionado);

         // Verificar si el curso ya está asignado al estudiante
         boolean cursoAsignado = adminService.verificarCursoAsignadoEst(codigoEstudiante, codigoCurso);

         if (cursoAsignado) {
             JOptionPane.showMessageDialog(this, "Este curso ya ha sido asignado al estudiante.", "Error", JOptionPane.ERROR_MESSAGE);
         } else {
             // Asignar el curso al estudiante
             boolean asignado = adminService.asignarCursoAEstudiante(codigoEstudiante, codigoCurso);

             if (asignado) {
                 JOptionPane.showMessageDialog(this, "Curso asignado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
             } else {
                 JOptionPane.showMessageDialog(this, "Error al asignar el curso. Intente nuevamente.", "Error", JOptionPane.ERROR_MESSAGE);
             }
         }
     } else {
         JOptionPane.showMessageDialog(this, "Por favor, seleccione un curso.", "Error", JOptionPane.ERROR_MESSAGE);
     }
 }

    
    private void eliminarCurso() {
    // Obtener los cursos asignados al estudiante
    List<String> cursosAsignados = adminService.obtenerCursosAsignados(codigoEstudiante); // Método que devuelve los cursos asignados

    if (cursosAsignados == null || cursosAsignados.isEmpty()) {
        JOptionPane.showMessageDialog(this, "El estudiante no tiene cursos asignados.", "Información", JOptionPane.INFORMATION_MESSAGE);
        return;
    }

    // Mostrar los cursos en un cuadro de diálogo para seleccionar
    String[] cursosArray = cursosAsignados.toArray(new String[0]);
    String cursoSeleccionado = (String) JOptionPane.showInputDialog(this, 
            "Selecciona el curso a eliminar", 
            "Eliminar Curso", 
            JOptionPane.PLAIN_MESSAGE, 
            null, 
            cursosArray, 
            cursosArray[0]);

        if (cursoSeleccionado != null && !cursoSeleccionado.isEmpty()) {
            // Obtener el código del curso seleccionado (si es necesario)
            String codigoCurso = adminService.obtenerCodigoCursoPorNombre(cursoSeleccionado);

            // Llamar al servicio para eliminar el curso
            boolean eliminado = adminService.eliminarCursoDeEstudiante(codigoEstudiante, codigoCurso);

            if (eliminado) {
                JOptionPane.showMessageDialog(this, "Curso eliminado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Error al eliminar el curso. Intente nuevamente.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        } else {
            JOptionPane.showMessageDialog(this, "No se seleccionó ningún curso.", "Advertencia", JOptionPane.WARNING_MESSAGE);
        }
    }

    
    private void abrirEditarEstudiante() {
        new EditarEstudianteUI(codigoEstudiante).setVisible(true);
    }
    
    
}


