# Staging readiness checklist

- **Entorno**: desplegar la misma versión del repo (branch/tag), usar `gpu_env` o contenedor equivalente; configurar variables sensibles solo por `.env`/secrets del proveedor.
- **Datos**: usar subconjunto representativo (nominal, borde, pesado) sin datos de producción sin anonimizar.
- **Salud básica**: endpoint/CLI de health y versión accesible; log estructurado (JSON) en nivel INFO; errores con trazas.
- **Métricas**: latencia p50/p95/p99, tasa de errores, uso de CPU/GPU/memoria/disk; alarmas básicas si se exceden umbrales definidos.
- **Tests de humo**: ejecutar `python scripts/smoke.py --url <health>` y casos clave definidos; debe devolver 0.
- **Tests automáticos**: `pytest` pasa en staging; compilar sin SyntaxError (`python -m compileall .`).
- **Seguridad**: sin secrets en repo; dependencias auditadas (`pip-audit`); CORS/TLS configurados; validación de inputs.
- **Performance ligera**: prueba de carga corta (locust/k6) 10-100 rps; revisar colas/timeouts.
- **Criterios de salida**: documentar umbrales aceptados y firmar go/no-go.
