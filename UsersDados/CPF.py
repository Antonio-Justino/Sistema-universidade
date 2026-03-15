from validate_docbr import CPF
from tkinter import messagebox

cpf = CPF()


def verificar_cpf(numero):
    return cpf.validate(numero)

def salvar(self):
    numero = self.entry_cpf.get()

    if cpf.validate(numero):
        messagebox.showinfo("Validação", "CPF válido")
    else:
        messagebox.showerror("Erro", "CPF inválido")

