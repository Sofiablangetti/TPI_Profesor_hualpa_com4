def validar_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print(" Campo vacío. Reintentá.")

def validar_numero(mensaje, tipo):
    while True:
        try:
            valor = tipo(input(mensaje))
            if valor > 0:
                return valor
            else:
                print(" Debe ser un número positivo.")
        except ValueError:
            print(" Dato inválido. Reintentá.")
