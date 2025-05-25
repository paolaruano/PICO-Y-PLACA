
import re
from datetime import datetime

# Patrones de placas por tipo de vehículo
patrones = {
    'particular': r'^[A-Z]{3} \d{3}$',    # Ej: AAA 123
    'publico': r'^[A-Z]{2} \d{4}$',       # Ej: AB 1234
    'moto': r'^[A-Z]{3} \d{2}[A-Z]?$'     # Ej: ABC 12 o ABC 12A
}

# Restricciones por día
restriccion = {
    0: [7, 8],  # Lunes
    1: [9, 0],  # Martes
    2: [1, 2],  # Miércoles
    3: [3, 4],  # Jueves
    4: [5, 6]   # Viernes
}

dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

def validar_formato_placa(placa):
    for tipo, patron in patrones.items():
        if re.match(patron, placa.upper()):
            return {"tipo": tipo, "es_valida": True, "placa": placa.upper()}
    return {"tipo": None, "es_valida": False, "mensaje": "Formato de placa inválido."}

def obtener_dia_pico_placa(digito):
    for dia, digitos in restriccion.items():
        if digito in digitos:
            return dias_semana[dia]
    return "Sin restricción (fin de semana)"

def consultar_placa_en_dia(placa, nombre_dia):
    validacion = validar_formato_placa(placa)
    if not validacion['es_valida']:
        return f"❌ {validacion['mensaje']}"

    digitos = ''.join(filter(str.isdigit, validacion['placa']))
    if not digitos:
        return f"❌ No se encontraron dígitos en la placa {placa}"

    ultimo = int(digitos[-1])
    try:
        dia_index = dias_semana.index(nombre_dia.capitalize())
    except ValueError:
        return "❌ Día inválido. Usa nombres como: Lunes, Martes, etc."

    restringidos = restriccion.get(dia_index, [])

    if ultimo in restringidos:
        return f"🚫 La placa '{placa.upper()}' tiene pico y placa el {nombre_dia.capitalize()}."
    else:
        return f"✅ La placa '{placa.upper()}' NO tiene pico y placa el {nombre_dia.capitalize()}."

# Ejemplo interactivo (solo si se ejecuta directamente)
if __name__ == "__main__":
    print("🔍 Asistente de Pico y Placa\n")

    placa = input("Ingrese la placa (ej: ABC 123): ")
    dia = input("Ingrese el día (ej: Lunes): ")

    resultado = consultar_placa_en_dia(placa, dia)
    print(resultado)
