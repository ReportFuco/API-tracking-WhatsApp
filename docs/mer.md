```mermaid
	erDiagram
		direction TB
		usuario {
			bigint id_usuario PK
			varchar nombre  v
			varchar numero_telefono UK
			boolean activo
			datetime fecha_registro
		}

		mensaje {
			bigint id_mensaje PK
			bigint id_usuario FK
			text contenido
			varchar direccion
			datetime fecha_envio
		}

		habito {
			bigint id_habito PK
			bigint id_usuario FK
			varchar nombre
			bigint id_categoria FK
			text descripcion
			varchar frecuencia
			boolean activo
			datetime fecha_creacion
		}

		categoria_habito {
			bigint id_categoria PK
			varchar nombre
			datetime fecha_creacion
		}


		registro_habito {
			bigint id_registro PK
			bigint id_habito FK
			date fecha
			text observacion
		}

		libro {
			int id_libro PK
			string nombre_libro
			string autor
			int total_paginas
			string categoria
		}

		lectura {
			bigint id_lectura PK
			bigint id_usuario FK
			int id_libro FK
			date fecha_inicio
			date fecha_fin
			string estado
		}

		registro_lectura {
			bigint id_registro PK
			bigint id_lectura FK
			int pagina_inicio
			int pagina_final
			text detalle
			date fecha_registro
		}

		banco {
			int id_banco PK
			varchar nombre_banco
		}

		cuenta_bancaria {
			bigint id_cuenta PK
			bigint id_usuario FK
			int id_banco FK
			varchar nombre_targeta
			varchar tipo_tarjeta
		}

		categoria_finanza {
			bigint id_categoria PK
			varchar nombre
		}

		transaccion_finanza {
			bigint id_transaccion PK
			bigint id_usuario FK
			bigint id_categoria FK
			bigint id_cuenta FK
			varchar tipo
			int monto
			text descripcion
			datetime fecha
		}

		entrenamiento {
			bigint id_entrenamiento PK
			bigint id_usuario FK
			varchar tipo
			varchar subtipo
			datetime fecha
			text observacion
		}

		entrenamiento_aerobico {
			bigint id_aerobico PK
			bigint id_entrenamiento FK
			decimal distancia_km
			time duracion
			decimal ritmo_promedio
			int calorias
		}

		entrenamiento_fuerza {
			bigint id_fuerza PK
			bigint id_entrenamiento FK
			varchar musculo_principal
			text rutina
		}

		ejercicio {
			bigint id_ejercicio PK
			bigint id_fuerza FK
			varchar nombre
			int series
			int repeticiones
			decimal peso_kg
		}

		usuario||--o{mensaje:"envia"
		usuario||--o{habito:"tiene"
		categoria_habito||--o{habito:"clasifica"
		habito||--o{registro_habito:"registra"
		usuario||--o{lectura:"realiza"
		libro||--o{lectura:"puede ser leído"
		lectura||--o{registro_lectura:"registra"
		usuario||--o{cuenta_bancaria:"posee"
		banco||--o{cuenta_bancaria:"ofrece"
		cuenta_bancaria||--o{transaccion_finanza:"realiza"
		usuario||--o{transaccion_finanza:"efectua"
		categoria_finanza||--o{transaccion_finanza:"clasifica"
		usuario||--o{entrenamiento:"realiza"
		entrenamiento||--||entrenamiento_aerobico:"detalle_aerobico"
		entrenamiento||--||entrenamiento_fuerza:"detalle_fuerza"
		entrenamiento_fuerza||--o{ejercicio:"contiene"
	```
