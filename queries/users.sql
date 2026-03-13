

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