from datetime import datetime
import re

restricciones = {
    "mastes": {
        0: [1, 2],
        1: [3, 4],
        2: [5, 6],
        3: [7, 8],
        4: [9, 0],
    }
}

dias_texto = {
    "lunes": 0,
    "martes": 1,
    "miércoles": 2,
    "miercoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sábado": 5,
    "sabado": 5,
    "domingo": 6
}

def extraer_placa(texto):
    match = re.search(r'\b([A-Z]{3}-?\d{3,4})\b', texto.upper())
    return match.group(1).replace('-', '') if match else None

def verificar_pico_placa(placa, modo="mastes"):
    if not placa or len(placa) < 6:
        return "No entendí bien la placa, ¿puedes repetirla?"

    digito_final = int(placa[-1])
    hoy = datetime.today().weekday()  # 0 = lunes, 6 = domingo

    if hoy > 4:
        dias_ingles = {
            "Monday": "lunes",
            "Tuesday": "martes",
            "Wednesday": "miércoles",
            "Thursday": "jueves",
            "Friday": "viernes",
            "Saturday": "sábado",
            "Sunday": "domingo"
        }
        dia_ingles = datetime.today().strftime('%A')
        dia_espanol = dias_ingles.get(dia_ingles, dia_ingles)
        return f"No hay pico y placa hoy ({dia_espanol}). ¡Puedes circular!"

    restringidos = restricciones.get(modo, {}).get(hoy, [])
    if digito_final in restringidos:
        return f"Hoy no puedes circular con la placa {placa}, tiene pico y placa."
    else:
        return f"Sí puedes circular hoy con la placa {placa}."

def obtener_restriccion_por_dia(texto, modo="mastes"):
    dia_encontrado = next((d for d in dias_texto if d in texto.lower()), None)
    if not dia_encontrado:
        return None
    dia = dias_texto[dia_encontrado]
    if dia >= 5:
        return f"No hay pico y placa el {dia_encontrado}."

    restringidos = restricciones.get(modo, {}).get(dia, [])
    return f"El {dia_encontrado.capitalize()} no pueden circular las placas terminadas en: {', '.join(map(str, restringidos))}."

def procesar_mensaje(mensaje):
    respuesta_dia = obtener_restriccion_por_dia(mensaje)
    if respuesta_dia:
        return respuesta_dia
    placa = extraer_placa(mensaje)
    return verificar_pico_placa(placa)

# Ejemplos de uso
if __name__ == "__main__":
    ejemplos = [
        "¿Puedo circular con la placa ABC123?",
        "Qué pico y placa hay el lunes",
        "Mi placa es XYZ678 y quiero saber si puedo circular",
        "Hay restricción el viernes?",
        "¿Puedo salir el domingo con placa HJM589?"
    ]

    for mensaje in ejemplos:
        print(f"Usuario: {mensaje}")
        print(f"Bot: {procesar_mensaje(mensaje)}\n")
