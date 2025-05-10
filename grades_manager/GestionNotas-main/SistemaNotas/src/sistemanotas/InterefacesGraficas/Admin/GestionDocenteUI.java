package sistemanotas.InterefacesGraficas.Admin;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import sistemanotas.Estructura.AdminService;

public class GestionDocenteUI extends JFrame {

    private String codigoDocente;
    private String codigoCurso;
    private AdminService adminService;

    public GestionDocenteUI(String codigoDocente) {

        adminService = new AdminService();
        this.codigoDocente = codigoDocente;
        setTitle("Gestión de Docentes");
        setSize(500, 400);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        JButton editarDocenteButton = new JButton("Editar Docente");
        JButton eliminarDocenteButton = new JButton("Eliminar Docente");
        JButton asignarCursoButton = new JButton("Asignar Curso");
        JButton eliminarCursoButton = new JButton("Eliminar Curso");

        panel.add(editarDocenteButton);
        panel.add(eliminarDocenteButton);
        panel.add(asignarCursoButton);
        panel.add(eliminarCursoButton);
        add(panel);

        editarDocenteButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                abrirEditarDocente();
            }
        });

        eliminarDocenteButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                int confirm = JOptionPane.showConfirmDialog(null, 
                    "¿Está seguro de que desea eliminar este docente?", 
                    "Confirmar Eliminación", JOptionPane.YES_NO_OPTION);

                if (confirm == JOptionPane.YES_OPTION) {
                    boolean eliminado = adminService.eliminarDocente(codigoDocente);

                    if (eliminado) {
                        JOptionPane.showMessageDialog(null, "Docente eliminado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                    } else {
                        JOptionPane.showMessageDialog(null, "Error al eliminar docente.", "Error", JOptionPane.ERROR_MESSAGE);
                    }
                }
            }
        });

        // Acción para asignar un curso
        asignarCursoButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                abrirAsignarCurso();
            }
        });
        
        eliminarCursoButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                eliminarCursoDocente();
            }
        });
    }

    private void abrirEditarDocente() {
        new EditarDocenteUI(codigoDocente).setVisible(true);
    }

    private void abrirAsignarCurso() {
        new AsignarCursoUI(codigoDocente).setVisible(true);
    }
    
    private void eliminarCursoDocente() {
        // Obtener los cursos asignados al docente
        List<String> cursosAsignados = adminService.obtenerCursosPorDocente(codigoDocente);

        if (cursosAsignados == null || cursosAsignados.isEmpty()) {
            JOptionPane.showMessageDialog(this, "El docente no tiene cursos asignados.", "Información", JOptionPane.INFORMATION_MESSAGE);
            return;
        }

        // Mostrar un cuadro de diálogo para seleccionar el curso a eliminar
        String[] cursosArray = cursosAsignados.toArray(new String[0]);
        String cursoSeleccionado = (String) JOptionPane.showInputDialog(
            this, 
            "Seleccione el curso a eliminar:", 
            "Eliminar Curso del Docente", 
            JOptionPane.PLAIN_MESSAGE, 
            null, 
            cursosArray, 
            cursosArray[0]
        );

        if (cursoSeleccionado != null && !cursoSeleccionado.isEmpty()) {
            // Obtener el código del curso seleccionado
            String codigoCurso = adminService.obtenerCodigoCursoPorNombre(cursoSeleccionado);

            // Eliminar la asignación del curso al docente
            boolean eliminado = adminService.eliminarCursoDeDocente(codigoCurso, codigoDocente);

            if (eliminado) {
                JOptionPane.showMessageDialog(this, "Curso eliminado exitosamente.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Error al eliminar el curso. Intente nuevamente.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        } else {
            JOptionPane.showMessageDialog(this, "No se seleccionó ningún curso.", "Advertencia", JOptionPane.WARNING_MESSAGE);
        }
    }

}
    
