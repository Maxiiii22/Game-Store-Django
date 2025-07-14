# 🕹️ Game Store - Sistema E-commerce en Django

**Game Store** es una plataforma e-commerce desarrollada con **Django**, que permite comprar videojuegos, consolas, celulares, relojes inteligentes y accesorios de PC. Incluye un sistema completo de carrito, pedidos, usuarios, retiro en tiendas físicas, direcciones de envío y control de stock.

---

## 🧰 Funcionalidades Principales

- 🧍 ** Gestión de Usuarios ("Aplicación Usuarios") **
  - Sistema de usuarios personalizado (`CustomUser`).
  - Asociación de usuarios con los modulos de Pedido, DireccionEnvio y Carrito.

- 🛒 **Carrito de Compras ("Aplicación Carrito") **
  - Permite agregar productos desde distintas categorías al carrito (videojuegos, consolas, celulares, relojes inteligentes y accesorios de PC).
  - Uso de `GenericForeignKey` para gestionar productos de diferentes modelos en una misma estructura.
  - Reserva de stock automática  mediante un modelo de `ReservaStock`.
  - Confirmación de pedidos con elección de envío o retiro en tienda.    

- 📦 **Sistema de Pedidos**
  - Los pedidos pueden tener estado (pendiente, enviado, cancelado, etc.).
  - Las reservas de stock se vinculan con el pedido para asegurar la disponibilidad.
  - Gestión de pedidos por usuario.
  - Confirmación de pedidos y vinculación con direcciones de envío o retiro por sucursal.

 - 📱 **Tienda ("Aplicación Tienda")**
  - Diversos modelos de productos: videojuegos, consolas, celulares, smartwatches y accesorios de PC.



- 🧩 **Modularidad del Código**
  - Separación clara por apps (`carrito`, `usuarios`, etc.).
  - Uso de `context_processors` para pasar datos globales como el total del carrito.

---

## 🧩 Apps del Proyecto

| App          | Propósito                                                                 |
|--------------|--------------------------------------------------------------------------|
| `usuarios`   | Usuarios personalizados, autenticación, datos extra                      |
| `carrito`    | Carrito, pedidos, direcciones, stock                                     |
| `tienda`     | Modelos para consolas, juegos, celulares, smartwatches y accesorios      |

---

## 🧠 Tecnologías Utilizadas

| Tecnología     | Descripción                                      |
|----------------|--------------------------------------------------|
| Django         | Framework backend principal                      |
| SQLite         | Base de datos por defecto para desarrollo        |
| HTML/CSS       | Interfaz de usuario con templates personalizados |
| Django ORM     | Mapear modelos como objetos en la base de datos  |

---

