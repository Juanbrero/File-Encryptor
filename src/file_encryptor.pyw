import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import sys


class Window:

    def file_search(self):
        self.selected_pathfiles = filedialog.askopenfilenames(filetypes=[('Archivos de texto', '*.txt'), ('Todos los archivos', '*.*')])
        temp_files = ""

        if self.selected_pathfiles:
            for path in reversed(self.selected_pathfiles):
                temp_files = temp_files +  os.path.basename(path) + ";"
                    
            self.selected_files.set(temp_files)
        else:
            self.selected_files.set("")
            self.selected_pathfiles = ()
        
    def show_notification(self, msg):
   
        notif_window = tk.Toplevel(self.root)
        notif_window.overrideredirect(True)
        notif_window.attributes("-topmost", True)

        notif_frame = ttk.Frame(notif_window, style="Notification.TFrame")
        notif_frame.pack(expand=True, fill=tk.BOTH)

        self.root.update_idletasks()  # Asegurar que la geometría de root está actualizada
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        notif_width = 300  # Ancho de la ventana emergente
        
        x = root_x + (root_width - notif_width) // 2 - 15 # Centrar horizontalmente con respecto a root
        y = root_y + 45  # Ajustar a la parte superior de root

        notif_window.geometry(f"350x30+{x}+{y}")
    
        msg_label = ttk.Label(notif_frame, text=msg, style="Notification.TLabel")
        msg_label.pack(expand=True)
        notif_window.after(3000, notif_window.destroy)

        style = ttk.Style()
        style.configure("Notification.TFrame", background="LightGoldenrod1", relief="solid", borderwidth=1)
        style.configure("Notification.TLabel", background="LightGoldenrod1", font=("Arial Black", 10))

    def get_values(self):
        
        if (self.selected_pathfiles and (self.input_key.get() != "")):
            for path in self.selected_pathfiles:
                xor_mask(file_name=path,key=self.input_key.get())
            
            self.selected_pathfiles = ()
            self.selected_files.set("")
            self.key.set("")
            self.show_notification("Archivo/s enmascarado/s con exito!")
        elif (self.selected_pathfiles and (self.input_key.get() == "")):
            self.show_notification("Clave necesaria! Ingrese una.")
        elif (self.selected_pathfiles == () and (self.input_key.get() != "")):
            self.show_notification("No hay archivos seleccionados!")
        
    def show_pass(self):
        if self.input_key.cget('show') == '':
            self.input_key.config(show='•')
            self.show_pass_button.config(image=self.show_img)
        else:
            self.input_key.config(show='')
            self.show_pass_button.config(image=self.hide_img)        

    def resize_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((29,29))
        return ImageTk.PhotoImage(img)

    def __init__(self):
        
        self.selected_pathfiles = ()

        self.root = tk.Tk()
        self.root.title("File Encryptor")
        self.root.resizable(0,0)

        icon_path = resource_path("src/icon.ico")

        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")
        
        self.root.config(bg="DeepSkyBlue3", relief=tk.GROOVE, bd=10)

        wtotal = self.root.winfo_screenwidth()
        htotal = self.root.winfo_screenheight()
        wwindow = 600
        hwindow = 350
        pwidth = round(wtotal/2-wwindow/2)
        pheight= round(htotal/2-hwindow/2)
        self.root.geometry(str(wwindow) + "x" + str(hwindow) + "+" + str(pwidth) + "+" + str(pheight))

        frame = tk.Frame(self.root, width=400, height=200)
        frame.pack(expand=1)
        frame.config(bg="DeepSkyBlue4", relief=tk.GROOVE, bd=10)
        
        file_label = tk.Label(text="Directorio del archivo:", bg="DeepSkyBlue4", font=("Arial Black", 11))
        file_label.place(x=105,y=90)
        
        self.selected_files = StringVar()
        self.key = StringVar()

        self.file_selected_entry = tk.Entry(textvariable=self.selected_files, width=45, bg="snow", relief=tk.RAISED, bd=1.5, state="readonly")
        self.file_selected_entry.place(x=110, y=129)

        search_button = tk.Button(height= 1, text="Examinar", font=("Arial", 10), bg="light gray", relief=tk.RAISED, bd=1.5, command=self.file_search).place(x=400,y=125)

        key_label = tk.Label(text="Clave de encriptado/desencriptado:", bg="DeepSkyBlue4", font=("Arial Black", 11)).place(x=105,y=162)
        
        self.input_key = tk.Entry(textvariable=self.key, width=45, bg="snow", relief=tk.RAISED, bd=1.5)
        self.input_key.place(x=110, y=203)
        self.input_key.config(show="•")

        showimg_path = resource_path("src/show.png")
        hideimg_path = resource_path("src/hide.png")

        self.show_img = self.resize_image(showimg_path)
        self.hide_img = self.resize_image(hideimg_path)
        self.show_pass_button = tk.Button(height=12, width=13, image=self.show_img, background="snow",relief=tk.FLAT, bd=1.5, command=self.show_pass)
        self.show_pass_button.place(x=363,y=204)

        enter_button = tk.Button(height=1, width=7, text="OK", font=("Arial", 10), bg="light gray", relief=tk.RAISED, bd=1.5 , command=self.get_values).place(x=400,y=200)
        
        self.root.mainloop()
    

def xor_mask(file_name, key):
    key_index = 0
    content = ''
    encrypted_content = ''
    max_key_index = len(key) - 1
    # extraigo el contenido del archivo
    with open(file_name, 'r') as f:
        content = f.read()

        # aplico la mascara xor
        for char in content:
            encrypted_char = ord(char) ^ ord(key[key_index])
            encrypted_content += chr(encrypted_char)
            if key_index >= max_key_index:
                key_index = 0
            else:
                key_index += 1

    # reemplazo el contenido original por el enmascarado.
    with open(file_name, 'w') as f:
        f.write(encrypted_content)


def resource_path(relative_path):
    """ Devuelve la ruta absoluta del recurso """
    try:
        # PyInstaller crea esta variable para encontrar la ruta temporal
        base_path = sys._MEIPASS
    except AttributeError:
        # En un entorno normal, simplemente usa la ruta absoluta del script
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
  

if __name__ == '__main__':

    window = Window()
    