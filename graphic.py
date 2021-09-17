# importamos todos los modulos necesarios
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2TkAgg)
from matplotlib.figure import Figure
import tkinter as Tk

# Declaramos la clase "Ventana"
class Ventana():
    def __init__(self, master):
        # Asignamos las propiedades
        self.frame = Tk.Frame(master)
        
        # Definimos las figuras y sus posiciones en la ventana
        # Para ello utilizamos "Figure"
        self.f = Figure( figsize=(20, 9), dpi=80 )
        """
        Ahora definimos los graficos, en este caso solo uno, "ax0".
        Para ello utilizamos el métodos "add_axes" proporcionado por Figure.
        """
        self.ax0 = self.f.add_axes( (0.25, .25, .50, .50), axisbg=(.75,.75,.75), frameon=False)
        
        # Ahora, utilizamos los tipicos métodos de matplotlib
        # definimos las etiquetas de lo ejes X e Y.
        # Y con plot generamos el gráfico con los datos
        self.ax0.set_xlabel( 'Y' )
        self.ax0.set_ylabel( 'X' )
        self.ax0.plot([1,4,5,6,7,4,8])
        
        self.frame = Tk.Frame( root )
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
 
        # Creamos el canvas, que podemos decir que es el lugar en donde
        # se mostrara el gráfico
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.show()
     
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame )
        self.toolbar.pack()
        self.toolbar.update()
 
 
if __name__ == '__main__':
    # Ahora preparamos a la ventana
    root = Tk.Tk()
    app = Ventana(root)
    # Titulo de la ventana
    root.title( "Gráficos" )
    # Dimensiones de la ventana
    root.geometry("500x500")
    root.update()
    root.deiconify()
    root.mainloop()