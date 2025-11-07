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

