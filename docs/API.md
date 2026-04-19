# API Tracking WhatsApp

## Resumen

Esta API centraliza registros personales y operativos en varios dominios:

- autenticación
- usuarios
- finanzas
- entrenamientos
- catálogo
- compras
- nutrición
- lecturas

La aplicación expone documentación interactiva en:

- `/docs`
- `/redoc`

Este archivo está pensado para ser más fácil de leer por una persona y también más fácil de parsear por una IA.

## Estado de esta documentación

Fuentes usadas para construir este documento:

- `docs/api.json`: snapshot OpenAPI existente del proyecto
- `app/routes/**`: fuente de verdad más actual sobre endpoints, permisos y comportamiento
- `app/schemas/**`: fuente de verdad sobre payloads de entrada y salida

Nota importante:

- `docs/api.json` no refleja todavía todos los módulos nuevos (`catalogo`, `compras`, `nutricion`).
- cuando exista diferencia entre este archivo y `docs/api.json`, prevalece el código en `app/routes` y `app/schemas`.

## Base URL

Prefijo principal de la API:

```txt
/api
```

Autenticación:

```txt
/auth
```

Ejemplos:

```txt
GET /api/usuarios/perfil
POST /auth/register
POST /auth/jwt/login
```

## Autenticación

La API usa JWT con `fastapi-users`.

### Flujo base

1. Registrar usuario con `POST /auth/register`
2. Iniciar sesión con `POST /auth/jwt/login`
3. Usar el token en el header `Authorization`

Header esperado:

```http
Authorization: Bearer <token>
```

### Endpoints de auth

#### `POST /auth/register`
Crea un usuario de autenticación y, según la lógica del proyecto, da soporte al perfil de usuario de la app.

Payload base:

```json
{
  "email": "tu-correo@gmail.com",
  "password": "TuClave123",
  "username": "tu_usuario",
  "nombre": "TuNombre",
  "apellido": "TuApellido",
  "telefono": "56912345678"
}
```

Campos esperados:

- `email`: correo válido
- `password`: entre 6 y 20 caracteres
- `username`: máximo 20 caracteres
- `nombre`: máximo 20 caracteres
- `apellido`: máximo 20 caracteres
- `telefono`: máximo 11 caracteres

#### `POST /auth/jwt/login`
Inicia sesión y devuelve el token JWT.

#### Endpoints adicionales de auth
`fastapi-users` suele exponer también rutas auxiliares del router JWT, dependiendo de la configuración activa del paquete.

## Convenciones globales

### Formato general

- casi todos los recursos usan esquemas `Create`, `Patch/Edit` y `Response`
- las respuestas suelen venir serializadas con `from_attributes=True`
- la mayoría de los `DELETE` responden `204 No Content`
- los errores comunes usan `404`, `409`, `400` y `422`

### Permisos

Hay 3 patrones principales:

- `current_user`: cualquier usuario autenticado
- `current_superuser`: solo administrador
- ownership: el usuario solo puede ver o modificar sus propios datos en compras, nutrición, finanzas y entrenamientos

### Reglas prácticas

- recursos maestros o catálogos suelen estar restringidos a `superuser` para crear, editar o eliminar
- recursos personales suelen asignarse automáticamente al usuario autenticado y no requieren mandar `id_usuario`
- algunos deletes son lógicos y no físicos, por ejemplo `producto` y varias entidades de usuario/finanzas

## Módulos

### 1. Usuarios
Prefijo: `/api/usuarios`

#### Endpoints

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/usuarios/perfil` | usuario | Obtiene el perfil del usuario autenticado |
| `PATCH` | `/api/usuarios/perfil` | usuario | Edita el perfil del usuario autenticado |
| `GET` | `/api/usuarios/` | superuser | Lista usuarios |
| `DELETE` | `/api/usuarios/{id_usuario}` | superuser | Desactiva usuario |
| `DELETE` | `/api/usuarios/{id_usuario}/permanente` | superuser | Elimina usuario definitivamente |

#### Payload útil

`PATCH /api/usuarios/perfil`

```json
{
  "username": "nuevo_usuario",
  "nombre": "NuevoNombre",
  "apellido": "NuevoApellido",
  "telefono": "56912345678",
  "email": "nuevo@mail.com"
}
```

#### Respuesta típica

```json
{
  "id_usuario": 1,
  "username": "fuco",
  "nombre": "Francisco",
  "apellido": "Arancibia",
  "telefono": "56912345678",
  "email": "correo@mail.com",
  "created_at": "2026-01-01T12:00:00"
}
```

### 2. Finanzas
Prefijo: `/api/finanzas`

Submódulos:

- `banco`
- `producto-financiero`
- `categoria`
- `cuentas`
- `movimientos`

#### Bancos

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/finanzas/banco/` | usuario | Lista bancos |
| `GET` | `/api/finanzas/banco/{id_banco}` | usuario | Obtiene banco por ID |
| `POST` | `/api/finanzas/banco/` | superuser | Crea banco |
| `PATCH` | `/api/finanzas/banco/{id_banco}` | superuser | Edita banco |
| `DELETE` | `/api/finanzas/banco/{id_banco}` | superuser | Elimina banco |

Payload base:

```json
{
  "nombre_banco": "Santander"
}
```

#### Productos financieros

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/finanzas/producto-financiero/` | usuario | Lista productos financieros, acepta `id_banco`, `q` e `incluir_inactivos` |
| `GET` | `/api/finanzas/producto-financiero/{id_producto_financiero}` | usuario | Obtiene producto financiero |
| `POST` | `/api/finanzas/producto-financiero/` | superuser | Crea producto financiero para un banco |
| `PATCH` | `/api/finanzas/producto-financiero/{id_producto_financiero}` | superuser | Edita producto financiero |
| `DELETE` | `/api/finanzas/producto-financiero/{id_producto_financiero}` | superuser | Desactiva producto si no tiene cuentas activas |

Payload base:

```json
{
  "id_banco": 1,
  "nombre_producto": "CuentaRUT",
  "descripcion": "Producto principal de BancoEstado"
}
```

#### Categorías financieras

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/finanzas/categoria/` | usuario | Lista categorías |
| `GET` | `/api/finanzas/categoria/{id_categoria}` | usuario | Obtiene categoría por ID |
| `POST` | `/api/finanzas/categoria/` | superuser | Crea categoría |
| `PATCH` | `/api/finanzas/categoria/{id_categoria}` | superuser | Edita categoría |
| `DELETE` | `/api/finanzas/categoria/{id_categoria}` | superuser | Elimina categoría |

Payload base:

```json
{
  "nombre": "comida"
}
```

#### Cuentas bancarias

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/finanzas/cuentas/` | usuario | Lista las cuentas del usuario |
| `GET` | `/api/finanzas/cuentas/{id_cuenta}` | usuario + ownership | Obtiene cuenta y movimientos |
| `POST` | `/api/finanzas/cuentas/` | usuario | Crea una cuenta del usuario autenticado |
| `PATCH` | `/api/finanzas/cuentas/{id_cuenta}` | usuario + ownership | Edita cuenta |
| `DELETE` | `/api/finanzas/cuentas/{id_cuenta}` | usuario + ownership | Desactiva cuenta |

Payload create:

```json
{
  "id_producto_financiero": 1,
  "nombre_cuenta": "Cuenta principal"
}
```

Campos importantes:

- `id_producto_financiero`
- `nombre_cuenta`
- el producto financiero define el banco y el tipo comercial real de la cuenta
- ejemplos válidos dependen del catálogo cargado para cada banco: `CuentaRUT`, `Cuenta Corriente`, `CMR`, etc.

#### Movimientos

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/finanzas/movimientos/` | usuario | Lista movimientos del usuario a partir de sus cuentas |
| `GET` | `/api/finanzas/movimientos/{id_movimiento}` | usuario + ownership por cuenta | Obtiene movimiento por ID |
| `POST` | `/api/finanzas/movimientos/` | usuario | Crea movimiento |
| `PATCH` | `/api/finanzas/movimientos/{id_movimiento}` | usuario + ownership por cuenta | Edita movimiento |

Payload create:

```json
{
  "id_categoria": 1,
  "id_cuenta": 1,
  "tipo_movimiento": "gasto",
  "tipo_gasto": "fijo",
  "monto": 3500,
  "descripcion": "Compra en supermercado",
  "created_at": "2026-01-03T18:37:18"
}
```

Enums usados:

- `tipo_movimiento`: `gasto`, `ingreso`
- `tipo_gasto`: `variable`, `fijo`

### 3. Entrenamientos
Prefijo: `/api/entrenamientos`

Submódulos:

- `ejercicios`
- `gimnasio`
- `fuerza`
- `series`

#### Ejercicios

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/entrenamientos/ejercicios/` | usuario | Lista ejercicios, acepta filtros `q` y `tipo` |
| `GET` | `/api/entrenamientos/ejercicios/musculos` | usuario | Lista los tipos musculares disponibles |
| `GET` | `/api/entrenamientos/ejercicios/{id_ejercicio}` | usuario | Obtiene un ejercicio |
| `POST` | `/api/entrenamientos/ejercicios/` | superuser | Crea ejercicio |
| `PATCH` | `/api/entrenamientos/ejercicios/{id_ejercicio}` | superuser | Edita ejercicio |
| `DELETE` | `/api/entrenamientos/ejercicios/{id_ejercicio}` | superuser | Elimina ejercicio si no tiene series asociadas |

Payload create:

```json
{
  "nombre": "Press banca plano",
  "tipo": "pecho",
  "url_video": "https://youtube.com/ejemplo"
}
```

Notas:

- `movimiento` ya no guarda `id_usuario` directo
- el ownership se resuelve por `id_cuenta`, porque cada cuenta pertenece a un único usuario
- cambiar de cuenta en un `PATCH` solo permite cuentas activas del mismo usuario autenticado

#### Gimnasios

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/entrenamientos/gimnasio/` | usuario | Lista gimnasios, acepta búsqueda `q` |
| `GET` | `/api/entrenamientos/gimnasio/{id_gimnasio}` | usuario | Detalle de gimnasio |
| `POST` | `/api/entrenamientos/gimnasio/` | superuser | Crea gimnasio |
| `PATCH` | `/api/entrenamientos/gimnasio/{id_gimnasio}` | superuser | Edita gimnasio |
| `DELETE` | `/api/entrenamientos/gimnasio/{id_gimnasio}` | superuser | Desactiva gimnasio |

Payload create:

```json
{
  "nombre_gimnasio": "Smart Fit Oeste",
  "nombre_cadena": "Smart Fit",
  "direccion": "Av. Siempre Viva 123",
  "comuna": "Nunoa",
  "latitud": -33.456,
  "longitud": -70.648
}
```

#### Entrenamiento de fuerza

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/entrenamientos/fuerza/` | usuario | Lista sesiones de fuerza del usuario |
| `GET` | `/api/entrenamientos/fuerza/activo` | usuario | Devuelve la sesión activa con series |
| `GET` | `/api/entrenamientos/fuerza/{id_entrenamiento_fuerza}` | usuario + ownership | Detalle de una sesión |
| `POST` | `/api/entrenamientos/fuerza/` | usuario | Inicia una sesión de fuerza |
| `PATCH` | `/api/entrenamientos/fuerza/activo/cerrar` | usuario | Cierra la sesión activa |

Payload create:

```json
{
  "observacion": "Pierna y hombro",
  "id_gimnasio": 1
}
```

#### Series de fuerza

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `POST` | `/api/entrenamientos/series/` | usuario | Agrega serie a la sesión activa |
| `PATCH` | `/api/entrenamientos/series/{id_fuerza_detalle}` | usuario + ownership activa | Edita serie |
| `DELETE` | `/api/entrenamientos/series/{id_fuerza_detalle}` | usuario + ownership activa | Elimina serie |

Payload create:

```json
{
  "id_ejercicio": 10,
  "es_calentamiento": false,
  "cantidad_peso": 60,
  "repeticiones": 8
}
```

### 4. Catálogo
Prefijo: `/api/catalogo`

Submódulos:

- `marca`
- `producto`

#### Marcas

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/catalogo/marca/` | usuario | Lista marcas |
| `GET` | `/api/catalogo/marca/{id_marca}` | usuario | Obtiene marca |
| `POST` | `/api/catalogo/marca/` | superuser | Crea marca |
| `PATCH` | `/api/catalogo/marca/{id_marca}` | superuser | Edita marca |
| `DELETE` | `/api/catalogo/marca/{id_marca}` | superuser | Elimina marca |

Payload create:

```json
{
  "nombre_marca": "Nestle"
}
```

#### Productos

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/catalogo/producto/` | usuario | Lista productos |
| `GET` | `/api/catalogo/producto/{id_producto}` | usuario | Obtiene producto |
| `POST` | `/api/catalogo/producto/` | superuser | Crea producto |
| `PATCH` | `/api/catalogo/producto/{id_producto}` | superuser | Edita producto |
| `DELETE` | `/api/catalogo/producto/{id_producto}` | superuser | Desactiva producto |

Payload create:

```json
{
  "id_marca": 1,
  "nombre_producto": "Yogurt protein",
  "codigo_barra": "7801234567890",
  "categoria": "Lacteos",
  "subcategoria": "Yogurt",
  "sabor": "Frutilla",
  "formato": "Botella",
  "contenido_neto": 350,
  "unidad_contenido": "ml",
  "activo": true
}
```

Notas:

- `codigo_barra` es único
- `DELETE` marca el producto como inactivo, no lo borra físicamente

### 5. Compras
Prefijo: `/api/compras`

Submódulos:

- `cadena`
- `local`
- `compra`
- `compra-detalle`

#### Cadenas

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/compras/cadena/` | usuario | Lista cadenas |
| `GET` | `/api/compras/cadena/{id_cadena}` | usuario | Obtiene cadena |
| `POST` | `/api/compras/cadena/` | superuser | Crea cadena |
| `PATCH` | `/api/compras/cadena/{id_cadena}` | superuser | Edita cadena |
| `DELETE` | `/api/compras/cadena/{id_cadena}` | superuser | Elimina cadena |

Payload create:

```json
{
  "nombre_cadena": "Lider"
}
```

#### Locales

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/compras/local/` | usuario | Lista locales |
| `GET` | `/api/compras/local/{id_local}` | usuario | Obtiene local |
| `POST` | `/api/compras/local/` | superuser | Crea local |
| `PATCH` | `/api/compras/local/{id_local}` | superuser | Edita local |
| `DELETE` | `/api/compras/local/{id_local}` | superuser | Elimina local |

Payload create:

```json
{
  "id_cadena": 1,
  "nombre_local": "Lider Nunoa",
  "latitud": -33.456,
  "longitud": -70.648,
  "direccion": "Av. Ejemplo 123"
}
```

#### Compras

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/compras/compra/` | usuario | Lista compras del usuario |
| `GET` | `/api/compras/compra/{id_compra}` | usuario + ownership | Obtiene compra |
| `POST` | `/api/compras/compra/` | usuario | Crea compra asociada al usuario autenticado |
| `PATCH` | `/api/compras/compra/{id_compra}` | usuario + ownership | Edita compra |
| `DELETE` | `/api/compras/compra/{id_compra}` | usuario + ownership | Elimina compra |

Payload create:

```json
{
  "id_local": 1,
  "fecha_compra": "2026-04-18T16:30:00"
}
```

#### Detalle de compra

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/compras/compra-detalle/?id_compra={id_compra}` | usuario + ownership | Lista detalles de una compra |
| `GET` | `/api/compras/compra-detalle/{id_detalle}` | usuario + ownership | Obtiene detalle por ID |
| `POST` | `/api/compras/compra-detalle/` | usuario + ownership | Crea detalle |
| `PATCH` | `/api/compras/compra-detalle/{id_detalle}` | usuario + ownership | Edita detalle |
| `DELETE` | `/api/compras/compra-detalle/{id_detalle}` | usuario + ownership | Elimina detalle |

Payload create:

```json
{
  "id_compra": 1,
  "id_producto": 10,
  "cantidad_comprada": 2,
  "unidad_compra": "unidad",
  "precio_unitario": 1490,
  "precio_total": 2980,
  "cantidad_unidades": 2
}
```

### 6. Nutrición
Prefijo: `/api/nutricion`

Submódulos:

- `consumo`
- `consumo-detalle`
- `meta`
- `peso`
- `tabla`

#### Consumos

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/nutricion/consumo/` | usuario | Lista consumos del usuario |
| `GET` | `/api/nutricion/consumo/{id_consumo}` | usuario + ownership | Obtiene consumo |
| `POST` | `/api/nutricion/consumo/` | usuario | Crea consumo |
| `PATCH` | `/api/nutricion/consumo/{id_consumo}` | usuario + ownership | Edita consumo |
| `DELETE` | `/api/nutricion/consumo/{id_consumo}` | usuario + ownership | Elimina consumo |

Payload create:

```json
{
  "fecha_consumo": "2026-04-18T14:00:00",
  "tipo_comida": "almuerzo",
  "observacion": "Comi fuera de casa"
}
```

#### Detalle de consumo

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/nutricion/consumo-detalle/?id_consumo={id_consumo}` | usuario + ownership | Lista detalle de un consumo |
| `GET` | `/api/nutricion/consumo-detalle/{id_consumo_detalle}` | usuario + ownership | Obtiene detalle |
| `POST` | `/api/nutricion/consumo-detalle/` | usuario + ownership | Crea detalle |
| `PATCH` | `/api/nutricion/consumo-detalle/{id_consumo_detalle}` | usuario + ownership | Edita detalle |
| `DELETE` | `/api/nutricion/consumo-detalle/{id_consumo_detalle}` | usuario + ownership | Elimina detalle |

Payload create:

```json
{
  "id_consumo": 1,
  "id_producto": 10,
  "cantidad_consumida": 1,
  "unidad_consumida": "porcion"
}
```

#### Metas nutricionales

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/nutricion/meta/` | usuario | Lista metas del usuario |
| `GET` | `/api/nutricion/meta/{id_meta}` | usuario + ownership | Obtiene meta |
| `POST` | `/api/nutricion/meta/` | usuario | Crea meta |
| `PATCH` | `/api/nutricion/meta/{id_meta}` | usuario + ownership | Edita meta |
| `DELETE` | `/api/nutricion/meta/{id_meta}` | usuario + ownership | Elimina meta |

Payload create:

```json
{
  "fecha_inicio": "2026-04-18",
  "fecha_fin": "2026-05-18",
  "calorias_objetivo": 2200,
  "proteinas_objetivo": 160,
  "carbohidratos_objetivo": 220,
  "grasas_objetivo": 70
}
```

#### Registro de peso

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/nutricion/peso/` | usuario | Lista registros de peso |
| `GET` | `/api/nutricion/peso/{id_peso}` | usuario + ownership | Obtiene registro |
| `POST` | `/api/nutricion/peso/` | usuario | Crea registro de peso |
| `PATCH` | `/api/nutricion/peso/{id_peso}` | usuario + ownership | Edita registro |
| `DELETE` | `/api/nutricion/peso/{id_peso}` | usuario + ownership | Elimina registro |

Payload create:

```json
{
  "fecha_registro": "2026-04-18",
  "peso_kg": 78.4
}
```

#### Tabla nutricional

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/nutricion/tabla/` | usuario | Lista tablas nutricionales |
| `GET` | `/api/nutricion/tabla/{id_tabla}` | usuario | Obtiene tabla |
| `POST` | `/api/nutricion/tabla/` | superuser | Crea tabla nutricional |
| `PATCH` | `/api/nutricion/tabla/{id_tabla}` | superuser | Edita tabla nutricional |
| `DELETE` | `/api/nutricion/tabla/{id_tabla}` | superuser | Elimina tabla nutricional |

Payload create:

```json
{
  "id_producto": 10,
  "porcion_cantidad": 30,
  "porcion_unidad": "g",
  "calorias": 120,
  "proteinas": 24,
  "carbohidratos": 3,
  "grasas": 1,
  "azucares": 2,
  "sodio": 80,
  "fibra": 0
}
```

### 7. Lecturas
Prefijo: `/api/lecturas`

Estado actual del módulo:

- existen routers base para `libros` y `registro`
- hoy actúan más como estructura del módulo que como API funcional completa
- no se observan endpoints implementados dentro de esos routers en el código actual

Rutas base del módulo:

- `/api/lecturas/libros`
- `/api/lecturas/registro`

## Payloads de referencia por recurso

Esta sección resume los cuerpos más comunes para IA y automatizaciones.

### Auth register

```json
{
  "email": "user@mail.com",
  "password": "Secret123",
  "username": "usuario",
  "nombre": "Nombre",
  "apellido": "Apellido",
  "telefono": "56912345678"
}
```

### Usuario patch

```json
{
  "username": "nuevo_user",
  "nombre": "Nuevo",
  "apellido": "Nombre",
  "telefono": "56912345678",
  "email": "nuevo@mail.com"
}
```

### Cuenta create

```json
{
  "id_producto_financiero": 1,
  "nombre_cuenta": "Cuenta sueldo"
}
```

### Producto financiero create

```json
{
  "id_banco": 1,
  "nombre_producto": "CMR",
  "descripcion": "Tarjeta y linea comercial de Falabella"
}
```

### Movimiento create

```json
{
  "id_categoria": 1,
  "id_cuenta": 1,
  "tipo_movimiento": "gasto",
  "tipo_gasto": "variable",
  "monto": 15990,
  "descripcion": "Compra farmacia"
}
```

### Gimnasio create

```json
{
  "nombre_gimnasio": "Energy",
  "nombre_cadena": "Energy Club",
  "direccion": "Calle 123",
  "comuna": "Providencia",
  "latitud": -33.42,
  "longitud": -70.61
}
```

### Fuerza create

```json
{
  "observacion": "Pecho y triceps",
  "id_gimnasio": 1
}
```

### Serie fuerza create

```json
{
  "id_ejercicio": 4,
  "es_calentamiento": false,
  "cantidad_peso": 80,
  "repeticiones": 6
}
```

### Ejercicio create

```json
{
  "nombre": "Remo con barra",
  "tipo": "espalda",
  "url_video": "https://youtube.com/ejemplo"
}
```

### Marca create

```json
{
  "nombre_marca": "Soprole"
}
```

### Producto create

```json
{
  "id_marca": 1,
  "nombre_producto": "Leche protein",
  "codigo_barra": "7801111111111",
  "categoria": "Lacteos",
  "subcategoria": "Leche",
  "sabor": "Chocolate",
  "formato": "Caja",
  "contenido_neto": 330,
  "unidad_contenido": "ml",
  "activo": true
}
```

### Compra create

```json
{
  "id_local": 1,
  "fecha_compra": "2026-04-18T10:15:00"
}
```

### Compra detalle create

```json
{
  "id_compra": 1,
  "id_producto": 5,
  "cantidad_comprada": 1,
  "unidad_compra": "unidad",
  "precio_unitario": 2390,
  "precio_total": 2390,
  "cantidad_unidades": 1
}
```

### Consumo create

```json
{
  "fecha_consumo": "2026-04-18T13:00:00",
  "tipo_comida": "desayuno",
  "observacion": "Rapido antes de salir"
}
```

### Consumo detalle create

```json
{
  "id_consumo": 1,
  "id_producto": 5,
  "cantidad_consumida": 1,
  "unidad_consumida": "unidad"
}
```

### Meta nutricional create

```json
{
  "fecha_inicio": "2026-04-18",
  "fecha_fin": "2026-06-18",
  "calorias_objetivo": 2400,
  "proteinas_objetivo": 180,
  "carbohidratos_objetivo": 250,
  "grasas_objetivo": 70
}
```

### Peso usuario create

```json
{
  "fecha_registro": "2026-04-18",
  "peso_kg": 79.3
}
```

### Tabla nutricional create

```json
{
  "id_producto": 5,
  "porcion_cantidad": 30,
  "porcion_unidad": "g",
  "calorias": 120,
  "proteinas": 25,
  "carbohidratos": 2,
  "grasas": 1,
  "azucares": 1,
  "sodio": 90,
  "fibra": 0
}
```

## Respuestas y errores comunes

### Códigos frecuentes

- `200 OK`: lectura o actualización exitosa
- `201 Created`: creación exitosa
- `204 No Content`: eliminación o desactivación exitosa
- `400 Bad Request`: payload vacío o inválido para la operación
- `401 Unauthorized`: falta token o es inválido
- `403 Forbidden`: el usuario no tiene permisos suficientes
- `404 Not Found`: recurso no existe o no pertenece al usuario
- `409 Conflict`: duplicado o regla de negocio violada
- `422 Unprocessable Entity`: validación de esquema falló

### Ejemplo de error

```json
{
  "detail": "Producto no encontrado"
}
```

## Notas para integraciones con IA

Sugerencias para agentes o automatizaciones:

- asumir que todos los recursos personales usan ownership, incluso si el `id` existe
- no enviar `id_usuario` en compras, consumos, metas, peso, cuentas o movimientos cuando la API lo calcula desde el token
- tratar `DELETE` de `producto`, `usuario` y algunas entidades financieras como desactivación lógica cuando el modelo lo indique
- usar `PATCH` solo con los campos que realmente cambian
- verificar duplicados antes de crear si el flujo depende de `codigo_barra`, `nombre_marca`, `nombre_cadena`, `nombre_banco`, `nombre_cuenta` o `username`

## Mapa rápido de prefijos

```txt
/auth
/api/usuarios
/api/finanzas
/api/entrenamientos
/api/catalogo
/api/compras
/api/nutricion
/api/lecturas
```

## Archivos fuente relacionados

- `app/main.py`
- `app/routes/__init__.py`
- `app/auth/routes.py`
- `app/routes/**`
- `app/schemas/**`
- `docs/api.json`

