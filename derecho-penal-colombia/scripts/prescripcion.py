#!/usr/bin/env python3
"""Prescripción de la acción penal en Colombia (arts. 83 y 86 de la Ley 599 de 2000).

Calcula el término de prescripción a partir del máximo de la pena del delito,
la fecha límite para formular imputación y, si ya hubo imputación, la nueva
fecha límite tras la interrupción.

Ejemplos:
  python prescripcion.py --pena-max-meses 108 --fecha-hechos 2021-03-15
  python prescripcion.py --pena-max-meses 144 --fecha-hechos 2019-01-10 --fecha-imputacion 2023-06-01
  python prescripcion.py --pena-max-meses 90 --fecha-hechos 2020-05-05 --servidor-publico

La pena máxima debe tomarse del texto VIGENTE del tipo penal a la fecha de los
hechos, incluidos los agravantes o atenuantes específicos que modifican sus
límites (no las circunstancias genéricas de los arts. 55 y 58).
"""
import argparse
import calendar
from datetime import date, timedelta
from fractions import Fraction


def parse_date(s):
    return date.fromisoformat(s) if s else None


def add_months(d, months):
    """Suma meses (admite fracción: la parte decimal se convierte en días, 30 por mes)."""
    whole = int(months)
    frac = Fraction(months) - whole
    y = d.year + (d.month - 1 + whole) // 12
    m = (d.month - 1 + whole) % 12 + 1
    day = min(d.day, calendar.monthrange(y, m)[1])
    out = date(y, m, day)
    return out + timedelta(days=round(float(frac) * 30))


def fmt_months(m):
    m = Fraction(m)
    years = int(m // 12)
    rest = m - years * 12
    a = f"{years} año" + ("s" if years != 1 else "")
    if rest == 0:
        return f"{a} ({float(m):g} meses)"
    return f"{a} y {float(rest):g} meses ({float(m):g} meses)"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pena-max-meses", type=float, help="Máximo de la pena de prisión del delito, en meses")
    p.add_argument("--especial", choices=["ninguno", "30-anios", "imprescriptible"], default="ninguno",
                   help="30-anios: desaparición forzada, tortura, desplazamiento forzado y demás del inciso 2 del art. 83. "
                        "imprescriptible: genocidio, lesa humanidad, crímenes de guerra, delitos sexuales contra menores (Ley 2081 de 2021)")
    p.add_argument("--servidor-publico", action="store_true",
                   help="Servidor público (o particular con funciones públicas) que cometió el delito en ejercicio de sus funciones: aumento en la mitad")
    p.add_argument("--exterior", action="store_true", help="Conducta iniciada o consumada en el exterior: aumento en la mitad")
    p.add_argument("--fecha-hechos", help="Fecha de consumación o del último acto (AAAA-MM-DD)")
    p.add_argument("--fecha-imputacion", help="Fecha de la formulación de imputación o del traslado del escrito de acusación en el abreviado (AAAA-MM-DD)")
    p.add_argument("--suspension-meses", type=float, default=0,
                   help="Meses de suspensión a sumar (p. ej. principio de oportunidad, hasta 36)")
    p.add_argument("--hoy", help="Fecha de referencia (AAAA-MM-DD); por defecto, hoy")
    a = p.parse_args()

    hoy = parse_date(a.hoy) or date.today()
    supuestos = []

    if a.especial == "imprescriptible":
        print("La acción penal es IMPRESCRIPTIBLE para este delito.")
        print("Verifica que el delito y la fecha de los hechos estén cubiertos (Estatuto de Roma; Ley 2081 de 2021 para delitos sexuales contra menores, aplicable a hechos no prescritos a su entrada en vigor).")
        return

    if a.especial == "30-anios":
        base = Fraction(360)
        print(f"1. Término especial del art. 83, inciso 2: {fmt_months(base)}")
    else:
        if a.pena_max_meses is None:
            p.error("Falta --pena-max-meses")
        pena = Fraction(a.pena_max_meses).limit_denominator(1000)
        base = min(max(pena, Fraction(60)), Fraction(240))
        print(f"1. Máximo de la pena: {fmt_months(pena)}")
        if base != pena:
            print(f"   Ajustado a los límites del art. 83 (mínimo 5, máximo 20 años): {fmt_months(base)}")
        else:
            print(f"   Dentro de los límites de 5 a 20 años: {fmt_months(base)}")

    termino = base
    if a.servidor_publico:
        termino = termino * Fraction(3, 2)
        print(f"2. Aumento en la mitad por servidor público: {fmt_months(termino)}")
        supuestos.append("El aumento por servidor público se aplicó sobre el término ya ajustado a los límites de 5 a 20 años, como lo ha entendido la Sala Penal; confirma la línea vigente.")
    if a.exterior:
        termino = termino * Fraction(3, 2)
        print(f"   Aumento en la mitad por conducta en el exterior: {fmt_months(termino)}")
        supuestos.append("El aumento por conducta en el exterior no puede exceder el máximo fijado en el art. 83; revisa el texto vigente.")

    print(f"\nTérmino de prescripción de la acción (antes de imputación): {fmt_months(termino)}")

    # Interrupción (art. 86)
    nuevo = termino / 2
    nuevo_ajustado = min(max(nuevo, Fraction(60)), Fraction(120))
    print(f"Término tras la interrupción por imputación: mitad = {fmt_months(nuevo)}; "
          f"ajustado a 5-10 años = {fmt_months(nuevo_ajustado)}")
    if a.servidor_publico:
        supuestos.append("Con servidor público, la Corte Suprema ha discutido si el tope de 10 años del art. 86 se aplica antes o después del aumento; verifica.")

    fh = parse_date(a.fecha_hechos)
    fi = parse_date(a.fecha_imputacion)
    susp = Fraction(a.suspension_meses).limit_denominator(1000)

    if fh:
        limite_imp = add_months(fh, termino + susp)
        print(f"\nFecha de los hechos: {fh.isoformat()}")
        if susp:
            print(f"Suspensión sumada: {float(susp):g} meses")
        print(f"Fecha límite para formular imputación: {limite_imp.isoformat()}")
        if fi:
            if fi > limite_imp:
                print(f"ATENCIÓN: la imputación ({fi.isoformat()}) fue posterior a la fecha límite. "
                      "La acción habría prescrito antes de la imputación.")
            else:
                limite_final = add_months(fi, nuevo_ajustado)
                print(f"Fecha de imputación: {fi.isoformat()} (interrumpe la prescripción)")
                print(f"Nueva fecha límite tras la interrupción: {limite_final.isoformat()}")
                print("  Tras la sentencia de segunda instancia el término se suspende hasta por 5 años (art. 189 Ley 906).")
                estado = "PRESCRITA" if hoy > limite_final else "VIGENTE"
                print(f"Estado a {hoy.isoformat()}: {estado}")
        else:
            estado = "PRESCRITA (si no hubo imputación)" if hoy > limite_imp else "VIGENTE"
            print(f"Estado a {hoy.isoformat()}: {estado}")

    print("\nSupuestos y verificaciones:")
    supuestos.insert(0, "La pena máxima debe ser la del texto vigente a la fecha de los hechos, con los modificadores específicos de sus límites.")
    supuestos.append("Las fracciones de mes se convierten a 30 días.")
    supuestos.append("En concurso, cada delito prescribe por separado.")
    for s in supuestos:
        print(f"- {s}")


if __name__ == "__main__":
    main()
