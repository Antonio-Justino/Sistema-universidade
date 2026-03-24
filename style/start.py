import customtkinter as ctk

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
            command=self.tem,
            fg_color="#blue",
            hover_color="#deepblue",
            font=("Roboto", 14, "bold"),
            height=45
        )
        self.btn_cadastro.pack(pady=40, padx=40, fill="x")

        self.btn_ncadastro = ctk.CTkButton(
            self,
            text="Tenho não tenho cadastro",
            command=self.tem,
            fg_color="#red",
            hover_color="#deepred",
            font=("Roboto", 14, "bold"),
            height=45
        )
        self.btn_cadastro.pack(pady=40, padx=40, fill="x")
