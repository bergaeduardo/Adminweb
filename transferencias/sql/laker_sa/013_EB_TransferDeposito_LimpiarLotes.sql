/* ============================================================================
   EB_TransferDeposito_LimpiarLotes
   Servidor: XL-TANGO   Base: LAKER_SA

   Purga los lotes ABANDONADOS por antigüedad: los que quedaron cargados a
   medias, validados y nunca ejecutados, o con error. Reemplaza al TRUNCATE
   global que usa la herramienta de muestras (ese TRUNCATE es lo que hace que
   dos usuarios concurrentes se pisen el lote).

   ATENCIÓN — ESTAS TABLAS NO SON STAGING DESCARTABLE:
   los lotes con Estado = 2 (aplicados) son EL HISTORIAL de la herramienta.
   Son la única fuente de "qué se movió, quién lo movió y cuándo", y de ahí
   salen los totales de la pantalla de historial. NUNCA se borran.

   La versión original de este SP borraba por fecha sin mirar el Estado, o sea
   que se habría llevado el historial. No llegó a pasar porque nunca se agendó,
   pero es la razón de este comentario: si alguien vuelve a tocar el DELETE,
   el filtro por Estado tiene que quedar.

   El DELETE TOP (500) mantiene la operación acotada, para que una limpieza no
   pueda convertirse nunca en un bloqueo largo sobre las tablas.
   El detalle se va solo por el ON DELETE CASCADE de la FK.
   ============================================================================ */

CREATE OR ALTER PROCEDURE dbo.EB_TransferDeposito_LimpiarLotes
    @Dias INT = 15
AS
BEGIN
    SET NOCOUNT ON;

    DELETE TOP (500) FROM dbo.EB_TransferDepositoLote
    WHERE FechaAlta < DATEADD(DAY, -@Dias, GETDATE())
      AND Estado <> 2;   -- 2 = aplicado: es el historial, no se toca

    SELECT @@ROWCOUNT AS LotesEliminados;
END
GO
