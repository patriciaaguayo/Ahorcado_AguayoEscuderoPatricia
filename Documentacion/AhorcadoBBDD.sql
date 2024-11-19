create database ahorcado;
use ahorcado;

create table if not exists usuarios(
idUsuario int primary key auto_increment,
nombre varchar (255)
);

create table if not exists ahorcado(
idPartida int primary key auto_increment,
intentos int
);

drop table ahorcado;

create table if not exists historial (
idUsuario int,
idPartida int,
Ganadas int,
Perdidas int,
primary key (idUsuario, idPartida),
FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario),
FOREIGN KEY (idPartida) REFERENCES ahorcado(idPartida)
);

create table if not exists tematicas (
idPalabra int primary key auto_increment,
palabra varchar (255),
tipo varchar (255)
);

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
('pantalla', 'Informatico'),
('intezfaz', 'Informatico'),
('metodo', 'Informatico'),
('variable', 'Informatico'),
('clase', 'Informatico');

create table if not exists Partida (
idPartida int,
idPalabra int,
primary key (idPartida, idPalabra),
FOREIGN KEY (idPartida) REFERENCES ahorcado(idPartida),
FOREIGN KEY (idPalabra) REFERENCES tematicas(idPalabra)
);

