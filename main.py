import sys

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt5 import uic

#CLASE PRODUCTO
class Producto:
                                                        #Tendrá nombre, precio y descripción
    def __init__(self, nombre, precio, description):
        self.nombre = nombre
        self.precio = precio
        self.description = description

                                                        #Modificamos el toString para que sólo nos devuelva el nombre
    def __str__(self):
        nombreProducto = self.nombre
        return nombreProducto


#ARRAYS QUE VAMOS A UTILIZAR:
listaProductos = []                 #para guardar los objetos de productos y trabajar con nuestro ListWidget
listaFactura = []                  #mostrará todos los productos en la factura desglosada


class TPVKebab(QMainWindow):

    def __init__(self):  #EN EL INIT VOY A DECLARAR LOS DIFERENTES COMPONENTES Y LOS ASOCIARÉ A LOS DIFERENTES MÉTODOS
        super().__init__()
        uic.loadUi("TPVKebab.ui", self)

        #BOTONES PARA LOS PLATOS
        self.kTernera.clicked.connect(self.guardarKTernera)
        self.kPollo.clicked.connect(self.guardarKPollo)
        self.kMixto.clicked.connect(self.guardarKMixto)
        self.dTernera.clicked.connect(self.guardarDTernera)
        self.dPollo.clicked.connect(self.guardarDPollo)
        self.dMixto.clicked.connect(self.guardarDMixto)
        self.lahmacun.clicked.connect(self.guardarLahmacun)
        self.patatas.clicked.connect(self.guardarPatatas)
        self.plato.clicked.connect(self.guardarPlato)

        #BOTÓN DE ELIMINAR
        self.deleteBtn.clicked.connect(self.eliminarProducto)

        #BOTÓN DE LIMPIAR PEDIDO
        self.limpiarPed.clicked.connect(self.limpiarPedido)

        # TIEMPO
        self.fechayhora.setDateTime(QDateTime.currentDateTime())

        #CALCULAR TOTAL
        self.btnOK.clicked.connect(self.mostrar_factura_kebab) #le paso al botón de OK el método para calcular el precio y
                                                               #ejecutar el diálogo con la factura

        self.lista.clicked.connect(self.cambiarDescripcion)






    #MESSAGE BOX PARA MOSTRAR LA FACTURA

    def mostrar_factura_kebab(total):
        # Crea un cuadro de diálogo de información
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Factura simplificada")

        # Crea el texto de la factura
        factura_texto = "Gracias por visitar nuestro restaurante. Aquí está su factura:\n\n"
        factura_texto += ("Total a pagar: " + total.calcIVA() + "€" + "\n")
        factura_texto += "Gracias por su compra. ¡Vuelve pronto!"

        # Establece el texto de la factura en el cuadro de diálogo
        msgBox.setText(factura_texto)

        # Agrega botones para cerrar el cuadro de diálogo
        msgBox.addButton(QMessageBox.Ok)
        infoButton = QPushButton("Desglose")
        msgBox.addButton(infoButton, QMessageBox.ActionRole)

        # Establece el botón predeterminado como "Aceptar"
        msgBox.setDefaultButton(infoButton)

        def mostrar_factura_desglosada():
            # CREAMOS EL SEGUNDO DIÁLOGO QUE SE MOSTRARÁ CUANDO MARQUEMOS EL BOTÓN DE DESGLOSE

            factura_desglosada = "Factura desglosada:\n\n"
            factura_desglosada += ("Productos que contiene el pedido: \n\n" + total.cargarFactura() + "\n\n")
            factura_desglosada += ("Precio final sin IVA: " + "{:.2f}".format(total.precioTotal()) + "€" + "\n")
            factura_desglosada += ("Importe total con IVA incluido: " + total.calcIVA() + "€" + "\n\n")
            factura_desglosada += "¡Que te aproveche!\n Gracias por seguir rindiendo culto al Kebab con nosotros."
            #Con el operador '+=' podemos organizar mejor nuestros strings si son largos a la hora de setearlos desde el código

            imprimir = QPushButton("Imprimir factura")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Factura desglosada")

            msg.setText(factura_desglosada)

            msg.addButton(imprimir, QMessageBox.ActionRole)
            msg.addButton(QMessageBox.Ok)
            msg.setDefaultButton(imprimir)

            imprimir.clicked.connect(lambda: imprimir_factura(factura_desglosada)) #CON EL LAMBDA CONECTO EL BOTÓN IMPRIMIR CON EL MÉTODO DE ABAJO
            returnValue = msg.exec_()

        # con este método imprimo la factura en un .txt
        def imprimir_factura(factura_desglosada):
            factura = open("factura.txt", "w")     # si no está creado, lo genera automáticamente, si ya existe lo sobrescribe
            factura.write(factura_desglosada)      # le pasamos el texto que se mostró en el diálogo
            factura.close()

        infoButton.clicked.connect(mostrar_factura_desglosada) # Cuando se presione el botón se llamará al método de arriba para abir el desglose de la factura
        returnValue = msgBox.exec_()



    #MÉTODOS PARA GUARDAR PRODUCTOS

    # Al no manejar bases de datos, sencillamente hacemos un método de creación de objeto que se adapte a cada botón,
    # con lo cual, cada uno llamará a uno de ellos para crear el producto correspondiente

    def guardarKTernera(self):
        producto = Producto("Kebab de Ternera", 3.30, "Kebab de Ternera sencillo con vegetales y dos salsas")
        listaProductos.append(producto)   # Añadimos el producto al arraylist
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)
                                                                          # añadimos el nombre del producto y su precio al ListWidget
                                                                          # OJO, AL LISTWIDGET LE AÑADIMOS UN STRING COMPUESTO POR CAMPOS DEL OBJETO, NO EL OBJETO ENTERO
                                                                          # Cuando se seleccione un botón se mostrará la descripción del producto creado

    def guardarKPollo(self):
        producto = Producto("Kebab de Pollo", 3.30, "Kebab de Pollo sencillo con vegetales y dos salsas")
        listaProductos.append(producto)
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)

    def guardarKMixto(self):
        producto = Producto("Kebab Mixto", 3.50, "Kebab de Ternera y Pollo sencillo con vegetales y dos salsas")
        listaProductos.append(producto)
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)

    def guardarDTernera(self):
        producto = Producto("Durum de Ternera", 3.30, "Durum de Ternera sencillo con vegetales y dos salsas")
        listaProductos.append(producto)
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)

    def guardarDPollo(self):
        producto = Producto("Durum de Pollo", 3.30, "Durum de Pollo sencillo con vegetales y dos salsas")
        listaProductos.append(producto)
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)

    def guardarDMixto(self):
        producto = Producto("Durum Mixto", 3.50, "Durum de Ternera y Pollo sencillo con vegetales y dos salsas")
        listaProductos.append(producto)
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)

    def guardarLahmacun(self):
        producto = Producto("Lahmacun", 4.30, "Lahmacun con legumbres, carne y dos salsas")
        listaProductos.append(producto)
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)

    def guardarPatatas(self):
        producto = Producto("Patatas", 2.20, "Ración de patatas con salsa roja y blanca")
        listaProductos.append(producto)
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)

    def guardarPlato(self):
        producto = Producto("Plato de patatas con carne", 4.50, "Palo de patatas con carne acompañado de salsa roja y blanca")
        listaProductos.append(producto)
        self.lista.addItem(producto.nombre + ", " + str(producto.precio))
        self.textDescription.setText("\n" + producto.description)


    #MÉTODO PARA ELIMINAR UN PRODUCTO DEL ARRAYLIST

    def eliminarProducto(self):
        # Con el método currentRow obetenemos el índice de la posición del ítem que seleccionamos en la lista
        # Abrimos una sentencia if else para que, si pulsamos el botón de eliminar sin tener la referencia del
        # índice nos muestre un mensaje de error.

        if(self.lista.currentRow() >= 0):    # si el índice es igual o mayor a 0 (lo que quiere decir que tenemos un producto seleccionado)...
            #print(self.lista.currentRow())
            listaProductos.pop(self.lista.currentRow())
            self.lista.takeItem(self.lista.currentRow())
            self.textDescription.setText("")
            self.cambiarDescripcion()        # actualizo el LineEdit que contiene las descripciones

            # Como los objetos los añado en el mismo orden tanto en el arraylist como en el listwidget,
            # tienen el mismo índice, por lo tanto puedo utilizar currentRow() para eliminarlos
            # IMPORTANTE: Primero se elimina el objeto del arraylist, después se elimina la tupla del listwidget, si no, podemos generar conflictos

        else:                                # si por el contrario, currentRow() nos devuelve -1 (detectamos que no hay ningún producto seleccionado)...
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning!")
            msgBox.setText("Para eliminar un producto del pedido primero debes seleccionarlo")
            msgBox.addButton(QMessageBox.Ok)
            msgBox.exec()


    # MÉTODO PARA LIMPIAR EL LISTWIDGET Y EL ARRAYLIST
    def limpiarPedido(self):
        listaProductos.clear()
        self.lista.clear()
        self.textEditCalcPantalla.setText("")
        self.textDescription.setText("")

    # MÉTODO PARA SUMAR LOS PRECIOS
    def precioTotal(self):
        precio = 0.00
        for i in listaProductos:                   # recorremos el arraylist
            producto = i
            precio = precio + producto.precio      # en cada vuelta sumamos el precio del producto con el del siguiente
        return precio

    # PARA CALCULAR EL PRECIO FINAL CON EL IVA
    def calcIVA(self):
        iva = (self.precioTotal() * 0.21)
        precioFinal = "{:.2f}".format((self.precioTotal() + iva))   # el format nos permite hacer que nuestro valor float devuelva sólo dos decimales
        self.textEditCalcPantalla.setText("\n" + " " + precioFinal) # seteamos el LineEdit de debajo del listWidget con el precio final
        return precioFinal

    # MÉTODO PARA GENERAR EL ALBARÁN CON LOS PRODUCTOS DEL PEDIDO
    def cargarFactura(self):
        for Producto in listaProductos:
            listaFactura.append(Producto.nombre + "  " + "{:.2f}".format(Producto.precio))  # por cada producto del arraylist, imprime su nombre y su precio
        listaFactura.sort() #ordénalo
        #devoldemos el array toString
        return listaFactura.__str__()


    #MÉTODO PARA CAMBIAR LA DESCRIPCIÓN QUE SALE EN EL LINE EDIT PULSANDO EN EL LISTWIDGET
    def cambiarDescripcion(self):
        if (self.lista.currentRow() >= 0):
            producto = listaProductos[self.lista.currentRow()]             # creo un objeto que sirva de referencia a través del índice de la lista
            self.textDescription.setText("\n" + producto.description)      # muestro la descripción de ese objeto para la lista


# este if es necesario para que pyqt5 se inicie correctamente
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = TPVKebab()
    GUI.show()
    sys.exit(app.exec_())



