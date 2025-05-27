Una aplicación de escritorio en Python con interfaz gráfica (PySide6) que permite:
- Cargar un Autómata Finito No Determinista (AFN) desde un archivo .txt o .jff (JFLAP).
- Visualizar la quíntupla del AFN, clausuras ε y tabla de transiciones.
- Ejecutar la construcción por subconjuntos paso a paso.
- Mostrar la quíntupla resultante del AFD y su tabla de transiciones.
- Generar un reporte detallado (pasos del algoritmo, detalles del AFD, listado de δ′).
- Explorar teoría asociada y registrar un log de pasos y acciones.
- Exportar AFN y AFD a archivos JFLAP (.jff) con layout en cuadrícula para mejor visualización.

Características principales
1. Cargar AFN
    - Desde .txt con formato etiquetado o crudo.
    - Desde .jff (JFLAP).
2. Visualización
    - Quíntuplas
    - Tabla de transiciones y Clausuras ε.
3. Construcción de AFD
    - Algoritmo de subconjuntos con pasos detallados.
    - Nombres automáticos S₀, S₁, … para subconjuntos.
4. Reporte
    - Tabla de pasos (Origen, Símbolo, Mover, ε-cierre).
    - Detalles del AFD y listado completo de δ′.
5. Exportación JFLAP
    - AFN y AFD a .jff con layout en grid para evitar montones.
6. Módulos adicionales
    - Teoría integrada.
    - Log de acciones.

## Instalación:
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/afn-to-afd.git
   cd afn-to-afd
   ```
2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .\.venv\Scripts\activate   # Windows
   ```
3. Instala dependencias:
   ```bash
   pip install PySide6 lxml
   ```
    ó
   
   ```bash
   pip3 install PySide6 lxml
   ```


Uso

Ejecuta la aplicación:
```bash
python src/main.py
```
ó

```bash
python3 src/main.py
```

### Estructura de carpetas

```text
afn-to-afd/
├── src/
│   ├── gui/
│   │   └── widgets/        # Componentes de interfaz
│   ├── nfa_dfa/            # Lógica de AFN, AFD y exportación JFLAP
│   ├── parsers/            # Parsers de .txt y .jff
│   └── main.py             # Punto de entrada
├── requirements.txt        # Dependencias
└── README.md               # Documentación
```


