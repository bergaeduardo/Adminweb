/* ============================================================================
   Índice para la pantalla de historial
   Servidor: XL-TANGO   Base: LAKER_SA
   Idempotente y aditivo.

   Todas las consultas del historial filtran por Estado = 2 (aplicados) y
   ordenan/filtran por FechaProceso, así que este índice cubre las tres:
   totales por depósito, totales por artículo y el detalle paginado.

   A 35 filas no cambia nada; se crea desde el principio para que no haga
   falta acordarse cuando la tabla crezca.
   ============================================================================ */

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_EBTDL_Estado_FechaProceso'
      AND object_id = OBJECT_ID('dbo.EB_TransferDepositoLote')
)
    CREATE NONCLUSTERED INDEX IX_EBTDL_Estado_FechaProceso
        ON dbo.EB_TransferDepositoLote (Estado, FechaProceso)
        INCLUDE (Usuario, NroComprobante, IdTarea);
GO
