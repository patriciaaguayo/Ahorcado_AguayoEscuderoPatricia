create database ahorcado;
use ahorcado;

drop database ahorcado;

create table if not exists usuarios(
idUsuario int primary key auto_increment,
nombre varchar (255),
Ganadas int,
Perdidas int
);

select * from usuarios;

create table if not exists tematicas (
idPalabra int primary key auto_increment,
palabra varchar (255),
tipo varchar (255)
);

select * from tematicas;

INSERT INTO tematicas (palabra, tipo) VALUES 
('carla', 'Personas'),
('alberto', 'Personas'),
('andrea', 'Personas'),
('mariano', 'Personas'),
('martin', 'Personas'),
('naranja', 'Frutas'),
('pera', 'Frutas'),
('manzana', 'Frutas'),
('uva', 'Frutas'),
('platano', 'Frutas'),
('pantalla', 'Conceptos_Informaticos'),
('intezfaz', 'Conceptos_Informaticos'),
('metodo', 'Conceptos_Informaticos'),
('variable', 'Conceptos_Informaticos'),
('clase', 'Conceptos_Informaticos');