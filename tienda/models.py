from django.db import models
from django.utils.text import slugify  # slugify nos ayudara a generar slug automaticamente.


# Create your models here.

###### Modelos relacionados/complementarios de los Juegos #######

class Genero(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Plataforma(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nombre

############################################################

class Empresa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Marca(models.Model):
    logo_marca = models.ImageField(upload_to='logos/', blank=True, null=True)
    nombre = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

class Modelo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.marca.nombre})"


class ProductoConImagen(models.Model): # Tabla donde estaran la Imagen Principal del producto
    imagen_principal = models.ImageField(upload_to='productos/imagenes/', blank=True, null=True)
    
    def __str__(self):
        return self.imagen_principal.name.split('/')[-1]  # Con .name.split('/')[-1]  solo mostramos el nombre del archivo y no toda su ruta .

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField() # Solo números enteros positivos
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    garantia = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    disponible = models.BooleanField(default=True)  
    modelo = models.ForeignKey(Modelo,on_delete=models.SET_NULL, null=True, blank=True)  # Relacionamos con el Modelo "Empresa".
    slug = models.SlugField(default="", null=False, unique=True,)  # Campo de tipo SLUG en donde le valor por defecto es "" , no podra ser NULL y no se debe repetir.
    
    class Meta:
        abstract = True  # El abstract = True significa que Django no va a crear una tabla para este modelo, pero los hijos sí van a heredar sus campos.
    
    @property  # @property convierte el método modelo_name en un atributo calculado, es decir, puedes acceder a él como si fuera un atributo normal del objeto. No necesitas llamar explícitamente al método desde tu vista; simplemente accedes a producto.modelo_name como si fuera un campo de modelo.
    def modelo_name(self):
        return self._meta.model_name           # Devuelve el nombre del modelo heredado en minusculas (como "consolas", "relojes", etc.) 
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):  # Cuando se guarde un registro
        if not self.slug:  # Y no tenga un Slug
            nombre = self.nombre.strip().lower()  # strip() remueve espacios accidentales y  lower() normaliza para que no te genere slugs distintos por mayúsculas.
            self.slug = slugify(nombre)  # Se genera uno automaticamente usando el nombre del producto.
        super().save(*args, **kwargs)  # Guardamos.



class Juegos(ProductoConImagen,Producto):  # Hereda los campos de el modelo/tabla "Producto" y de "ProductoConImagen".
    CLASIFICACIONES_EDAD = [
        ('E', 'Everyone (E)'),
        ('E10', 'Everyone 10+ (E10+)'),
        ('T', 'Teen (T)'),
        ('M', 'Mature (M)'),
        ('A', 'Adults Only (AO)'),
    ]
    FORMATO_CHOICES = [
        ('FISICO', 'Físico')
    ]
    
    generos = models.ManyToManyField("Genero")    # Relacion de Muchos a Muchos con el modelo "Géneros (Crea una tercera tabla JuegosXGenero)"
    plataforma = models.ForeignKey(Plataforma, on_delete=models.SET_NULL, null=True, blank=True) # Relacionamos con el Modelo "Plataformas" , donde este campo puede estar vacio o ser NULL .
    edicion = models.CharField(max_length=50,  default="Standar")
    tamaño_juego = models.CharField(max_length=30)
    clasificacion_edad = models.CharField(max_length=4, choices=CLASIFICACIONES_EDAD)
    formato = models.CharField(max_length=10, choices=FORMATO_CHOICES)
    
    def __str__(self):
        if self.stock == 0:
            return f"{self.nombre} - Sin stock"
        else:
            return f"{self.nombre} - Stock: {self.stock}"    
        
    def save(self, *args, **kwargs):  # Cuando se guarde un registro de un juego,
        if not self.slug:  # Y no tenga un Slug :
            nombre = self.nombre.strip().lower()  # strip() remueve espacios accidentales y  lower() normaliza para que no te genere slugs distintos por mayúsculas.
            edicion = self.edicion.strip().lower() if self.edicion else ""  # Se chequea si self.edicion existe (por si llega a estar vacío).
            self.slug = slugify(f"{nombre} {edicion}")  # Se genera uno automaticamente usando el nombre del producto ,la edicion y la plataforma.
        super().save(*args, **kwargs)  # Guardamos.
            

class ImagenSecundaria(models.Model):  # Tabla donde estaran las imagnes secundarias de los productos
    producto = models.ForeignKey(ProductoConImagen, on_delete=models.CASCADE, 
                                related_name="imagenes_secundarias") # El related_name='imagenes_secundarias' en el ForeignKey nos permite crear un nombre para poder acceder a todas las imágenes_secundarias que esten asociadas a una imagen_principa del modelo "ProductoConImagen".
                                                                    # Solo debemos hacer un for de esta manera por ejemplo : {% for img in consola.imagenes_secundarias.all %} 
                                                                    # Si no usamos "related_name" deberiamos hacerlo asi : {% for img in consola.ImagenSecundaria_set.all %}
    imagen = models.ImageField(upload_to='productos/imagenes_secundarias/')

    def __str__(self):
        nombre = str(self.producto)
        nombre_sin_ext = nombre.rsplit('.', 1)[0]  # Y con esto quitamos el tipo de archivo que es la imagen (.png.jpg,etc)
        return f"Imagen de {nombre_sin_ext}: {self.imagen.name.split('/')[-1]}"

class Consolas(ProductoConImagen,Producto):  # Hereda los campos de el modelo/tabla "Producto" y de "ProductoConImagen".
    edicion = models.CharField(max_length=50, blank=True, null=True)
    almacenamiento = models.CharField(max_length=50, blank=True, null=True)  
    cant_controles = models.CharField(max_length=50)  
    duracion_bateria = models.CharField(max_length=50, blank=True, null=True)
    peso = models.CharField(max_length=50)
    tamaño = models.CharField(max_length=50)
    juegos_incluidos = models.CharField(max_length=50, blank=True, null=True)


    def save(self, *args, **kwargs):  # Cuando se guarde un registro de una Consola
        if not self.slug:  # Y no tenga un Slug
            nombre = self.nombre.strip().lower()  # strip() remueve espacios accidentales y  lower() normaliza para que no te genere slugs distintos por mayúsculas.
            edicion = self.edicion.strip().lower()  
            self.slug = slugify(f"{nombre} {edicion}")  # Se genera un slug automaticamente usando el nombre del producto y la edicion.  (Play-5-Slim-Digital)
        super().save(*args, **kwargs)  # Guardamos.
    
    def __str__(self):
        if self.stock == 0:
            return f"{self.nombre} - Sin stock"
        else:
            return f"{self.nombre} - Stock: {self.stock}" 
    

class Celulares(ProductoConImagen,Producto):  # Hereda los campos de el modelo/tabla "Producto" y de "ProductoConImagen".
    sistema_operativo = models.CharField(max_length=50)
    almacenamiento = models.CharField(max_length=50)
    procesador = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    pantalla = models.CharField(max_length=100)  # Tamaño y tipo
    resolucion_cam_frontal = models.CharField(max_length=100)  
    resolucion_cam_trasera = models.CharField(max_length=100)  
    
    def __str__(self):
        if self.stock == 0:
            return f"{self.nombre} - Sin stock"
        else:
            return f"{self.nombre} - Stock: {self.stock}" 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nombre}")
        super().save(*args, **kwargs)


class RelojInteligentes(ProductoConImagen,Producto):  # Hereda los campos de el modelo/tabla "Producto" y de "ProductoConImagen".
    tipo_pantalla = models.CharField(max_length=50)
    tamaño_pantalla = models.CharField(max_length=50)
    duracion_bateria = models.CharField(max_length=100)
    conectividad = models.CharField(max_length=100)  # Ej: Bluetooth, Wi-Fi, LTE
    compatibilidad = models.CharField(max_length=100)  # Ej: Android, iOS
    sensores = models.TextField()
    
    def __str__(self):
        if self.stock == 0:
            return f"{self.nombre} - Sin stock"
        else:
            return f"{self.nombre} - Stock: {self.stock}" 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nombre}")
        super().save(*args, **kwargs)


# <----------------------------------------------------------------------->

class Conexion(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo

class AccesoriosPC(ProductoConImagen,Producto):  # Hereda los campos de el modelo/tabla "Producto" y de "ProductoConImagen".
    TIPO_ACCESORIO_CHOICES = [
        ('teclado', 'Teclado'),
        ('mouse', 'Mouse'),
        ('altavoz', 'Altavoz'),
        ('microfono', 'Micrófono'),
        ('auricular', 'Auricular'),
        ('camara', 'Cámara'),
    ]    
    tipo = models.CharField(max_length=30, choices=TIPO_ACCESORIO_CHOICES)
    conexiones = models.ManyToManyField(Conexion)  # Crea una tabla "accesoriosPcXConexion"
    rgb = models.BooleanField(default=False)
    compatibilidad = models.CharField(max_length=100)  
    microfono_integrado = models.BooleanField(blank=True, null=True)
    inalambrico = models.BooleanField(default=False)
    bateria = models.CharField(max_length=50, blank=True, null=True)
    tiempo_bateria = models.CharField(max_length=50, blank=True, null=True)  
    peso = models.CharField(max_length=50)
    dimensiones = models.CharField(max_length=100, blank=True, null=True)  # Ej: 30x10x5 cm
    resolucion = models.CharField(max_length=100, blank=True, null=True)  # Resolución de cámara o sensor óptico (ej: "1080p", "8000 DPI").

    def __str__(self):
        if self.stock == 0:
            return f"{self.nombre} - Sin stock"
        else:
            return f"{self.nombre} - Stock: {self.stock}" 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nombre}")
        super().save(*args, **kwargs)
        
