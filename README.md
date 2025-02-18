# Parrot Challenge

## Sobre el proyecto
Está desarrollado con:
- Python
- Django
- Django Rest Framework

## Desplegar en local el proyecto
Para hacer el despliegue de manera local del proyecto y no tener que realizar ninguna instalción, es necesrio Docker, si se tiene Docker instalado basta con ejecutar el siguiente comando en la ruta principal del proyecto
```
docker-compose --env-file .env.local -f docker-compose.local.yml up --build -d
```

La ruta de la api es http://127.0.0.1:8000/api/

Por defecto ya viene un superusuario generado

```
email: admin@admin.com
password: admin
```
Puedes hacer login con él para obtener tus JWT

## Reglas de negocio
- Existen 3 usuarios Admin, Waiter y Customer
    - Solo los usuarios Admin y Waiter pueden interactuar con el sistema
    - Solo los usuarios Admin pueden crear usuarios Waiter
    - A nivel de Django, los usuarios Admin son los `is_superuser` y los Mesesros son los `is_satff`
    - Los usuarios Admin tienen acceso a todos los endpoints
- Sobre las ordenes
    - Los productos se crean al momento de crear las órdenes
    - Si un producto ya existe, este es el que se toma, no se crea uno nuevo ni se actualiza
    - Si se pasa el mismo producto en el request, se toma el primero que se pasó
    - Se puede pasar un email del Customer para llevarle un registro de sus órdenes en caso de que en futuras iteraciones se llegue a requerir, es un campo opcional.

## Endpoits
Los endpoints disponibles son los siguientes:

- `POST` `/api/login/`
- `POST` `/api/token/refresh/`
- `POST` `/api/waiters/`
- `POST` `/api/orders/`
- `GET` `/api/orders/`
- `GET` `/api/reports/excel`

### `POST` `/api/login/`
Sirve para hacer login dentro de la plataforma, para cualquier usuario que pueda autenticarse

Ejemplo de entrada
```json
{
    "email": "email@email.com",
    "password": "password"
}
```
Ejemplo de respuesta
```json
{
    "refresh": "acces_refresh",
    "access": "access_token"
}
```
### `POST` `/api/token/refresh/`
Usando el refresh_token, te crea un nuevo access_token

Ejemplo de entrada
```json
{
    "refresh": "refresh_token"
}
```
Ejemplo de respuesta
```json
{
    "access": "access_token"
}
```
### `POST` `/api/waiters/`
Permite crear usuarios de tipo Mesero. Solamente los usuarios Admin pueden usar este endpoint, para ello necesitan pasar el JWT en los headers `Authorization: Bearer <ACCESS_TOKEN>`.

Ejemplo de entrada
```json
{
    "email": "waiter@user.com",
    "name": "Pedro Picapiedra",
    "password": "securepassword"
}
```
Ejemplo de respuesta
```json
{
    "id": 5,
    "name": "Pedro Picapiedra",
    "email": "waiter@user.com"
}
```
### `POST` `/api/orders/`

Permite crear ordenes, solo los usuarios autorizados pueden crear ordenes (usuarios Admin y Mesero). Al momento de crear una orden, se crean los productos, si ya existe el producto, no se crea y se toma este.

- `customer_email` es opcional, si se pasa el campo, la orden se vincula a un Customer, sin embargo el Customer no tiene ninguna funcionalidad por ahora, es por si más adelante se desea realizar alguna nueva feature facilitarlo. Si no se pasa el campo no se crea la vinculación ni el registro en la tabla de Customer, solo se añade el nombre a la `customer_name` a la orden.
- `quantity` si no se pasa, por defecto toma el valor de 1.
- Si vienen productos con el mismo nombre, se suman en un solo registro.
- El precio del producto es el del primer producto que se pasa.
- `price_at_order`, como se observa en la respuesta de la orden no viene el campo `price`, sino `price_at_order`. Este es el precio del producto al momento de la creación de la orden, esto con fines de poder llevar un registro y que la modificación del `precio` del producto, no afecte las ordenes creadas.

Ejemplo de entrada
```json
{
    "customer_name": "Vilma Picapiedra",
    "customer_email": "vilma@picapiedra.com",
    "products": [
        {"name": "Pizza", "price": 199},
        {"name": "Coca Cola", "price": 20, "quantity": 2},
        {"name": "Coca Cola", "price": 50, "quantity": 2}
    ]
}
```
Ejemplo de respuesta
```json
{
    "id": 52,
    "waiter": "Pedro Picapiedra <waiter@user.com>",
    "customer_name": "Vilma Picapiedra",
    "products": [
        {
            "name": "Pizza",
            "quantity": 1,
            "price_at_order": "199.00"
        },
        {
            "name": "Coca Cola",
            "quantity": 4,
            "price_at_order": "20.00"
        }
    ],
    "total": 279.0,
    "created_at": "2025-02-18T06:50:38.521672Z"
}
```
### `GET` `/api/reports/excel`
Retorna el reporte de productos vendidos en un archivo excel. Los query parameters `start_date` y `end_date` son requeridos, también requiere del JWT. Tiene que ser Admin para acceder a la ruta.

### `GET` `/api/orders/`
Retorna las ordenes paginadas de 20 en 20, solo los usuarios Auténticados (Waiter y Admin) pueden verlas. Requiere JWT


## Para probar
Si tienes postman, puedes descargar esta colección que ya tiene los endpoints declarados
[POSTMAN COLLECTION](https://luis-maciel.postman.co/workspace/Postman-API-Fundamentals-Studen~1f75330f-9725-4578-ab5e-b9ae4ca872af/request/40258957-c946cb6e-0af2-44cb-a531-fd633bc42ce5?action=share&creator=40258957&ctx=documentation)

