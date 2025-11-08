📘 Endpoints de la API

👤 USUARIOS
| Método     | Ruta                                                | Descripción                                      | Body | Auth |  Autor |
| :--------- | :-------------------------------------------------- | :----------------------------------------------- | :--: | :--: | :----: |
| **GET**    | `/usuarios/`                                        | Lista todos los usuarios.                        |   —  |   —  | Carlos |
| **GET**    | `/usuarios/<int:usuario_id>/`                       | Obtiene un usuario específico por su ID.         |   —  |   —  | Carlos |
| **POST**   | `/usuarios/crear/`                                  | Crea un nuevo usuario. (La contraseña se cifra). | JSON |   —  | Carlos |
| **PUT**    | `/usuarios/actualizar/<int:usuario_id>/`            | Actualiza todos los campos de un usuario.        | JSON |   —  | Carlos |
| **PATCH**  | `/usuarios/actualizar_especifica/<int:usuario_id>/` | Actualiza uno o más campos de un usuario.        | JSON |   —  | Carlos |
| **DELETE** | `/usuarios/borrar/<int:usuario_id>/`                | Borra (físicamente) un usuario.                  |   —  |   —  | Carlos |


🧩 CARTAS
| Método     | Ruta                                            | Descripción                                       | Body | Auth |  Autor |
| :--------- | :---------------------------------------------- | :------------------------------------------------ | :--: | :--: | :----: |
| **GET**    | `/cartas/`                                      | Lista todas las cartas.                           |   —  |   —  | Sergio |
| **GET**    | `/cartas/<int:carta_id>/`                       | Obtiene una carta específica.                     |   —  |   —  | Sergio |
| **POST**   | `/cartas/crear/`                                | Crea una nueva carta. (Calcula puntuación total). | JSON |   —  | Sergio |
| **PUT**    | `/cartas/actualizar/<int:carta_id>/`            | Actualiza todos los campos de una carta.          | JSON |   —  | Sergio |
| **PATCH**  | `/cartas/actualizar_especifica/<int:carta_id>/` | Actualiza uno o más campos de una carta.          | JSON |   —  | Sergio |
| **DELETE** | `/cartas/borrar/<int:carta_id>/`                | Borra (lógicamente) una carta (`activo=false`).   |   —  |   —  | Sergio |


🛡️ EQUIPOS
| Método     | Ruta                                     | Descripción                                                      | Body | Auth |      Autor      |
| :--------- | :--------------------------------------- | :--------------------------------------------------------------- | :--: | :--: | :-------------: |
| **POST**   | `/equipo/asignar/<int:usuario_id>/`      | Crea un equipo y le asigna una plantilla aleatoria (**Req3.1**). | JSON |   —  | Sergio y Carlos |
| **DELETE** | `/equipo/eliminar/<int:usuario_id>/`     | Borra el equipo de un usuario (**Req3**).                        |   —  |   —  |      Sergio     |
| **GET**    | `/equipo/consultar/<int:usuario_id>/`    | Consulta el equipo de un usuario y sus cartas (**Req6**).        |   —  |   —  |      Carlos     |
| **POST**   | `/equipos/<int:equipo_id>/anadir_carta/` | Añade una carta a un equipo (**Req7**).                          | JSON |   —  |      Carlos     |


- Ejemplo de crear_usuario (POST /api/usuarios/crear/)

{
    "username": "Pepe",
    "email": "pepe@ejemplo.com",
    "password": "Pepe1234",
    "nombre": "Pepe",
    "apellidos": "Rodriguez"
}


- Ejemplo de actualizar_usuario (PUT /api/usuarios/actualizar/<id>/)

{
    "username": "Pepe1",
    "email": "pepe1@ejemplo.com",
    "password": "Pepe1234",
    "nombre": "Pepe",
    "apellidos": "Rodriguez"
}

- Ejemplo de actualizar_campos_especificos_usuario (PATCH /api/usuarios/actualizar_especifica/<id>/

{
    "email": "soloelmail@nuevo.com"
}


- Ejemplo de crear_carta (Jugador de Campo) (POST /api/cartas/crear/)
  
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
    "fisico": 80
}

- Ejemplo de crear_carta (Portero) (POST /api/cartas/crear/)

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
    "posicionamiento": 89
}

- Ejemplo de actualizar_carta (PUT /api/cartas/actualizar/<id>/) La vista PUT espera todos los campos (los no relevantes se ponen a 30 por defecto).

{
    "nombre": "Mbappé Editado",
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
    "salto": 30,
    "parada": 30,
    "saque": 30,
    "reflejos": 30,
    "velocidad": 30,
    "posicionamiento": 30
}

- Ejemplo de actualizar_campos_especificos_carta (PATCH /api/cartas/actualizar_especifica/<id>/)

{
    "tiro": 99,
    "club_id": 5
}

- Ejemplo de asignar_equipo_a_usuario (POST api/equipo/asignar/<int:usuario_id>/ Solo necesita el nombre; el servidor rellena las cartas aleatoriamente.

{
    "nombre": "Real Vardrid"
}

- Ejemplo de anadir_carta_a_equipo (POST /api/equipos/<int:equipo_id>/anadir_carta/) Solo necesita el ID de la carta a añadir.

{
    "carta_id": 302
}



