#!/usr/bin/env python3
"""Dosificación punitiva (arts. 60 y 61 de la Ley 599 de 2000).

1. Parte de los límites mínimo y máximo del tipo (en meses).
2. Aplica, en orden, los modificadores del marco: aumentos y disminuciones por
   fracciones (agravantes o atenuantes específicos, tentativa, complicidad, etc.).
   Regla usada: en un AUMENTO "de a a b", el mínimo sube en a y el máximo en b;
   en una DISMINUCIÓN "de a a b", el mínimo baja en la fracción mayor y el máximo
   en la menor (así se amplía el ámbito, como lo aplica la Sala Penal).
3. Divide el ámbito en cuartos (art. 61).
4. Opcional: aplica una rebaja posterior (allanamiento o preacuerdo) a una pena concreta.

Ejemplos:
  python dosificacion.py --min 96 --max 216
  python dosificacion.py --min 208 --max 450 --tentativa
  python dosificacion.py --min 48 --max 108 --aumento 1/3-1/2 --complicidad
  python dosificacion.py --min 64 --max 144 --pena 64 --rebaja 1/2
"""
import argparse
from fractions import Fraction


def frac(s):
    return Fraction(s)


def rango(s):
    if "-" in s:
        a, b = s.split("-", 1)
        return frac(a), frac(b)
    x = frac(s)
    return x, x


def fm(m):
    m = Fraction(m)
    meses = float(m)
    total_dias = round(meses * 30)
    meses_ent, dias = divmod(total_dias, 30)
    anios, meses_r = divmod(meses_ent, 12)
    partes = []
    if anios:
        partes.append(f"{anios} año" + ("s" if anios != 1 else ""))
    if meses_r:
        partes.append(f"{meses_r} mes" + ("es" if meses_r != 1 else ""))
    if dias:
        partes.append(f"{dias} día" + ("s" if dias != 1 else ""))
    return f"{meses:.2f} meses ({', '.join(partes) or '0'})"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--min", type=frac, required=True, help="Mínimo de la pena del tipo, en meses")
    p.add_argument("--max", type=frac, required=True, help="Máximo de la pena del tipo, en meses")
    p.add_argument("--aumento", action="append", default=[], help='Aumento por fracciones, p. ej. "1/3-1/2" o "1/3". Repetible')
    p.add_argument("--disminucion", action="append", default=[], help='Disminución por fracciones, p. ej. "1/6-1/2". Repetible')
    p.add_argument("--tentativa", action="store_true", help="Art. 27: mínimo a la mitad, máximo a las tres cuartas partes")
    p.add_argument("--complicidad", action="store_true", help="Art. 30: disminución de una sexta parte a la mitad")
    p.add_argument("--interviniente", action="store_true", help="Art. 30 inc. final: disminución de una cuarta parte")
    p.add_argument("--tope", type=frac, default=Fraction(600), help="Tope de la prisión en meses (600 = 50 años)")
    p.add_argument("--pena", type=frac, help="Pena concreta fijada dentro del cuarto, en meses, para aplicar --rebaja")
    p.add_argument("--rebaja", help='Rebaja posterior sobre --pena, p. ej. "1/2" (allanamiento en imputación), "1/3", "1/6"')
    a = p.parse_args()

    lo, hi = a.min, a.max
    print(f"Marco del tipo: de {fm(lo)} a {fm(hi)}")

    pasos = [("aumento", r) for r in a.aumento] + [("disminucion", r) for r in a.disminucion]
    if a.tentativa:
        pasos.append(("disminucion", "1/4-1/2"))
    if a.complicidad:
        pasos.append(("disminucion", "1/6-1/2"))
    if a.interviniente:
        pasos.append(("disminucion", "1/4"))

    for tipo, r in pasos:
        x, y = rango(r)
        menor, mayor = min(x, y), max(x, y)
        if tipo == "aumento":
            lo, hi = lo * (1 + menor), hi * (1 + mayor)
            print(f"Aumento {r}: mínimo +{menor}, máximo +{mayor} → de {fm(lo)} a {fm(hi)}")
        else:
            lo, hi = lo * (1 - mayor), hi * (1 - menor)
            print(f"Disminución {r}: mínimo −{mayor}, máximo −{menor} → de {fm(lo)} a {fm(hi)}")

    if hi > a.tope:
        print(f"El máximo supera el tope de {fm(a.tope)}; se ajusta.")
        hi = a.tope

    ambito = hi - lo
    q = ambito / 4
    print(f"\nÁmbito de movilidad: {fm(ambito)}; cada cuarto: {fm(q)}")
    nombres = ["Cuarto mínimo", "Primer cuarto medio", "Segundo cuarto medio", "Cuarto máximo"]
    for i, n in enumerate(nombres):
        print(f"  {n}: de {fm(lo + q * i)} a {fm(lo + q * (i + 1))}")

    print("\nArt. 61: sin circunstancias genéricas o solo de menor punibilidad (art. 55) → cuarto mínimo; "
          "concurren de menor y mayor → cuartos medios; solo de mayor punibilidad (art. 58) → cuarto máximo.")

    if a.pena is not None and a.rebaja:
        r = frac(a.rebaja)
        final = a.pena * (1 - r)
        print(f"\nPena fijada: {fm(a.pena)}; rebaja de {r}: {fm(a.pena * r)}; pena final: {fm(final)}")
        print("Verifica que el delito no tenga exclusión de rebajas (art. 199 Ley 1098, art. 26 Ley 1121, feminicidio) "
              "y el porcentaje según la etapa (arts. 351, 356 núm. 5, 367 Ley 906).")

    print("\nSupuestos: 1 mes = 30 días para la conversión; los límites del tipo deben tomarse del texto vigente "
          "a la fecha de los hechos (incluido el aumento de la Ley 890 de 2004 cuando aplique).")


if __name__ == "__main__":
    main()
