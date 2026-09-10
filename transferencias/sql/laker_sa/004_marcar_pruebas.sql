/* ============================================================================
   Marca de lotes de PRUEBA
   Servidor: XL-TANGO   Base: LAKER_SA
   Idempotente y aditivo.

   Durante el desarrollo de la herramienta (v1, v2 y v3) se ejecutaron
   transferencias reales contra producción para verificar que cada tabla
   quedara bien. Cada prueba fue devuelta con un movimiento inverso, así que
   el efecto NETO sobre el stock fue CERO — verificado por par
   (depósito, artículo).

   Pero los registros quedaron, y ensucian el historial y sus totales. Esta
   marca los saca de la pantalla SIN BORRARLOS:

     - es reversible (si algo quedó mal clasificado se desmarca y vuelve);
     - deja la explicación de por qué existen esos comprobantes en Tango.

   LO QUE ESTA MARCA *NO* HACE:
   los comprobantes en sta14/sta20 y las filas del WMS quedan donde están. Son
   el rastro de auditoría del ERP y no se tocan: un reporte de Tango los va a
   seguir mostrando. Lo único que cambia es el historial de esta herramienta.

   Se marcan SOLO los 12 lotes ejecutados por el desarrollo. Los otros 3
   movimientos aplicados (00506164 y 00506173 de Mblanco, y 00506171 de
   Sgarcia) son acciones del equipo y quedan visibles a propósito.
   ============================================================================ */

IF COL_LENGTH('dbo.EB_TransferDepositoLote', 'EsPrueba') IS NULL
    ALTER TABLE dbo.EB_TransferDepositoLote
        ADD EsPrueba BIT NOT NULL CONSTRAINT DF_EBTDL_EsPrueba DEFAULT 0;
GO

/* Los 12 lotes del desarrollo, por comprobante interno.
   Van listados uno por uno a propósito: es más largo que un rango de fechas,
   pero deja constancia exacta de qué se marcó, y no puede arrastrar por error
   un movimiento del equipo que haya caído en el mismo día. */
UPDATE dbo.EB_TransferDepositoLote
   SET EsPrueba = 1
 WHERE ComprobInterno IN (
        '00506160',  -- v1: transferencia simple
        '00506161',  -- v1: artículo con partidas
        '00506162',  -- v1: devolución de la anterior, vía HTTP
        '00506163',  -- v1: devolución de partidas (rama UPDATE en destino)
        '00506165',  -- v2: transferencia simple, mismo código
        '00506166',  -- v2: recodificación
        '00506167',  -- v2: recodificación en el lugar
        '00506168',  -- v2: devolución de la anterior
        '00506169',  -- v2: devolución de la recodificación
        '00506170',  -- v2: devolución de la transferencia
        '00506174',  -- v3: fila armada por el modo escaneo
        '00506175'   -- v3: devolución de la anterior
       );
GO

SELECT EsPrueba, COUNT(*) AS Lotes
FROM dbo.EB_TransferDepositoLote
WHERE Estado = 2
GROUP BY EsPrueba;
GO
