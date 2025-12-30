

-- UPDATE entrenamiento_fuerza
-- SET estado = 'cerrado'
-- WHERE id_entrenamiento_fuerza = 1;


-- select * from entrenamiento_fuerza;

-- select u.id_usuario, u.nombre, e.id_entrenamiento, e.tipo_entrenamiento, ef.estado 
-- from usuario u 
-- join entrenamiento e on e.id_usuario = u.id_usuario
-- join entrenamiento_fuerza ef ON ef.id_entrenamiento = e.id_entrenamiento
-- where u.id_usuario=1;

-- select * from ejercicios;

-- CREATE EXTENSION IF NOT EXISTS unaccent;
-- select * from movimiento;



INSERT INTO movimiento (id_categoria,id_usuario, id_cuenta, tipo_movimiento, tipo_gasto, monto, descripcion) VALUES (1,1,1,'gasto', 'variable',  3000, 'nada');

select * from movimiento;