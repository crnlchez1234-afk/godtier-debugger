# 🚀 Roadmap to Tier 1 Commercial Product
*De Prototipo "God Tier" a Estándar de la Industria*

## 🛡️ Fase 1: Seguridad y Robustez (The "Do No Harm" Update)
El objetivo es garantizar que la IA nunca pueda dañar el entorno del usuario.

- [ ] **Sandboxing de Ejecución:** Implementar un ejecutor aislado para los "Mutantes" de Darwin.
    - *Opción A (Ligera):* Usar `multiprocessing` con límites de recursos (timeout, memoria).
    - *Opción B (Robusta):* Ejecutar validaciones dentro de un contenedor Docker efímero.
- [ ] **Validación de AST:** Crear un "Linter de Seguridad" que rechace código generado con imports peligrosos (`os`, `subprocess`, `shutil`) a menos que estén en una lista blanca explícita.
- [ ] **Timeouts Estrictos:** Si un mutante tarda más de X segundos o 2x el tiempo original, se mata el proceso inmediatamente (prevención de bucles infinitos).

## 🏗️ Fase 2: Escalabilidad y Contexto (The "Enterprise" Update)
Hacer que funcione en repositorios reales, no solo en scripts.

- [ ] **Soporte de Imports Relativos:** Asegurar que `main.py` pueda parchear funciones en `src/utils/helper.py` sin romper las referencias.
- [ ] **Gene Memory (Persistencia):**
    - Crear `darwin.db` (SQLite).
    - Almacenar: `FunctionSignature`, `OriginalSourceHash`, `OptimizedSource`, `PerformanceGain`.
    - Al iniciar, consultar la DB antes de invocar a la IA.
- [ ] **Manejo de Clases:** Mejorar el extractor AST para manejar métodos de instancia (`self`) y métodos de clase (`cls`) correctamente.

## 🤝 Fase 3: Experiencia de Desarrollador (The "DX" Update)
Herramientas para que el humano confíe y controle a la máquina.

- [ ] **Modo Interactivo (TUI):** Usar librerías como `Textual` o `Rich` para mostrar un dashboard en la terminal en lugar de texto plano.
    - Ver el código original y el mutante lado a lado.
    - Botones para Aceptar/Rechazar cambios.
- [ ] **Reportes HTML/JSON:** Generar un reporte al final de la ejecución (`debug_report.html`) con gráficos de rendimiento y detalles de los errores corregidos.
- [ ] **Integración con Git:** Opción para que Darwin cree una rama nueva (`git checkout -b darwin-optimizations`) y haga commit de los cambios en lugar de modificar el archivo en vivo.

## 🧠 Fase 4: Inteligencia Avanzada (The "AGI" Update)
Mejorar la calidad de las soluciones.

- [ ] **Soporte Multi-Modelo:**
    - Configuración para usar OpenAI/Anthropic API si el usuario tiene una Key (para problemas difíciles).
    - Fallback automático: Si Phi-2 falla 3 veces, intentar con un modelo mayor si está disponible.
- [ ] **RAG (Retrieval Augmented Generation):** Que la IA pueda leer documentación de las librerías que usa el usuario (ej. leer docs de `pandas` si el script usa pandas) para sugerir optimizaciones idiomáticas.

## 📦 Fase 5: Empaquetado y Distribución
- [ ] **Instalador One-Click:** `.exe` o `pip install neurosys-debugger` que configure el entorno Python y descargue los modelos automáticamente.
- [ ] **VS Code Extension:** La meta final. Una extensión que haga todo esto desde la UI del editor.
