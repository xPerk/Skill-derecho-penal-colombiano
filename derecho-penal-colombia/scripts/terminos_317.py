#!/usr/bin/env python3
"""Libertad por vencimiento de términos: art. 317 de la Ley 906 de 2004
(texto modificado por el art. 6 de la Ley 2477 de 2025).

Plazos:
  num. 5: 60 días desde la imputación sin escrito de acusación ni solicitud de preclusión
  num. 6: 120 días desde la acusación sin inicio de la audiencia de juicio
  num. 7: 150 días desde el inicio del juicio sin audiencia de lectura de fallo
Se duplican en justicia especializada, con tres o más procesados, en delitos de
corrupción (Ley 1474 de 2011), en delitos sexuales (Título IV del Libro II) y en
los arts. 103A y 104A del Código Penal.

Ejemplos:
  python terminos_317.py --imputacion 2026-05-10
  python terminos_317.py --imputacion 2026-01-15 --acusacion 2026-03-01 --duplicar
  python terminos_317.py --acusacion 2026-02-01 --descontar-dias 20 --hoy 2026-07-01
"""
import argparse
from datetime import date, timedelta


def d(s):
    return date.fromisoformat(s) if s else None


def tramo(nombre, inicio, fin_evento, plazo, descontar, hoy):
    vence = inicio + timedelta(days=plazo + descontar)
    print(f"\n{nombre}")
    print(f"  Inicio: {inicio.isoformat()}  |  Plazo: {plazo} días" + (f" + {descontar} días descontados" if descontar else ""))
    print(f"  Vence: {vence.isoformat()} (la libertad procede desde el día siguiente)")
    if fin_evento:
        if fin_evento <= vence:
            print(f"  El acto que corta el término ocurrió el {fin_evento.isoformat()}, dentro del plazo: NO procede por este numeral.")
        else:
            print(f"  El acto que corta el término ocurrió el {fin_evento.isoformat()}, DESPUÉS del vencimiento: "
                  "la causal se configuró entre ambas fechas (si se pidió en ese lapso).")
    else:
        transcurridos = (hoy - inicio).days - descontar
        if hoy > vence:
            print(f"  A {hoy.isoformat()} han transcurrido {transcurridos} días computables: TÉRMINO VENCIDO, procede solicitar la libertad.")
        else:
            print(f"  A {hoy.isoformat()} han transcurrido {transcurridos} días computables; faltan {(vence - hoy).days} días.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--imputacion", help="Fecha de la formulación de imputación (AAAA-MM-DD)")
    p.add_argument("--acusacion", help="Fecha de presentación del escrito de acusación o de la solicitud de preclusión")
    p.add_argument("--inicio-juicio", help="Fecha de inicio de la audiencia de juicio oral")
    p.add_argument("--lectura-fallo", help="Fecha de la audiencia de lectura de fallo")
    p.add_argument("--duplicar", action="store_true",
                   help="Aplica el parágrafo: justicia especializada, 3 o más procesados, corrupción, delitos sexuales, arts. 103A y 104A")
    p.add_argument("--descontar-dias", type=int, default=0,
                   help="Días que no se cuentan por maniobras dilatorias de la defensa")
    p.add_argument("--hoy", help="Fecha de referencia (AAAA-MM-DD); por defecto, hoy")
    a = p.parse_args()

    hoy = d(a.hoy) or date.today()
    f = 2 if a.duplicar else 1
    imp, acu, ini, lec = d(a.imputacion), d(a.acusacion), d(a.inicio_juicio), d(a.lectura_fallo)

    if not any([imp, acu, ini]):
        p.error("Indica al menos --imputacion, --acusacion o --inicio-juicio")

    print("Art. 317 Ley 906 de 2004 (Ley 2477 de 2025)" + (" — plazos DUPLICADOS por el parágrafo" if a.duplicar else ""))
    if imp:
        tramo("Numeral 5: imputación → escrito de acusación o solicitud de preclusión", imp, acu, 60 * f, a.descontar_dias, hoy)
    if acu:
        tramo("Numeral 6: acusación → inicio de la audiencia de juicio", acu, ini, 120 * f, a.descontar_dias, hoy)
    if ini:
        tramo("Numeral 7: inicio del juicio → audiencia de lectura de fallo", ini, lec, 150 * f, a.descontar_dias, hoy)

    print("\nSupuestos y verificaciones:")
    print("- Se cuentan días calendario; confirma el criterio vigente de la Sala Penal sobre el cómputo.")
    print("- Los días descontados se aplican a cada tramo; ajústalos si la dilación afectó solo uno.")
    print("- El término se reinicia si se improbó la aceptación de cargos, un preacuerdo o el principio de oportunidad.")
    print("- En fuerza mayor, la audiencia debe reanudarse a más tardar en la mitad del plazo.")
    print("- Verifica que el procesado esté privado de la libertad por esta actuación y que no haya otra causa de detención.")


if __name__ == "__main__":
    main()
