from django.db import models
from usuarios.models import CustomUser 

# Create your models here.

# -----------------------------------------------------------
from django.contrib.contenttypes.models import ContentType  
from django.contrib.contenttypes.fields import GenericForeignKey


class DireccionEnvio(models.Model):
    PROVINCIAS_CHOICES = [
        ("Buenos Aires", "Buenos Aires"),
        ("Ciudad Autónoma de Buenos Aires", "Ciudad Autónoma de Buenos Aires"),
        ("Catamarca", "Catamarca"),
        ("Chaco", "Chaco"),
        ("Chubut", "Chubut"),
        ("Córdoba", "Córdoba"),
        ("Corrientes", "Corrientes"),
        ("Entre Ríos", "Entre Ríos"),
        ("Formosa", "Formosa"),
        ("Jujuy", "Jujuy"),
        ("La Pampa", "La Pampa"),
        ("La Rioja", "La Rioja"),
        ("Mendoza", "Mendoza"),
        ("Misiones", "Misiones"),
        ("Neuquén", "Neuquén"),
        ("Río Negro", "Río Negro"),
        ("Salta", "Salta"),
        ("San Juan", "San Juan"),
        ("San Luis", "San Luis"),
        ("Santa Cruz", "Santa Cruz"),
        ("Santa Fe", "Santa Fe"),
        ("Santiago del Estero", "Santiago del Estero"),
        ("Tierra del Fuego", "Tierra del Fuego"),
        ("Tucumán", "Tucumán"),
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='direcciones_envio')
    direccion = models.CharField(max_length=255)
    numero_puerta = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100, choices=PROVINCIAS_CHOICES)
    codigo_postal = models.CharField(max_length=20)
    instrucciones_envio = models.TextField(blank=True, null=True)
    
    def getDireccion(self):
        return f"{self.direccion}, {self.ciudad}, {self.provincia} - CP: {self.codigo_postal}"

    def __str__(self):
        return f"Direccion del usuario {self.usuario.username}: (CP:{self.codigo_postal}) - {self.direccion}, {self.ciudad}, {self.provincia} | Datos extras: Numero puerta: {self.numero_puerta}, Instrucciones de envio: {self.instrucciones_envio}"

class Tiendas(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    horario_apertura = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    
    def getLocalRetiro(self):
        return f"{self.nombre} - Direccion: {self.direccion}) - Ubicacion: {self.ubicacion} - Ciudad: {self.ciudad} - Provincia: {self.provincia}"
    
    def __str__(self):
        return f"Tienda: {self.nombre} - Direccion: {self.direccion}) - Ubicacion: {self.ubicacion} - Horario apertura: {self.horario_apertura} - Ciudad: {self.ciudad} - Provincia: {self.provincia}"


class Carrito(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    creado = models.DateTimeField(auto_now_add=True)
    
    def total(self):
        return sum(linea.subtotal() for linea in self.lineas.all()) # Suma el subtotal de todas las líneas/LineaCarrito
    
    def __str__(self):
        return f"Carrito de: {self.usuario.username}, Total en carrito: $ { self.total()}"


class LineaCarrito(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE, related_name='lineas')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) 
    object_id = models.PositiveIntegerField()  
    producto = GenericForeignKey('content_type', 'object_id')  
    


    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad
    
    def __str__(self):
        return f"Producto del carrito de {self.carrito.usuario.username}: {self.producto.nombre} , Cantidad : {self.cantidad} , Subtotal: $ {self.subtotal()}"



class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]
    
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente") 
    metodo_envio = models.CharField(max_length=100, choices=[ ('envio_estandar', 'Envíar a domicilo'), ('retira_tienda', 'Retiro en tienda'), ], default='estandar')  
    direccion_envio = models.ForeignKey('DireccionEnvio', on_delete=models.SET_NULL, null=True, blank=True)
    retiro_local = models.ForeignKey('Tiendas', on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2) # Esto se refiere a que el total no puede terner mas de 10 digitos incuyendo los decimales es decir : 99.999.999,99 seria el max.

    
    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.username} - Total: ${self.total} - Estado: {self.estado}"


class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='lineasPedido', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return self.producto.precio * self.cantidad
    
    def __str__(self):
        return f"Linea del Pedido N°{self.pedido.id} del usuario {self.pedido.usuario.username}: - Producto: {self.producto.nombre} - Cantidad: {self.cantidad}"


class ReservaStock(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')
    cantidad = models.PositiveIntegerField()
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField()  # Por ejemplo, 15 minutos desde la creación

    def __str__(self):
        return f"Reserva de {self.cantidad} unidades de {self.producto.nombre} para {self.usuario.username}"
