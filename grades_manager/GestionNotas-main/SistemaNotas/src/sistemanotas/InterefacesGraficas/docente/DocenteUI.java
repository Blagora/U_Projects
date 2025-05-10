package sistemanotas.InterefacesGraficas.docente;

import sistemanotas.InterefacesGraficas.docente.AsignarNotasUI;
import sistemanotas.InterefacesGraficas.docente.GestionGruposUI;
import sistemanotas.InterefacesGraficas.docente.GestionCortesUI;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import sistemanotas.InterefacesGraficas.Login;

public class DocenteUI extends JFrame {
    private String docenteId; // ID del docente logueado

    public DocenteUI(String docenteId) {
        
        this.docenteId = docenteId;
        setTitle("Panel de Docente");
        setSize(400, 300);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel(new GridLayout(4, 1, 10, 10));

        JButton gestionarCortesButton = new JButton("Gestionar Cortes");
        JButton gestionarGruposButton = new JButton("Gestionar Grupos de Notas");
        JButton asignarNotasButton = new JButton("Asignar Notas");
        JButton salirButton = new JButton("Salir");

        panel.add(gestionarCortesButton);
        panel.add(gestionarGruposButton);
        panel.add(asignarNotasButton);
        panel.add(salirButton);

        add(panel);

        // Event Listeners
        gestionarCortesButton.addActionListener(e -> gestionarCortes());
        gestionarGruposButton.addActionListener(e -> gestionarGrupos());
        asignarNotasButton.addActionListener(e -> asignarNotas());
        salirButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                dispose();
                new Login().setVisible(true);
            }
        });
    }

    private void gestionarCortes() {
        // Mostrar ventana para gestionar cortes del curso
        new GestionCortesUI(docenteId).setVisible(true);
    }

    private void gestionarGrupos() {
        // Mostrar ventana para gestionar grupos dentro de cortes
        new GestionGruposUI(docenteId).setVisible(true);
    }

    private void asignarNotas() {
        // Mostrar ventana para asignar notas
        new AsignarNotasUI(docenteId).setVisible(true);
    }
}

