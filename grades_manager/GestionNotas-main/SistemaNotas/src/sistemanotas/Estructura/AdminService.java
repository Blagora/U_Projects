package sistemanotas.Estructura;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import sistemanotas.ConexionBD.ConexionDB;

public class AdminService {

    public Usuario autenticarUsuario(String usuario, String contrasena) {
        try (Connection conn = ConexionDB.getConnection()) {
            String query = "SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?";
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setString(1, usuario);
            stmt.setString(2, contrasena);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                int id = rs.getInt("id");
                int rolId = rs.getInt("rol_id");
                String nombreUsuario = rs.getString("usuario");
                String contrasenaUsuario = rs.getString("contrasena");

                switch (rolId) {
                    case 1: // Admin
                        return new Usuario(id, nombreUsuario, contrasenaUsuario, rolId); // Cambia a Admin si lo necesitas
                    case 2: // Docente
                        return obtenerDocentePorUsuarioId(id);
                    case 3: // Estudiante
                        return obtenerEstudiantePorUsuarioId(id);
                    default:
                        return null;
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public Estudiante obtenerEstudiantePorUsuarioId(int usuarioId) {
        try (Connection conn = ConexionDB.getConnection()) {
            String query = "SELECT * FROM estudiantes WHERE usuario_id = ?";
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setInt(1, usuarioId);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                return new Estudiante(
                    rs.getInt("id"),                 // id
                    rs.getString("usuario"),          // usuario
                    rs.getString("contrasena"),       // contrasena
                    rs.getInt("rol_id"),              // rolId
                    rs.getString("codigo"),           // codigo
                    rs.getString("nombre"),           // nombre
                    rs.getString("apellido"),         // apellido
                    rs.getString("correo")             // correo
                );
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public Docente obtenerDocentePorUsuarioId(int usuarioId) {
    try (Connection conn = ConexionDB.getConnection()) {
        String query = "SELECT * FROM docentes WHERE usuario_id = ?";
        PreparedStatement stmt = conn.prepareStatement(query);
        stmt.setInt(1, usuarioId);
        ResultSet rs = stmt.executeQuery();

        if (rs.next()) {
            return new Docente(
                rs.getInt("id"),                 // id
                rs.getString("usuario"),          // usuario
                rs.getString("contrasena"),       // contrasena
                rs.getInt("rol_id"),              // rolId
                rs.getString("codigo"),         //codigo
                rs.getString("nombre"),           // nombre
                rs.getString("apellido"),         // apellido
                rs.getString("correo"),           // correo
                rs.getString("area")            // area
            );
        }
    } catch (SQLException e) {
        e.printStackTrace();
    }
        return null;
    }
    
    public boolean agregarEstudiante(String codigo, String nombre, String apellido, String correo) {
        String insertUsuarioQuery = "INSERT INTO usuarios (usuario, contrasena, rol_id) VALUES (?, ?, ?)";
        String insertEstudianteQuery = "INSERT INTO estudiantes (codigo, usuario_id, nombre, apellido, correo) VALUES (?, ?, ?, ?, ?)";

        try (Connection conn = ConexionDB.getConnection()) {
            // Primero, insertamos el usuario
            PreparedStatement stmtUsuario = conn.prepareStatement(insertUsuarioQuery, Statement.RETURN_GENERATED_KEYS);
            stmtUsuario.setString(1, correo);  // El correo como usuario
            stmtUsuario.setString(2, codigo);  // El código como contraseña
            stmtUsuario.setInt(3, 3);             // El rol de estudiante es 3

            int rowsInsertedUsuario = stmtUsuario.executeUpdate();

            if (rowsInsertedUsuario > 0) {
                // Obtener el ID del usuario insertado
                ResultSet generatedKeys = stmtUsuario.getGeneratedKeys();
                if (generatedKeys.next()) {
                    int usuarioId = generatedKeys.getInt(1); // Obtener el ID generado

                    // Ahora insertamos el estudiante
                    PreparedStatement stmtEstudiante = conn.prepareStatement(insertEstudianteQuery);
                    stmtEstudiante.setString(1, codigo);       // Código del estudiante
                    stmtEstudiante.setInt(2, usuarioId);       // ID del usuario insertado
                    stmtEstudiante.setString(3, nombre);       // Nombre del estudiante
                    stmtEstudiante.setString(4, apellido);     // Apellido del estudiante
                    stmtEstudiante.setString(5, correo);       // Correo del estudiante

                    int rowsInsertedEstudiante = stmtEstudiante.executeUpdate();
                    return rowsInsertedEstudiante > 0; // Retorna true si se insertó correctamente
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false; // Retorna false en caso de error
    }
    
    public boolean agregarDocente(String codigo, String nombre, String apellido, String correo, String area) {
        String insertUsuarioQuery = "INSERT INTO usuarios (usuario, contrasena, rol_id) VALUES (?, ?, ?)";
        String insertDocenteQuery = "INSERT INTO docentes (codigo, usuario_id, nombre, apellido, correo, area) VALUES (?, ?, ?, ?, ?, ?)";

        try (Connection conn = ConexionDB.getConnection()) {
            // Primero, insertamos el usuario
            PreparedStatement stmtUsuario = conn.prepareStatement(insertUsuarioQuery, Statement.RETURN_GENERATED_KEYS);
            stmtUsuario.setString(1, correo);  // El correo como usuario
            stmtUsuario.setString(2, codigo);  // El código como contraseña
            stmtUsuario.setInt(3, 2);             // El rol de docente es 2

            int rowsInsertedUsuario = stmtUsuario.executeUpdate();

            if (rowsInsertedUsuario > 0) {
                // Obtener el ID del usuario insertado
                ResultSet generatedKeys = stmtUsuario.getGeneratedKeys();
                if (generatedKeys.next()) {
                    int usuarioId = generatedKeys.getInt(1); // Obtener el ID generado

                    // Ahora insertamos el estudiante
                    PreparedStatement stmtDocente = conn.prepareStatement(insertDocenteQuery);
                    stmtDocente.setString(1, codigo);       // Código del docente
                    stmtDocente.setInt(2, usuarioId);       // ID del usuario insertado
                    stmtDocente.setString(3, nombre);       // Nombre del docente
                    stmtDocente.setString(4, apellido);     // Apellido del docente
                    stmtDocente.setString(5, correo);       // Correo del docente
                    stmtDocente.setString(6, area);       // Area del docente
                    
                    int rowsInsertedDocente = stmtDocente.executeUpdate();
                    return rowsInsertedDocente > 0; // Retorna true si se insertó correctamente
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false; // Retorna false en caso de error
    }

    public Estudiante obtenerEstudiante(String codigo) {
    String query = "SELECT e.codigo, e.nombre, e.apellido, e.correo " +
                   "FROM estudiantes e " +
                   "JOIN usuarios u ON e.usuario_id = u.id " +
                   "WHERE e.codigo = ?";

    try (Connection conn = ConexionDB.getConnection();
         PreparedStatement stmt = conn.prepareStatement(query)) {
        
        stmt.setString(1, codigo);  // Asigna el código al parámetro de la consulta
        ResultSet rs = stmt.executeQuery();
        
        if (rs.next()) {
            // Extrae los datos del ResultSet
            String codigoEstudiante = rs.getString("codigo");
            String nombre = rs.getString("nombre");
            String apellido = rs.getString("apellido");
            String correo = rs.getString("correo");

            // Crea el objeto Estudiante usando valores predeterminados para parámetros adicionales
            return new Estudiante(
                0,                  // id
                "",                 // usuario
                "",                 // contrasena
                0,                  // rolId
                codigoEstudiante,   // código
                nombre,             // nombre
                apellido,           // apellido
                correo             // correo
            );
        }
        } catch (SQLException e) {
            e.printStackTrace();  // Maneja la excepción (puedes agregar un mejor manejo si lo prefieres)
        }

        return null; // Retorna null si no se encuentra el estudiante o si ocurre un error
    }
    
    public Docente obtenerDocente(String codigo) {
        String query = "SELECT d.codigo, d.nombre, d.apellido, d.correo, d.area " +
                       "FROM docentes d " +
                       "JOIN usuarios u ON d.usuario_id = u.id " +
                       "WHERE d.codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigo);  // Asigna el código al parámetro de la consulta
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                // Extrae los datos del ResultSet
                String codigoDocente = rs.getString("codigo");
                String nombre = rs.getString("nombre");
                String apellido = rs.getString("apellido");
                String correo = rs.getString("correo");
                String area = rs.getString("area");

                // Crea el objeto Estudiante usando valores predeterminados para parámetros adicionales
                return new Docente(
                    0,                  // id
                    "",                 // usuario
                    "",                 // contrasena
                    0,                  // rolId
                    codigoDocente,   // código
                    nombre,             // nombre
                    apellido,           // apellido
                    correo,           // correo
                    area             // area
                );
            }
            } catch (SQLException e) {
                e.printStackTrace();  // Maneja la excepción (puedes agregar un mejor manejo si lo prefieres)
            }
        return null; // Retorna null si no se encuentra el estudiante o si ocurre un error
    }
    
    public boolean actualizarEstudiante(String codigo, String nombre, String apellido, String correo) {
        String query = "UPDATE estudiantes SET nombre = ?, apellido = ?, correo = ? WHERE codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, nombre);   // Asigna el nombre al primer parámetro
            stmt.setString(2, apellido); // Asigna el apellido al segundo parámetro
            stmt.setString(3, correo);   // Asigna el correo al tercer parámetro
            stmt.setString(4, codigo);   // Usa el código para identificar al estudiante

            int rowsUpdated = stmt.executeUpdate();
            return rowsUpdated > 0; // Retorna true si se actualizó al menos una fila
        } catch (SQLException e) {
            e.printStackTrace(); // Manejo de la excepción (puedes mejorar el manejo si lo deseas)
        }

        return false; // Retorna false en caso de error
    }

    public boolean actualizarDocente(String codigo, String nombre, String apellido, String correo, String area) {
        String query = "UPDATE docentes SET nombre = ?, apellido = ?, correo = ?, area = ? WHERE codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, nombre);   // Asigna el nombre al primer parámetro
            stmt.setString(2, apellido); // Asigna el apellido al segundo parámetro
            stmt.setString(3, correo);   // Asigna el correo al tercer parámetro
            stmt.setString(4, area);   // Asigna el area al tercer parámetro
            stmt.setString(5, codigo);   // Usa el código para identificar al estudiante

            int rowsUpdated = stmt.executeUpdate();
            return rowsUpdated > 0; // Retorna true si se actualizó al menos una fila
        } catch (SQLException e) {
            e.printStackTrace(); // Manejo de la excepción (puedes mejorar el manejo si lo deseas)
        }

        return false; // Retorna false en caso de error
    }
    
    public boolean eliminarEstudiante(String codigo) {
        String query = "DELETE FROM estudiantes WHERE codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigo);  // Asigna el código al parámetro de la consulta
            int rowsAffected = stmt.executeUpdate();  // Ejecuta la consulta de eliminación

            return rowsAffected > 0;  // Devuelve true si se eliminó al menos un registro
        } catch (SQLException e) {
            e.printStackTrace();  // Maneja la excepción (puedes agregar un mejor manejo si lo prefieres)
        }
        return false;  // Devuelve false si no se eliminó ningún registro o si ocurrió un error
    }
    
    public boolean eliminarDocente(String codigo) {
        String query = "DELETE FROM docentes WHERE codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigo);  // Asigna el código al parámetro de la consulta
            int rowsAffected = stmt.executeUpdate();  // Ejecuta la consulta de eliminación

            return rowsAffected > 0;  // Devuelve true si se eliminó al menos un registro
        } catch (SQLException e) {
            e.printStackTrace();  // Maneja la excepción (puedes agregar un mejor manejo si lo prefieres)
        }
        return false;  // Devuelve false si no se eliminó ningún registro o si ocurrió un error
    }
    
    public boolean crearCurso(String codigo, String nombre) {
        String query = "INSERT INTO cursos (codigo, nombre) VALUES (?, ?)";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigo);  // Asigna el código al parámetro de la consulta
            stmt.setString(2, nombre);  // Asigna el nombre al parámetro de la consulta
            int rowsAffected = stmt.executeUpdate();  // Ejecuta la consulta de inserción

            return rowsAffected > 0;  // Devuelve true si se insertó al menos un registro
        } catch (SQLException e) {
            e.printStackTrace();  // Maneja la excepción (puedes agregar un mejor manejo si lo prefieres)
        }
        return false;  // Devuelve false si ocurrió un error o no se insertó el registro
    }

    public List<String> obtenerCursosDisponibles() {
        List<String> cursos = new ArrayList<>();
        String query = "SELECT nombre FROM cursos";  // Consulta para obtener los cursos disponibles

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                cursos.add(rs.getString("nombre"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return cursos;
    }

    public boolean asignarCursoADocente(String codigoCurso, String codigoDocente) {
    // Consulta para asignar el curso al docente
    String query = "UPDATE cursos SET docente_id = ? WHERE codigo = ?";

    try (Connection conn = ConexionDB.getConnection();
         PreparedStatement stmt = conn.prepareStatement(query)) {

        // Asigna los parámetros correctamente
        stmt.setString(1, codigoDocente);  // Código del docente
        stmt.setString(2, codigoCurso);    // Código del curso

        int rowsAffected = stmt.executeUpdate();  // Ejecuta la consulta de actualización

        return rowsAffected > 0;  // Devuelve true si la asignación fue exitosa
    } catch (SQLException e) {
        e.printStackTrace();
    }
    return false;
}
    
    public String obtenerCodigoCursoPorNombre(String nombreCurso)                                                                                                       {
        String query = "SELECT codigo FROM cursos WHERE nombre = ?";
        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, nombreCurso);  // Asigna el nombre del curso

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("codigo");  // Retorna el código del curso
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;  // Devuelve null si no se encuentra el curso
    }
    
    public boolean asignarCursoAEstudiante(String codigoEstudiante, String codigoCurso) {
        String query = "INSERT INTO estudiantes_cursos (estudiante_id, curso_id) " +
                       "SELECT e.id, c.id FROM estudiantes e, cursos c " +
                       "WHERE e.codigo = ? AND c.codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setString(1, codigoEstudiante);
            stmt.setString(2, codigoCurso);
            int rowsAffected = stmt.executeUpdate();

            return rowsAffected > 0;  // Si se insertó una fila, la asignación fue exitosa
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean eliminarCursoDeEstudiante(String codigoEstudiante, String codigoCurso) {
        String query = "DELETE FROM estudiantes_cursos " +
                       "WHERE estudiante_id = (SELECT id FROM estudiantes WHERE codigo = ?) " +
                       "AND curso_id = (SELECT id FROM cursos WHERE codigo = ?)";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigoEstudiante);  // Código del estudiante
            stmt.setString(2, codigoCurso);      // Código del curso
            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;  // Devuelve true si se eliminó exitosamente
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false;
    }

    public List<String> obtenerCursosAsignados(String codigoEstudiante) {
        List<String> cursos = new ArrayList<>();
        String query = "SELECT c.nombre FROM cursos c " +
                       "JOIN estudiantes_cursos ec ON c.id = ec.curso_id " +
                       "JOIN estudiantes e ON e.id = ec.estudiante_id " +
                       "WHERE e.codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigoEstudiante);  // Código del estudiante

            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    cursos.add(rs.getString("nombre"));  // Agrega el nombre del curso a la lista
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return cursos;
    }

    public List<String> obtenerCursosPorDocente(String codigoDocente) {
        List<String> cursos = new ArrayList<>();
        String query = "SELECT nombre FROM cursos WHERE docente_id = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigoDocente);  // Usa el código del docente

            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    cursos.add(rs.getString("nombre"));  // Agrega el nombre del curso a la lista
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return cursos;
    }

    public boolean eliminarCursoDeDocente(String codigoCurso, String codigoDocente) {
        String query = "UPDATE cursos SET docente_id = NULL WHERE codigo = ? AND docente_id = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigoCurso);     // Código del curso
            stmt.setString(2, codigoDocente);  // Código del docente

            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;  // Devuelve true si se actualizó al menos una fila
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false;
    }

    public List<String> obtenerTodosLosCursos() {
        List<String> cursos = new ArrayList<>();
        String query = "SELECT nombre FROM cursos";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                cursos.add(rs.getString("nombre"));  // Agrega el nombre de cada curso
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return cursos;
    }
    
    public boolean eliminarCurso(String codigoCurso) {
        String query = "DELETE FROM cursos WHERE codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, codigoCurso);  // Establece el código del curso
            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;  // Devuelve true si se eliminó el curso
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return false;
    }
    
    public boolean verificarCursoAsignado(String codigoDocente, String codigoCurso) {
        boolean asignado = false;
        String query = "SELECT 1 FROM cursos WHERE docente_id = ? AND codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setString(1, codigoDocente);
            stmt.setString(2, codigoCurso);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                asignado = true;  // El curso ya está asignado al docente
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return asignado;
    }

    public boolean verificarCursoAsignadoEst(String codigoEstudiante, String codigoCurso) {
        boolean asignado = false;
        String query = "SELECT 1 FROM estudiantes_cursos ec " +
                       "JOIN estudiantes e ON ec.estudiante_id = e.id " +
                       "JOIN cursos c ON ec.curso_id = c.id " +
                       "WHERE e.codigo = ? AND c.codigo = ?";

        try (Connection conn = ConexionDB.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setString(1, codigoEstudiante);
            stmt.setString(2, codigoCurso);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                asignado = true;  // El curso ya está asignado al estudiante
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return asignado;
    }


}
