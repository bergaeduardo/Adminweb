# SQL de Transferencias entre Depósitos

Los objetos de SQL Server que usa esta app viven acá, versionados, porque el
resto de la lógica de negocio del proyecto está en stored procedures invisibles
a git y eso ya nos costó caro (ver `EB_InsertardetallecomprobanteAjusteV1.2`,
que está roto en producción y nadie se enteró).

Todos los scripts son **idempotentes y re-ejecutables**: las tablas usan
`IF OBJECT_ID(...) IS NULL` y los procedimientos `CREATE OR ALTER`, que además
preserva los `GRANT` (un `DROP`+`CREATE` los perdería y rompería el login de la
app en silencio).

## Orden de aplicación

| # | Script | Servidor | Base |
|---|---|---|---|
| 1 | `laker_sa/001_tablas.sql` | `XL-TANGO` | `LAKER_SA` |
| 2 | `laker_sa/010_EB_TransferDeposito_Validar.sql` | `XL-TANGO` | `LAKER_SA` |
| 3 | `laker_sa/011_EB_TransferDeposito_Aplicar.sql` | `XL-TANGO` | `LAKER_SA` |
| 4 | `laker_sa/012_EB_TransferDeposito_Procesar.sql` | `XL-TANGO` | `LAKER_SA` |
| 5 | `laker_sa/013_EB_TransferDeposito_LimpiarLotes.sql` | `XL-TANGO` | `LAKER_SA` |
| 6 | `wms/020_IX_Movimientos_include_cantidad.sql` | **`XL-SALES\SQLEXPRESS`** | `UbicacionesStockMvc` |

> **Cuidado con el paso 6.** Corre en el **otro** servidor. Apuntar `sqlcmd` al
> servidor equivocado es el accidente de deploy obvio acá.

En Django, `LAKER_SA` es el alias `mi_db_2` y `UbicacionesStockMvc` es `mi_db_3`
(ver `core/local.py` / `core/production.py`).

## Arquitectura

```
Django (transferencias/sql_transferencias.py)
  │  1. uuid4() -> IdLote
  │  2. INSERT cabecera + executemany del detalle
  │  3. EXEC EB_TransferDeposito_Procesar @IdLote, @Usuario, @Host, @SoloValidar
  ▼
EB_TransferDeposito_Procesar          (orquesta, dueño de la transacción y del applock)
  ├── EB_TransferDeposito_Validar     (set-based; fuera de la transacción)
  └── EB_TransferDeposito_Aplicar     (dentro de la transacción, serializado)
        ├── EB_InsertarEncMovimientoV1.2   (reusado: cabecera sta14, talonario 850)
        ├── sta20  x2 por fila            (S en origen / E en destino)
        ├── sta19  delta agregado
        ├── sta10  movimiento de partida conservando n_partida
        └── Movimientos (WMS, vía linked server) con AMBAS ubicaciones
```

`EB_TransferDeposito_Procesar` devuelve **siempre dos resultsets**: primero las
filas con problema (vacío si está limpio), después una única fila de resumen.
Un `RAISERROR` significa falla técnica, nunca un dato malo del usuario.
