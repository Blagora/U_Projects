package sistemanotas.Estructura;

public class Usuario {
    protected int id;
    protected String usuario;
    protected String contrasena;
    protected int rolId;

    public Usuario(int id, String usuario, String contrasena, int rolId) {
        this.id = id;
        this.usuario = usuario;
        this.contrasena = contrasena;
        this.rolId = rolId;
    }

    public int getId() {
        return id;
    }

    public String getUsuario() {
        return usuario;
    }

    public String getContrasena() {
        return contrasena;
    }

    public int getRolId() {
        return rolId;
    }
}

