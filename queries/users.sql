
-- Ver los usuarios activos
SELECT * FROM usuario;
UPDATE usuario SET auth_user_id = 3 WHERE id_usuario = 3

SELECT * FROM usuario;
SELECT * FROM "user";
-- Movimiento de tabla
SELECT 
    mov.id_transaccion,
    mov.tipo_movimiento,
    mov.tipo_gasto,
    mov.monto,
    mov.descripcion,
    mov.created_at,
    cue.nombre_cuenta,
    cat.nombre
FROM movimiento AS mov
    LEFT JOIN cuenta_bancaria AS cue
        ON cue.id_cuenta = mov.id_cuenta
    LEFT JOIN categoria_finanza AS cat
        ON cat.id_categoria = mov.id_categoria;


UPDATE cuenta_bancaria 
SET activo = TRUE
WHERE id_cuenta = 1;
