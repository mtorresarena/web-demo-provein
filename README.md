# PROVEIN Jerez — landing demo

Landing estática y responsive para la sucursal de PROVEIN en Jerez, centrada en recambios para vehículos industriales.

## Uso local

No requiere compilación ni dependencias de producción:

```bash
python3 -m http.server 8000
```

Después, abre `http://localhost:8000`.

## Pruebas

Desde la raíz del repositorio:

```bash
python3 -m unittest discover -s tests -v
```

Las pruebas comprueban la estructura esencial, datos factuales, referencias locales, existencia de los seis activos y límites de presentación de las imágenes.

## Archivos

- `index.html`: contenido y estructura accesible.
- `styles.css`: diseño responsive, sin ampliar imágenes sobre sus dimensiones útiles.
- `script.js`: menú móvil y año del pie.
- `image-sources.json`: procedencia, dimensiones y hashes declarados de los activos.
- `public/assets/`: seis imágenes recuperadas previamente de la web oficial.

## Alcance y cautelas

Este sitio es una **demo interna**. Los datos se basan en las páginas oficiales de contacto, productos y empresa de PROVEIN, verificadas el 26 de julio de 2026. No se afirma stock, disponibilidad, precios ni garantías; tampoco se presentan marcas como clientes. No contiene vídeo ni material generado con IA.

El material visual procede de la web oficial y no consta como licencia libre. Antes de publicar deben confirmarse permiso, derechos y vigencia. Los apoyos son de baja resolución y se muestran contenidos. El hero es un reescalado Lanczos no generativo de una fuente de 720 × 369 px, por lo que su anchura efectiva se limita a 720 px.
