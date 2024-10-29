import tkinter as tk
from tkinter import ttk

class TuringBinaria:
    def __init__(self):
        self.cinta = []
        self.pos_cabeza = 0
        self.estado_actual = 'q0'
        self.transiciones = self.iniciar_transiciones()
        
    def iniciar_transiciones(self):
        return {
            ('q0', '1'): ('q1', '1', 'R'),
            ('q1', '0'): ('q2', '0', 'R'),
            ('q2', '+'): ('q3', '+', 'R'),
            ('q3', '0'): ('q3', '0', 'R'),
            ('q3', '1'): ('q3', '1', 'R'),
            ('q3', '='): ('q4', '=', 'R'),
            ('q4', ''): ('q5', '', 'S') 
        }
        
    def paso(self):
        if self.pos_cabeza >= len(self.cinta):
            self.cinta.append('')
        
        simbolo_actual = self.cinta[self.pos_cabeza]
        clave_transicion = (self.estado_actual, simbolo_actual)
        
        if clave_transicion not in self.transiciones:
            return False
        
        nuevo_estado, simbolo_escribir, movimiento = self.transiciones[clave_transicion]
        self.cinta[self.pos_cabeza] = simbolo_escribir
        self.estado_actual = nuevo_estado
        
        if movimiento == 'R':
            self.pos_cabeza += 1
            
        return True
    
    def extraer_numeros(self):
        cinta_texto = ''.join(self.cinta)
        partes = cinta_texto.split('+')
        if len(partes) != 2:
            return None, None
            
        num1 = partes[0].strip()
        num2 = partes[1].split('=')[0].strip()
        return self.binario_a_decimal(num1), self.binario_a_decimal(num2)
    
    def binario_a_decimal(self, binario):
        try:
            return int(binario, 2)
        except ValueError:
            return None
    
    def calcular_suma(self):
        num1, num2 = self.extraer_numeros()
        if num1 is None or num2 is None:
            return None
        return bin(num1 + num2)[2:]  
    
    def ejecutar(self, cadena):
        self.cinta = list(cadena)
        self.pos_cabeza = 0
        self.estado_actual = 'q0'
        
        while self.paso():
            if self.estado_actual == 'q5':
                return True
                
        return False


class InterfazTuring:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora Binaria con Turing")
        self.ventana.geometry("500x250")
        self.ventana.configure(bg="#33334d")  

        self.maquina_turing = TuringBinaria()
        self.crear_elementos()
        
    def crear_elementos(self):
        self.var_entrada = tk.StringVar()
        
        marco_entrada = tk.Frame(self.ventana, bg="#33334d")
        marco_entrada.pack(pady=20)
        
        campo_entrada = tk.Entry(marco_entrada, textvariable=self.var_entrada, font=('Arial', 14), width=30, bg="#e6e6ff", fg="#33334d")
        campo_entrada.pack(side=tk.TOP, padx=10)
        
        boton_calcular = tk.Button(
            self.ventana, 
            text="Calcular Suma", 
            command=self.ejecutar_maquina, 
            font=('Arial', 14), 
            bg="#666699", 
            fg="#ffffff", 
            width=20, 
            height=2
        )
        boton_calcular.pack(pady=20)

        self.var_resultado = tk.StringVar()
        etiqueta_resultado = tk.Label(self.ventana, textvariable=self.var_resultado, font=('Arial', 12), bg="#33334d", fg="#ffffff")
        etiqueta_resultado.pack(pady=10)
    
    def ejecutar_maquina(self):
        cadena_entrada = self.var_entrada.get()
        if not cadena_entrada:
            self.var_resultado.set("Por favor ingrese una expresión binaria")
            return
            
        try:
            es_valido = self.maquina_turing.ejecutar(cadena_entrada)
            if es_valido:
                resultado = self.maquina_turing.calcular_suma()
                if resultado:
                    self.var_resultado.set(f"Resultado: {resultado} (binario) = {int(resultado, 2)} (decimal)")
                else:
                    self.var_resultado.set("Error al calcular la suma")
            else:
                self.var_resultado.set("Expresión binaria inválida")
                
        except Exception as e:
            self.var_resultado.set(f"Error: {str(e)}")

if __name__ == "__main__":
    app = InterfazTuring()
    app.ventana.mainloop()
