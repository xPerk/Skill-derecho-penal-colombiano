# Derecho penal colombiano — skill para Claude

Skill que convierte a Claude en un asistente experto en derecho penal colombiano: Código Penal (Ley 599 de 2000), Código de Procedimiento Penal (Ley 906 de 2004), procedimiento abreviado, adolescentes, régimen penitenciario y las reformas de 2025 y 2026, con conocimiento cerrado a noviembre de 2026.

## Qué hace

- Analiza casos con método: tipicidad, antijuridicidad, culpabilidad, intervinientes, pena y consecuencias procesales.
- Ubica cualquier delito por título y artículo, y obliga a verificar el texto vigente antes de afirmar penas o plazos.
- Incluye las reformas recientes (Ley 2477 de 2025 verificada artículo por artículo; Leyes 2502 de 2025, 2590, 2608, 2627 y 2640 de 2026).
- Calcula con scripts: prescripción de la acción, libertad por vencimiento de términos (art. 317) y dosificación de la pena por cuartos.
- Redacta escritos a partir de plantillas: denuncia, querella, solicitud de libertad, hábeas corpus y reparación integral.

## Contenido

```
derecho-penal-colombia/
├── SKILL.md                     método, regla de vigencia y formato de respuesta
├── references/                  documentos de consulta
│   ├── parte-general.md
│   ├── parte-especial.md
│   ├── procedimiento.md
│   ├── reformas-2025-2026.md
│   ├── penas-beneficios-prescripcion.md
│   ├── leyes-especiales.md
│   ├── jurisprudencia.md
│   └── escritos.md
├── scripts/                     calculadoras en Python (solo biblioteca estándar)
│   ├── prescripcion.py
│   ├── terminos_317.py
│   └── dosificacion.py
└── assets/                      plantillas de escritos
    ├── denuncia.md
    ├── querella.md
    ├── solicitud-libertad-317.md
    ├── habeas-corpus.md
    └── solicitud-reparacion-integral.md
```

## Instalación

**En Claude (web o app):** descarga `derecho-penal-colombia.skill` de este repositorio y súbelo en la sección de Skills de la configuración de Claude.

**En Claude Code:** copia la carpeta `derecho-penal-colombia/` a `~/.claude/skills/`.

## Uso de las calculadoras

```bash
python derecho-penal-colombia/scripts/prescripcion.py --pena-max-meses 108 --fecha-hechos 2021-03-15
python derecho-penal-colombia/scripts/terminos_317.py --imputacion 2026-08-01
python derecho-penal-colombia/scripts/dosificacion.py --min 208 --max 450 --tentativa
```

Cada script imprime sus supuestos. Usa `--help` para ver todos los parámetros.

## Aviso

Esta skill ofrece orientación jurídica informada, no asesoría legal. No reemplaza a un abogado que conozca el expediente. Las normas penales cambian con frecuencia: verifica siempre el texto vigente en la Secretaría del Senado o en SUIN-Juriscol antes de actuar.
