import io
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
import requests

import matplotlib, numpy, sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Aplicacion:
  def __init__(self, window):
    super().__init__()
    self.wind = window
    self.wind.title("Pokédex")
    self.wind.resizable(False, False)
    try:
      self.wind.iconbitmap("pokeball.ico")
    except:
      pass
    # self.wind.iconbitmap("pokeball.ico")
    
    self.mainFrame = tk.LabelFrame(self.wind, text = "Datos del Pokémon")
    
    tk.Label(self.mainFrame, text = "Nombre: ").grid(row = 0, column = 0, sticky = "E")
    tk.Label(self.mainFrame, text = "Número: ").grid(row = 1, column = 0, sticky = "E")
    
    self.returnName = tk.StringVar()
    self.nombreEntry = tk.Entry(self.mainFrame, textvariable = self.returnName)
    self.nombreEntry.grid(row = 0, column = 1)
    self.nombreEntry.focus()

    self.returnNumber = tk.StringVar()
    self.numeroEntry = tk.Entry(self.mainFrame, textvariable = self.returnNumber)
    self.numeroEntry.grid(row = 1, column = 1)

    self.finalNotification = tk.StringVar()
    self.usrNotifications = tk.Label(self.mainFrame, textvariable = self.finalNotification)
    self.usrNotifications.grid(row = 2, column = 0, columnspan = 2, rowspan = 2)

    BtnConsultar = tk.Button(self.mainFrame, text = "Consultar", fg = "white", bg = "green", bd = 5, command = self.consultaPkmn)
    BtnConsultar.grid(row = 4, column = 0, columnspan = 2, sticky = "WE")

    BtnSalir = tk.Button(self.mainFrame, text = "Salir", command = self.wind.destroy, bg = "red", fg = "white", bd = 5)
    BtnSalir.grid(row = 5, column = 0, columnspan = 2, sticky = "WE")


    self.mainFrame.grid(row = 0, column = 0, sticky = "WENS")

  def consultaPkmn(self):
    if len(self.returnName.get()) == 0 and len(self.returnNumber.get()) == 0:
      self.finalNotification.set("Ingresa un nombre o un\nnúmero para consulta")
      self.usrNotifications.config(fg = "red")
    elif len(self.returnName.get()) != 0 and len(self.returnNumber.get()) != 0:
      self.finalNotification.set("Solo ingresar nombre o\nnúmero para consulta")
      self.usrNotifications.config(fg = "red")
    else:
      self.finalNotification.set("")
      try:
        if len(self.returnName.get()) != 0 and len(self.returnNumber.get()) == 0:
          datoConsulta = self.returnName.get()
          url = f"https://pokeapi.co/api/v2/pokemon/{datoConsulta}"
          data = requests.get(url).json()
          self.returnName.set(data["forms"][0]["name"])
          self.returnNumber.set(data["id"])
        else:
          datoConsulta = self.returnNumber.get()
          url = f"https://pokeapi.co/api/v2/pokemon/{datoConsulta}"
          data = requests.get(url).json()
          self.returnName.set(data["forms"][0]["name"])
          self.returnNumber.set(data["id"])
        #framePictures
        #more info
        self.MoreInfo = tk.LabelFrame(self.wind, text = " *** Más Información *** ")

        self.FramePictures = tk.LabelFrame(self.MoreInfo)
        tk.Label(self.FramePictures, text = "NORMAL").grid(row = 0, column = 0, sticky = "WE")
        tk.Label(self.FramePictures, text = "SHINY").grid(row = 0, column = 1, sticky = "WE")
        #Front Normal
        self.front_img_n = ImageTk.PhotoImage(Image.open(io.BytesIO(urlopen(data["sprites"]["front_default"]).read())))
        self.labelFrontn = tk.Label(self.FramePictures, image=self.front_img_n)
        self.labelFrontn.grid(row = 1, column = 0)
        #Back Picture
        self.back_img_n = ImageTk.PhotoImage(Image.open(io.BytesIO(urlopen(data["sprites"]["back_default"]).read())))
        self.labelBackn = tk.Label(self.FramePictures, image=self.back_img_n)
        self.labelBackn.grid(row = 2, column = 0)
        #front Shiny
        self.front_img_s = ImageTk.PhotoImage(Image.open(io.BytesIO(urlopen(data["sprites"]["front_shiny"]).read())))
        self.labelfronts = tk.Label(self.FramePictures, image=self.front_img_s)
        self.labelfronts.grid(row = 1, column = 1)
        #back shiny
        self.back_img_s = ImageTk.PhotoImage(Image.open(io.BytesIO(urlopen(data["sprites"]["back_shiny"]).read())))
        self.labelbacks = tk.Label(self.FramePictures, image=self.back_img_s)
        self.labelbacks.grid(row = 2, column = 1)
        self.FramePictures.grid(row = 0, column = 0, sticky = "WE", padx = (40, 40))
        self.fieldHabilidades = ttk.Treeview(self.MoreInfo)
        self.fieldHabilidades.grid(row = 0, column = 1, pady = (10,10), padx = (40, 40))
        self.fieldHabilidades.heading("#0", text = "Habilidades")
        self.scrollHabilidades = tk.Scrollbar(self.MoreInfo, orient = "vertical", command = self.fieldHabilidades.yview)
        self.scrollHabilidades.grid(row = 0, column = 2, sticky = "NS")
        self.fieldHabilidades["yscrollcommand"] = self.scrollHabilidades.set
        i = 0
        for i in range(len(data["abilities"])):
          self.fieldHabilidades.insert("",0, text = data["abilities"][i]["ability"]["name"])
        
        self.fieldMovimientos = ttk.Treeview(self.MoreInfo)
        self.fieldMovimientos.grid(row = 0, column = 3, padx = (40, 40))
        self.fieldMovimientos.heading("#0", text = "Movimientos")
        self.scrollMovimientos = tk.Scrollbar(self.MoreInfo, orient = "vertical", command = self.fieldMovimientos.yview)
        self.scrollMovimientos.grid(row = 0, column =  4, sticky = "NS", padx = (0, 0))
        self.fieldMovimientos["yscrollcommand"] = self.scrollMovimientos.set
        z = 0
        for z in range(len(data["moves"])):
          self.fieldMovimientos.insert("", 0, text = data["moves"][z]["move"]["name"])

        # lo ree coloque en el frame principal
        self.Altura = "Altura: {}".format(data["height"])
        tk.Label(self.mainFrame, text = self.Altura).grid(row = 6, column = 0, sticky = "WE", columnspan = 2)

        self.Peso = "Peso: {}".format(data["weight"])
        tk.Label(self.mainFrame, text = self.Peso).grid(row = 7, column = 0, sticky = "WE", columnspan = 2)

        self.baseExp = "Experiencia base: {}".format(data["base_experience"])
        tk.Label(self.mainFrame, text = self.baseExp).grid(row = 8, column = 0, sticky = "WE", columnspan = 2)
        
        self.tipos = []
        i = 0
        for i in range(len(data["types"])):
          self.tipos.append(data["types"][i]["type"]["name"])
        tk.Label(self.mainFrame, text = "Tipo: {}".format(" - ".join(self.tipos))).grid(row = 9, column = 0, sticky = "WE", columnspan = 2)
        #termina el recolocado

        self.categorias = []
        self.Efectividad = []
        for i in range(len(data["stats"])):
          self.categorias.append(data["stats"][i]["stat"]["name"]) #categorias
          self.Efectividad.append(data["stats"][i]["base_stat"]) #Efectividad
        ################################################
        self.f = Figure(figsize=(5,4), dpi=100)
        self.ax = self.f.add_subplot(111)
        self.data = self.Efectividad
        self.ind = self.categorias
        self.width = .7
        
        self.rects1 = self.ax.bar(self.ind, self.data, self.width)
        # plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
        self.canvas = FigureCanvasTkAgg(self.f, master=self.MoreInfo)
        self.canvas.get_tk_widget().grid(row = 3, column = 0, columnspan = 5, sticky = "WE")
        ################################################
        self.MoreInfo.grid(row = 0, column = 4, rowspan = 3, sticky = "N")
      except:
        self.finalNotification.set("Nombre o número no\nvalido para consulta")
        self.usrNotifications.config(fg = "red")

    