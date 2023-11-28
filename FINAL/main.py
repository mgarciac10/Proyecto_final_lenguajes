import tkinter as tk
import re
from AnalizadorLexicografico import AnalizadorLexicografico

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorLexicografico(root)
    root.mainloop()