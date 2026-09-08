/* ============================================================================
   EB_TransferDeposito_LimpiarLotes
   Servidor: XL-TANGO   Base: LAKER_SA

   Purga por antigüedad, en lugar del TRUNCATE global que usa la herramienta de
   muestras (ese TRUNCATE es lo que hace que dos usuarios concurrentes se pisen
   el lote).

   El DELETE TOP (500) mantiene la operación acotada, para que una limpieza no
   pueda convertirse nunca en un bloqueo largo sobre las tablas de staging.
   El detalle se va solo por el ON DELETE CASCADE de la FK.
   ============================================================================ */

CREATE OR ALTER PROCEDURE dbo.EB_TransferDeposito_LimpiarLotes
    @Dias INT = 15
AS
BEGIN
    SET NOCOUNT ON;

    DELETE TOP (500) FROM dbo.EB_TransferDepositoLote
    WHERE FechaAlta < DATEADD(DAY, -@Dias, GETDATE());

    SELECT @@ROWCOUNT AS LotesEliminados;
END
GO
