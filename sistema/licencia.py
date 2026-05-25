import os
import base64
import hashlib
from datetime import date, datetime

SECRET      = 'petshop_lic_2024'
ARCHIVO_LIC = '.lic'
DIAS_PRUEBA = 30

def _codificar(texto):
    return base64.b64encode(texto.encode()).decode()

def _decodificar(texto):
    return base64.b64decode(texto.encode()).decode()

def primera_ejecucion():
    if not os.path.exists(ARCHIVO_LIC):
        with open(ARCHIVO_LIC, 'w') as f:
            f.write(_codificar(str(date.today())))

def obtener_fecha_instalacion():
    try:
        with open(ARCHIVO_LIC, 'r') as f:
            return datetime.strptime(_decodificar(f.read().strip()), '%Y-%m-%d').date()
    except:
        return None

def verificar_licencia():
    fecha = obtener_fecha_instalacion()
    if not fecha:
        primera_ejecucion()
        return True
    return (date.today() - fecha).days <= DIAS_PRUEBA

def dias_restantes():
    fecha = obtener_fecha_instalacion()
    if not fecha:
        return DIAS_PRUEBA
    return max(0, DIAS_PRUEBA - (date.today() - fecha).days)

def generar_clave(fecha_str):
    """Usás esto vos para generar la clave del cliente"""
    return hashlib.sha256((SECRET + fecha_str).encode()).hexdigest()[:8].upper()

def activar_licencia(clave_ingresada):
    fecha = obtener_fecha_instalacion()
    if not fecha:
        return False
    if clave_ingresada.upper() == generar_clave(str(fecha)):
        with open(ARCHIVO_LIC, 'w') as f:
            f.write(_codificar(str(date.today())))
        return True
    return False