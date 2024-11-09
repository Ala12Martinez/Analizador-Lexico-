import re
import tkinter as tk
from tkinter import filedialog, Text

# Definición de los patrones para cada tipo de token
TOKENS = {
    'DELIMITADOR_INICIO': r'\[\[',
    'DELIMITADOR_FIN': r'\]\]',
    'TIPO_GRANDE': r'\$\w+',
    'TIPO_REAL': r'%\w+',
    'TIPO_LETRA': r'@\w+',
    'TIPO_LETRAS': r'@@\w+',
    'TIPO_VF': r'#\w+',
    'OPERADOR_MAT': r'[+\-*/%]',
    'OPERADOR_LOGICO': r'<>|=|>|<|>=|<=',
    'PALABRA_CLAVE': r'\b(FUNCION|OUTPUT|INPUT|MIENTRAS|CICLOF)\b',
    'IDENTIFICADOR': r'\b[A-Za-z_][A-Za-z0-9_]*\b',
    'NUMERO': r'\b\d+(\.\d+)?\b',
}

# Función para tokenizar el archivo
def tokenizar(codigo):
    tokens = []
    errores = []
    lineas = codigo.splitlines()
    
    for numero_linea, linea in enumerate(lineas, start=1):
        for tipo, patron in TOKENS.items():
            for coincidencia in re.finditer(patron, linea):
                tokens.append((tipo, coincidencia.group(), numero_linea))
                
        # Detectar errores (palabras no reconocidas)
        resto = re.sub('|'.join(TOKENS.values()), '', linea).strip()
        if resto:
            errores.append((resto, numero_linea))
    
    return tokens, errores
def mostrar_resultados(tokens, errores):
    # Crear la ventana
    ventana = tk.Tk()
    ventana.title("Analizador Léxico Brake++")
    
    # Mostrar tokens
    tk.Label(ventana, text="Tokens Encontrados:").pack()
    text_tokens = Text(ventana, height=10, width=50)
    for tipo, valor, linea in tokens:
        text_tokens.insert(tk.END, f"Línea {linea}: {tipo} -> {valor}\n")
    text_tokens.pack()

    # Mostrar errores
    tk.Label(ventana, text="Errores Encontrados:").pack()
    text_errores = Text(ventana, height=10, width=50)
    for valor, linea in errores:
        text_errores.insert(tk.END, f"Línea {linea}: Error -> {valor}\n")
    text_errores.pack()

    ventana.mainloop()

# Función para cargar el archivo y ejecutar el análisis
def cargar_archivo():
    archivo_path = filedialog.askopenfilename()
    if archivo_path:
        with open(archivo_path, 'r') as archivo:
            codigo = archivo.read()
        tokens, errores = tokenizar(codigo)
        mostrar_resultados(tokens, errores)

# Interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico de Brake++")
tk.Button(root, text="Cargar Archivo", command=cargar_archivo).pack()
root.mainloop()
