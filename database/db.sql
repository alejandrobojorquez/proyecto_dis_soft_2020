drop database electroquiz;

create database electroquiz;

use electroquiz;

create table usuarios (
id int primary key auto_increment,
nombres varchar(50),
login varchar(30),
clave varchar(30),
tipo varchar(10)
);

insert into usuarios(nombres,login,clave,tipo) values('Oscar Sifuentes','Fuentes@utec.edu.pe','Electro4321','alumno');

insert into usuarios(nombres,login,clave,tipo) values('Alianza','AL@utec.edu.pe','alianza','alumno');

insert into usuarios(nombres,login,clave,tipo) values('administrador','admin1','dis_soft_2020','admin');


create table preguntas(
id int primary key auto_increment,
enunciado varchar(250),
ans1 varchar(50),
ans2 varchar(50),
ans3 varchar(50),
ans4 varchar(50),
correct_ans varchar(50),
tipo varchar(1));

insert into preguntas(enunciado,ans1,ans2,ans3, ans4, correct_ans, tipo) values('¿Este juego funciona?','no creo','algun dia','hoy no gente','RPTA CORRECTA','RPTA CORRECTA','a');


