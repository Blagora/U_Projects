# GestionNotas
Proyecto tercer semestre POO
DB

CREATE DATABASE gestion_notas;
USE gestion_notas;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    contrasena VARCHAR(50) NOT NULL,
    rol_id INT,
    FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE CASCADE
);

CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    usuario_id INT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    correo VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE docentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    usuario_id INT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    correo VARCHAR(100),
    area VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo varchar(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    docente_id varchar(50),
    num_cortes INT DEFAULT 0,
    FOREIGN KEY (docente_id) REFERENCES docentes(codigo) ON DELETE SET NULL
);

CREATE TABLE estudiantes_cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    curso_id INT,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

CREATE TABLE cortes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    porcentaje INT NOT NULL,	
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

CREATE TABLE grupos_notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    corte_id INT NOT NULL,   
    nombre VARCHAR(50) NOT NULL,   
    porcentaje INT NOT NULL,    
    FOREIGN KEY (corte_id) REFERENCES cortes(id) ON DELETE CASCADE,
    UNIQUE (corte_id, nombre)   
);


CREATE TABLE notas_tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grupo_id INT NOT NULL,         
    estudiante_id INT NOT NULL,   
    nombre_tarea VARCHAR(50) NOT NULL, 
    nota INT NOT NULL CHECK (nota BETWEEN 0 AND 50),
    FOREIGN KEY (grupo_id) REFERENCES grupos_notas(id) ON DELETE CASCADE,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    UNIQUE (grupo_id, estudiante_id, nombre_tarea) 
);


-- Insertar los roles
INSERT INTO roles (nombre) VALUES ('ADMIN'), ('DOCENTE'), ('ESTUDIANTE');

-- Insertar el usuario admin con su rol
INSERT INTO usuarios (usuario, contrasena, rol_id) VALUES ('admin', 'admin123', 1);

Driver Java
https://dev.mysql.com/downloads/connector/j/
