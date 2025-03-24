import tkinter as tk
from tkinter import messagebox
from scraping_arxiv import get_arxiv_articles
from scraping_pubmed import get_pubmed_articles

# Función para cambiar de pantalla
def show_frame(frame):
    frame.tkraise()

# Función para ejecutar el scraping de arXiv
def run_scraping_arxiv():
    result = get_arxiv_articles()
    
    # Limpiar los widgets de texto
    text_result_cl.delete(1.0, tk.END)
    text_result_cv.delete(1.0, tk.END)
    
    # Mostrar los resultados de cs.CL en el primer widget
    for article in result["cs.CL"]:
        text_result_cl.insert(tk.END, f"DOI: {article[0]}\nTitle: {article[1]}\nAuthors: {article[2]}\nAbstract: {article[3]}\nSection: {article[4]}\nDate: {article[5]}\n\n")
    
    # Mostrar los resultados de cs.CV en el segundo widget
    for article in result["cs.CV"]:
        text_result_cv.insert(tk.END, f"DOI: {article[0]}\nTitle: {article[1]}\nAuthors: {article[2]}\nAbstract: {article[3]}\nSection: {article[4]}\nDate: {article[5]}\n\n")

# Función para ejecutar el scraping de PubMed
def run_scraping_pubmed():
    result = get_pubmed_articles()
    text_result_pubmed.delete(1.0, tk.END)
    for article in result:
        text_result_pubmed.insert(tk.END, f"DOI: {article[0]}\nTitle: {article[1]}\nAuthors: {article[2]}\nAbstract: {article[3]}\nJournal: {article[4]}\nDate: {article[5]}\n\n")

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Web Scraping")
root.geometry("800x620")

# Crear un contenedor para las pantallas
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Pantalla de inicio
frame_start = tk.Frame(container)
frame_arxiv = tk.Frame(container)
frame_pubmed = tk.Frame(container)

for frame in (frame_start, frame_arxiv, frame_pubmed):
    frame.grid(row=0, column=0, sticky="nsew")

# Configurar la pantalla de inicio
label_start = tk.Label(frame_start, text="Seleccione una opción")
label_start.pack(pady=10)

button_arxiv = tk.Button(frame_start, text="arXiv", command=lambda: show_frame(frame_arxiv))
button_arxiv.pack(pady=5)

button_pubmed = tk.Button(frame_start, text="PubMed", command=lambda: show_frame(frame_pubmed))
button_pubmed.pack(pady=5)

# Configurar la pantalla de arXiv
button_extract_arxiv = tk.Button(frame_arxiv, text="Extraer artículos", command=run_scraping_arxiv)
button_extract_arxiv.pack(pady=10)

label_cl = tk.Label(frame_arxiv, text="Artículos de cs.CL")
label_cl.pack()
text_result_cl = tk.Text(frame_arxiv, height=15, width=100)
text_result_cl.pack()

label_cv = tk.Label(frame_arxiv, text="Artículos de cs.CV")
label_cv.pack()
text_result_cv = tk.Text(frame_arxiv, height=15, width=100)
text_result_cv.pack()

button_back_arxiv = tk.Button(frame_arxiv, text="Volver", command=lambda: show_frame(frame_start))
button_back_arxiv.pack(pady=10)

# Configurar la pantalla de PubMed
button_extract_pubmed = tk.Button(frame_pubmed, text="Extraer artículos", command=run_scraping_pubmed)
button_extract_pubmed.pack(pady=10)

text_result_pubmed = tk.Text(frame_pubmed, height=30, width=100)
text_result_pubmed.pack()

button_back_pubmed = tk.Button(frame_pubmed, text="Volver", command=lambda: show_frame(frame_start))
button_back_pubmed.pack(pady=10)

# Mostrar la pantalla de inicio al iniciar
show_frame(frame_start)

root.mainloop()