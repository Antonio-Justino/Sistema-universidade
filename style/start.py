import customtkinter as ctk
from tkinter import messagebox
import sys
import os

ctk.set_appearance_mode("System mode")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema RAD - Cadastro Moderno")
        self.geometry("450x600")

        #Titulo
        self.label_titulo = ctk.CTkLabel(
            self, text="Bem vindo", font=("Roboto", 24, "bold")
        )
        self.label_titulo.pack(pady=30)

        self.btn_cadastro = ctk.CTkButton(
            self,
            text="Tenho cadastro",
            command=self.tem_cadastro,
            fg_color="#0000FF",
            hover_color="#00008B",
            font=("Roboto", 14, "bold"),
            height=45
        )
        self.btn_cadastro.pack(pady=40, padx=40, fill="x")

        self.btn_ncadastro = ctk.CTkButton(
            self,
            text="Não tenho cadastro",
            command=self.nao_tem,
            fg_color="#ff2c2c",
            hover_color="#8B0000",
            font=("Roboto", 14, "bold"),
            height=45
        )
        self.btn_ncadastro.pack(pady=40, padx=40, fill="x")
    
    def tem_cadastro(self):
        print("Ir para tela de login")

    def nao_tem(self):
        print("Ir para tela de cadastro")
