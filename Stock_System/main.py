"""
Este proyecto consiste en un sistema muuy básico de control de stock desarrollado en Python, 
que permite gestionar productos mediante operaciones como agregar, actualizar, eliminar y
listar artículos disponibles. Es funcional y sirve para practicar y aprender.
"""
class Procuto:
    def __init__(self, id, nombre, precio, cantidad):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    #para mostrar la información del producto de forma legible.
    def __str__(self):  
         return f'{self.nombre} (ID: {self.id}, Precio: {self.precio}, Cantidad: {self.cantidad})'
    

class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, producto):
        #comprobar si producto existe, y actualizar cantidad
        if producto.id in self.productos:
            print('Producto existente... Actualizando Stock')
            self.productos[producto.id].cantidad += producto.cantidad
        else:
            self.productos[producto.id] = producto
            print('Producto agregado al stock')

    def eliminar_producto(self, id):    #Elimina un producto por su id
        if id in self.productos:
            del self.productos[id]
            print(f'producto de ID {id} eliminado')
        else:
            print('no se encontro el producto.....')

    def actualizar_producto(self, id, cantidad, precio):    #Modifica la cantidad y el precio de un producto existente.
        if id in self.productos:
            self.productos[id].cantidad = cantidad
            self.productos[id].precio = precio
            print(f'cantidad y precio actulizado del producto ID {id}.')
        else:
            print('no se encontro el producto.....')
    
    def listar_productos(self): #Muestra todos los productos en el inventario.
        for producto in self.productos.values():
            print(producto)



inventario1 = Inventario()
#Creacion productos
producto1 = Procuto(id=1, nombre="leche", precio=1500, cantidad=320) 
producto2 = Procuto(id=2, nombre="jugos", precio=1800, cantidad=410)
producto3 = Procuto(id=3, nombre="avena", precio=3900, cantidad=160)
print(inventario1.productos)

#Agregar e imprimir producto 
inventario1.agregar_producto(producto1)
inventario1.agregar_producto(producto2)
inventario1.agregar_producto(producto3)
inventario1.listar_productos()

#Actualizar cantidad y precio de 1 producto
inventario1.actualizar_producto(id=3, cantidad=230, precio=3200)
inventario1.listar_productos()

#Eliminar 1 producto
inventario1.eliminar_producto(3)
print(inventario1.productos)

#Listar todos los productos
inventario1.listar_productos()


