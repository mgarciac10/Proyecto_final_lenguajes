import tkinter as tk
import re
from pathlib import Path


class AnalizadorLexicografico:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Lexicográfico")
        self.root.geometry("400x400")

        self.configurar_interfaz()

        self.palabras_permitidas = self.cargar_palabras_permitidas()

        self.diccionario_reemplazo = {
            ":)": "003-feliz.png",
            ":(": "009-triste.png",
            ":D": "005-sonriente.png",
            ";)": "018-guino.png",
            ":p": "023-cabeza-alienigena-1.png",
            "xD": "058-riendo.png",
            ":-)": "003-feliz.png",
            ":-(": "009-triste.png",
            "(y)": "031-me-gusta-1.png",
            "(n)": "028-pulgares-abajo.png",
            "<3": "001-emoji.png",
            "\\m/": "039-orar.png",
            ":-0": "004-conmocionado.png",
            ":0": "004-conmocionado.png",
            ":-|": "008-confuso.png",
            ":|": "008-confuso.png",
            ":*": "050-enamorado.png",
            ">:(": "051-enojado-2.png",
            "^^": "003-feliz.png",
            ":-]": "010-risa.png",
            ":3": "062-perro-2.png",
        }
        self.imagenes_emoticones = self.cargar_imagenes_emoticones()

    def configurar_interfaz(self):
        self.texto1 = tk.Label(self.root, text="Introduce la cadena de texto:")
        self.texto1.pack()

        self.input_text = tk.Text(self.root, height=3, width=40)
        self.input_text.pack()

        self.boton1 = tk.Button(self.root, text="Analizar", command=self.analizar_texto)
        self.boton1.pack()

        self.texto2 = tk.Label(self.root, text="Palabras:")
        self.texto2.pack()

        self.texto_resul = tk.Text(self.root, height=3, width=40, state=tk.DISABLED)
        self.texto_resul.pack()

        self.texto3 = tk.Label(self.root, text="Emoticones:")
        self.texto3.pack()

        self.imagen_e = tk.Label(self.root)
        self.imagen_e.pack()

        self.frame_emoticones = tk.Frame(self.root, height=50, width=400)
        self.frame_emoticones.pack()

        self.textosalida = tk.Label(self.root, text="Salida:")
        self.textosalida.pack()

        self.master_frame = tk.Frame(width=400)
        self.master_frame.pack()

    def contador_palabras(self, palabras_espanol):
        cantidad_palabras = str(len(palabras_espanol))
        return cantidad_palabras

    def contador_emoticones(self, emoticones):
        cantidad_emoticones = str(len(emoticones))
        return cantidad_emoticones

    def cargar_imagenes_emoticones(self):
        carpeta_emoticones = Path("C:/Users/user/Desktop/Universidad/Semestre 2/Programming Languages/FINAL/png")

        imagenes_emoticones = {}

        for nombre_emoticono, archivo_imagen in self.diccionario_reemplazo.items():
            ruta_imagen = carpeta_emoticones / archivo_imagen
            if ruta_imagen.is_file():
                imagen_emoticono = tk.PhotoImage(file=ruta_imagen)
                imagenes_emoticones[nombre_emoticono] = imagen_emoticono

        return imagenes_emoticones

    def cargar_palabras_permitidas(self):
        carpeta_letras = Path("C:/Users/user/Desktop/Universidad/Semestre 2/Programming Languages/FINAL/dics")

        palabras_permitidas = set()

        for letra in "abcdefghijklmnñopqrstuvwxyz":
            archivo_letra = carpeta_letras / f"{letra}.txt"

            if archivo_letra.is_file():
                with open(archivo_letra, "r", encoding="utf-8") as archivo:
                    palabras_letra = archivo.read().splitlines()
                    for palabra in palabras_letra:
                        palabras_permitidas.update(palabra.split(', '))

        return palabras_permitidas

    def mostrar_emoticones(self, emoticones):
        for widget in self.frame_emoticones.winfo_children():
            widget.destroy()

        for emoticon in emoticones:
            if emoticon in self.diccionario_reemplazo and emoticon in self.imagenes_emoticones:
                imagen_emoticono = self.imagenes_emoticones[emoticon]
                imagen_emoticono = imagen_emoticono.subsample(10, 10)

                etiqueta_emoticono = tk.Label(self.frame_emoticones, image=imagen_emoticono)
                etiqueta_emoticono.image = imagen_emoticono
                etiqueta_emoticono.pack(side=tk.LEFT)
            self.master_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def salida(self, lista, palabras_espanol, emoticones):
        self.master_frame.destroy()
        self.master_frame = tk.Frame(width=400)

        self.mostrar_emoticones(emoticones)

        self.textosalida.destroy()
        self.textosalida = tk.Label(text="Salida:")
        self.textosalida.pack()

        for elemento in lista:
            frame = tk.Frame(self.master_frame)

            if elemento in palabras_espanol:
                etiqueta_palabra = tk.Label(frame, text=elemento)
                etiqueta_palabra.pack(side=tk.LEFT)

            elif elemento in emoticones:
                if elemento in self.diccionario_reemplazo and elemento in self.imagenes_emoticones:
                    imagen_emoticono = self.imagenes_emoticones[elemento]
                    imagen_emoticono = imagen_emoticono.subsample(25, 25)

                    etiqueta_emoticono = tk.Label(frame, image=imagen_emoticono)
                    etiqueta_emoticono.image = imagen_emoticono
                    etiqueta_emoticono.pack(side=tk.LEFT)

            frame.pack(side=tk.LEFT)

        self.master_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def mod_lista(self, lista, emoticones):
        emoticon_pattern = f'({"|".join(map(re.escape, emoticones))})(?:-)?'

        nueva_lista = []
        for palabra in lista:
          if any(emoticon in palabra for emoticon in emoticones):
              partes = re.split(emoticon_pattern, palabra)
              nueva_lista.extend(partes)
          else:
              nueva_lista.append(palabra)

        nueva_lista = [item for item in nueva_lista if item]

        return nueva_lista

    def obtener_palabras(self, lista, emoticones):
        palabras = [palabra for palabra in lista if palabra.isalpha()]
        for i in range(len(palabras)):
            if palabras[i] in emoticones:
                del palabras[i]
            return palabras

    def analizar_texto(self):
        input_text = self.input_text.get("1.0", tk.END)
        lista = input_text.split()

        #Identifica los emoticones
        escaped_emoticons = [re.escape(emoticon) for emoticon in self.diccionario_reemplazo.keys()]
        emoticon_pattern = f'(?:{ "|".join(escaped_emoticons) })(?:-)?'
        emoticones = re.findall(emoticon_pattern, input_text)

        #Modifica la lista para que los emoticones sean elementos individuales
        lista = self.mod_lista(lista, emoticones)

        #Obtener palabras_espanol
        palabras_espanol = self.obtener_palabras(lista,emoticones)
        # Filtrar palabras permitidas
        palabras_espanol = [palabra for palabra in palabras_espanol if palabra.lower() in self.palabras_permitidas]

        # Muestra las palabras en el recuadro de palabras y la cantidad
        result_str = "Palabras" + "[" + self.contador_palabras(palabras_espanol) + "] :" + ", ".join(palabras_espanol)

        # Mostrar emoticones en el resultado
        emoticon_str = "Emoticones [" + self.contador_emoticones(emoticones) + "]"

        self.texto_resul.config(state=tk.NORMAL)
        self.texto_resul.delete("1.0", tk.END)
        self.texto_resul.insert(tk.END, result_str)
        self.texto_resul.config(state=tk.DISABLED)

        self.frame_emoticones.pack()

        self.texto3.destroy()
        self.texto3 = tk.Label(text=emoticon_str)
        self.texto3.pack()

        self.salida(lista, palabras_espanol, emoticones)