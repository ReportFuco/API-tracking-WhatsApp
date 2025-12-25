
-- Reiniciar los Index para no duplicar la información

truncate table 
    usuario,
    mensaje,
    gimnasio,
    entrenamiento,
    entrenamiento_aerobico,
    entrenamiento_fuerza,
    serie_fuerza,
    ejercicios,
    banco,
    cuenta_bancaria,
    categoria_finanza,
    movimiento,
    categoria_habito,
    habito,
    registro_habito,
    libros,
    lectura,
    registro_lectura
restart identity cascade;


-- ingresar Usuarios para las pruebas

insert into usuario (nombre, telefono)
values ('Francisco Arancibia', '56978086719'),
       ('Rodrigo Arancibia', '56954951334'),
       ('Daniel Arancibia', '56962288047');

-- insertar ejercicios

insert into ejercicios (nombre, tipo, url_video)
values ('Press banca con mancuerna', 'pecho', null),
       ('Press banca con barra', 'pecho', null),
       ('Press banca inclinada con mancuerna ', 'pecho', null),
       ('Press banca inclinada con barra', 'pecho', null),
       ('Aperturas con mancuerna en banco plano', 'pecho', null),
       ('Aperturas con mancuerna en banco inclinado', 'pecho', null),
       ('Aperturas en polea alta', 'pecho', null),
       ('Aperturas en polea media', 'pecho', null),
       ('Aperturas en polea baja', 'pecho', null),
       ('Máquina prensa pecho', 'pecho', null),
       ('Press militar con mancuerna', 'hombro', null),
       ('Press militar con barra', 'hombro', null),
       ('Elevaciones laterales', 'hombro', null),
       ('Elevaciones frontales', 'hombro', null),
       ('Curl de Biceps Martillo', 'bicep', null),
       ('Curl de Biceps Araña', 'bicep', null),
       ('Curl de Biceps Araña con barra', 'bicep', null);

-- ingresar Gimnasios
insert into gimnasio (nombre_gimnasio, nombre_cadena, direccion, comuna, latitud, longitud)
values ('SmartFit Maipú Central', 'SmartFit', 'Av. Pajaritos 2689, local 14', 'Maipú', -33.502612790405934, -70.7564164067453),
       ('SmartFit Monte Tabor', 'SmartFit', 'Av. Los Pajaritos 4500, local 14', 'Maipú', -33.480828702723116, -70.74637977826353),
       ('SmartFit Pajaritos', 'SmartFit', 'Avenida Teniente Cruz N°0015', 'Pudahuel', -33.469279741065556, -70.73597770695618),
       ('SmartFit Maipú City Point', 'SmartFit', 'Av. Los Pajaritos 1948', 'Maipú', -33.50946244351643, -70.75818382919813),
       ('SmartFit Oeste', 'SmartFit', 'Av. Américo Vespucio 2500', 'Cerrillos', -33.516320413640734, -70.70923236091664),
       ('SmartFit espacio M', 'SmartFit', 'Compañia de Jesús 1214 local 218', 'Santiago', -33.43895887354157, -70.65419773246775),
       ('SmartFit Catedral', 'SmartFit', 'Catedral 1850, Santiago', 'Santiago', -33.438157268,-70.6630968153);

insert into entrenamiento (id_usuario, tipo_entrenamiento)
values (1, 'fuerza');


insert into entrenamiento_fuerza (id_entrenamiento, id_gimnasio)
values (1, 1);


insert into serie_fuerza (id_entrenamiento_fuerza, id_ejercicio, es_calentamiento, cantidad_peso, repeticiones)
values (1, 1, 'false', 30, 10),
       (1, 1, 'false', 30, 10),
       (1, 1, 'false', 28, 10),
       (1, 1, 'false', 28, 10),
       (1, 3, 'false', 24, 10),
       (1, 3, 'false', 24, 10),
       (1, 3, 'false', 24, 10),
       (1, 3, 'false', 20, 8);
