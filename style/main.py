from database.banco import criar_tabelas
from login import TelaLogin

criar_tabelas()

if __name__ == "__main__":
    app = TelaLogin()
    app.mainloop()