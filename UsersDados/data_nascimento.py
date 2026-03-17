from datetime import datetime


def verificar_data(data_texto):
    try:
        data = datetime.strptime(data_texto, "%d/%m/%Y")
        return True
    except ValueError:
        return False