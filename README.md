## 🚀 **Endpoints de la API de Usuarios**

| **Método** | **Endpoint** | **Descripción** | **JSON (Request)** | **JSON (Success Response)** |
|-------------|---------------|------------------|--------------------|-----------------------------|
| 🟢 **GET** | `/api/usuarios/` | Obtiene una lista de todos los usuarios. | — | ```json
[
  {
    "id": 1,
    "username": "fran",
    "email": "fran@test.com"
  },
  {
    "id": 2,
    "username": "ana",
    "email": "ana@test.com"
  }
]
``` |
| 🟢 **GET** | `/api/usuarios/{usuario_id}/` | Obtiene los detalles de un usuario específico. | — | ```json
{
  "id": 1,
  "username": "fran",
  "email": "fran@test.com"
}
``` |
| 🟡 **POST** | `/api/usuarios/crear/` | Crea un nuevo usuario.<br>*(La contraseña se hashea)* | ```json
{
  "username": "nuevo",
  "email": "nuevo@test.com",
  "password": "1234"
}
``` | ```json
{
  "mensaje": "Usuario creado con éxito",
  "id": 2
}
``` |
| 🔵 **PUT** | `/api/usuarios/actualizar/{usuario_id}/` | Actualiza **todos los campos** de un usuario. | ```json
{
  "username": "editado",
  "email": "editado@test.com",
  "password": "nueva123"
}
``` | ```json
{
  "mensaje": "Usuario actualizado con éxito"
}
``` |
| 🟣 **PATCH** | `/api/usuarios/actualizar_especifica/{usuario_id}/` | Actualiza **uno o más campos** de un usuario. | ```json
{
  "email": "solo@nuevoemail.com"
}
``` | ```json
{
  "mensaje": "Usuario actualizado con éxito"
}
``` |
| 🔴 **DELETE** | `/api/usuarios/borrar/{usuario_id}/` | Elimina físicamente un usuario de la base de datos. | — | ```json
{
  "mensaje": "Usuario eliminado (físicamente) con éxito"
}
``` |

---

### 💡 **Notas adicionales**
- 🔐 Las contraseñas se almacenan **hasheadas** por motivos de seguridad.  
- ✅ Todas las respuestas devuelven objetos **JSON** bien estructurados.  


## 🃏 **Endpoints de la API de Cartas**

| **Método** | **Endpoint** | **Descripción** | **JSON (Request)** | **JSON (Success Response)** |
|-------------|---------------|------------------|--------------------|-----------------------------|
| 🟢 **GET** | `/api/cartas/` | Obtiene una lista de **todas las cartas activas**.<br>⚙️ Las *stats* devueltas dependen de la posición. | — | ```json
[
{
  "id": 1,
  "nombre": "Messi",
  "posicion": "DC",
  "puntuacion_total": 94,
  "club": "Inter Miami",
  "liga": "MLS",
  "pais": "Argentina",
  "activo": true,
  "ritmo": 80,
  "tiro": 90,
  "pase": 91,
  "regate": 94,
  "defensa": 35,
  "fisico": 65,
  "salto": 11,
  "parada": 6,
  "saque": 15,
  "reflejos": 8,
  "velocidad_portero": 10,
  "posicionamiento_portero": 14
}
,
  {
  "id": 2,
  "nombre": "Ter Stegen",
  "posicion": "POR",
  "puntuacion_total": 90,
  "club": "FC Barcelona",
  "liga": "La Liga",
  "pais": "Alemania",
  "activo": true,
  "salto": 88,
  "parada": 90,
  "saque": 85,
  "reflejos": 91,
  "velocidad": 45,
  "posicionamiento": 88,
  "ritmo": 43,
  "tiro": 14,
  "pase": 29,
  "regate": 22,
  "defensa": 15,
  "fisico": 41
}

]
``` |
| 🟢 **GET** | `/api/cartas/{carta_id}/` | Obtiene los detalles de una **carta activa específica**.<br>Devuelve stats de campo o de portero según la posición. | — | ```json
{
  "id": 2,
  "nombre": "Ter Stegen",
  "posicion": "POR",
  "puntuacion_total": 90,
  "club": "FC Barcelona",
  "liga": "La Liga",
  "pais": "Alemania",
  "activo": true,
  "salto": 88,
  "parada": 90,
  "saque": 85,
  "reflejos": 91,
  "velocidad": 45,
  "posicionamiento": 88,
  "ritmo": 43,
  "tiro": 14,
  "pase": 29,
  "regate": 22,
  "defensa": 15,
  "fisico": 41
}
``` |
| 🟡 **POST** | `/api/cartas/crear/` | Crea una nueva carta.<br>⚙️ La `puntuacion_total` se **calcula automáticamente** según la posición. | **Ej. (Delantero):**```json
{
  "nombre": "Mbappé",
  "posicion": "DC",
  "club_id": 1,
  "pais_id": 1,
  "liga_id": 1,
  "ritmo": 97,
  "tiro": 90,
  "pase": 85,
  "regate": 94,
  "defensa": 40,
  "fisico": 80,
  "salto": 12,
  "parada": 6,
  "saque": 14,
  "reflejos": 8,
  "velocidad_portero": 10,
  "posicionamiento_portero": 11
}
**Ej. (Portero):**
{
  "nombre": "Courtois",
  "posicion": "POR",
  "club_id": 2,
  "pais_id": 3,
  "liga_id": 1,
  "salto": 85,
  "parada": 90,
  "saque": 78,
  "reflejos": 91,
  "velocidad": 50,
  "posicionamiento": 89,
  "ritmo": 45,
  "tiro": 13,
  "pase": 27,
  "regate": 21,
  "defensa": 11,
  "fisico": 43
}

``` | ```json
{
  "mensaje": "Carta creada con éxito",
  "id": 151
}
``` |
| 🔵 **PUT** | `/api/cartas/actualizar/{carta_id}/` | Actualiza **todos los campos** de una carta.<br>⚙️ Recalcula automáticamente la `puntuacion_total`. | ```json
{
  "nombre": "Mbappé",
  "posicion": "DC",
  "club_id": 1,
  "pais_id": 1,
  "liga_id": 1,
  "ritmo": 98,
  "tiro": 91,
  "pase": 86,
  "regate": 95,
  "defensa": 41,
  "fisico": 81,
  "salto": 10,
  "parada": 8,
  "saque": 15,
  "reflejos": 5,
  "velocidad": 11,
  "posicionamiento": 7
}
``` | ```json
{
  "mensaje": "Carta actualizada con éxito"
}
``` |
| 🟣 **PATCH** | `/api/cartas/actualizar_especifica/{carta_id}/` | Actualiza **uno o más campos** de una carta.<br>⚙️ También recalcula la `puntuacion_total`. | ```json
{
  "tiro": 92,
  "club_id": 2
}
``` | ```json
{
  "mensaje": "Carta actualizada con éxito"
}
``` |
| 🔴 **DELETE** | `/api/cartas/borrar/{carta_id}/` | Desactiva una carta (**borrado lógico**).<br>🧩 El campo `activo` se pone a `false`. | — | ```json
{
  "mensaje": "Carta desactivada con éxito"
}
``` |

---

### 💡 **Notas adicionales**
- 🧠 El campo `puntuacion_total` se **calcula automáticamente** en el servidor basándose en las estadísticas correspondientes a la `posicion`.
- ✅ Todas las respuestas se devuelven en formato **JSON**.  
- 🚫 El borrado es **lógico**, es decir, el campo `activo` se establece en `false` en lugar de eliminar el registro físicamente.  
