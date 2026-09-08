/* ============================================================================
   EB_TransferDeposito_Procesar
   Servidor: XL-TANGO   Base: LAKER_SA

   Lo ÚNICO que llama Django. Orquesta, es dueño de la transacción y del
   applock, y define el contrato de retorno.

   CONTRATO: devuelve SIEMPRE dos resultsets, en este orden:
     1) filas con problema (vacío si el lote está limpio):
        Fila, DepOrigen, UbicOrigen, DepDestino, UbicDestino, Articulo,
        Cantidad, Resultado
     2) una única fila de resumen:
        Ok, FilasProcesadas, FilasConError, IdTarea, NroComprobante,
        ComprobInterno, Mensaje

   RAISERROR/THROW queda reservado para FALLAS TÉCNICAS, nunca para datos malos
   del usuario. Así, del lado de Python, una excepción significa sin ambigüedad
   "falla de sistema" y los datos malos son filas comunes que se iteran. (La
   herramienta de muestras hace lo contrario: hay que parsear el texto de un
   django.db.Error para saber qué fila estaba mal.)

   SET NOCOUNT ON es obligatorio: sin eso pyodbc ve los row counts como
   resultsets fantasma y nextset() se pasa de largo los datos reales.
   ============================================================================ */

CREATE OR ALTER PROCEDURE dbo.EB_TransferDeposito_Procesar
    @IdLote      UNIQUEIDENTIFIER,
    @Usuario     VARCHAR(50),
    @Host        VARCHAR(50) = 'TRANSFER-DEP',
    @SoloValidar BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @Errores INT = 0, @Estado TINYINT, @Aplicado BIT = 0,
            @IdTarea INT = NULL, @Prox VARCHAR(20) = NULL, @ProxInt VARCHAR(8) = NULL,
            @Mensaje VARCHAR(500) = NULL, @lock INT,
            /* Sobreviven al ROLLBACK; los usa el CATCH para compensar. */
            @IdTareaAplic INT = NULL, @ComprobIntAplic VARCHAR(8) = NULL;

    BEGIN TRY
        SELECT @Estado = Estado FROM dbo.EB_TransferDepositoLote WHERE IdLote = @IdLote;

        IF @Estado IS NULL
            THROW 51000, 'El lote indicado no existe.', 1;

        /* Idempotencia: si ya se aplicó, se devuelve el mismo resultado en vez
           de volver a mover stock. Un F5 o un doble clic quedan inocuos. */
        IF @Estado = 2
        BEGIN
            SELECT Fila, DepOrigen, UbicOrigen, DepDestino, UbicDestino,
                   Articulo, Cantidad, Resultado
              FROM dbo.EB_TransferDepositoDet
             WHERE IdLote = @IdLote AND 1 = 0;

            SELECT CAST(1 AS BIT) AS Ok,
                   Filas          AS FilasProcesadas,
                   0              AS FilasConError,
                   IdTarea, NroComprobante, ComprobInterno,
                   'El lote ya había sido aplicado. Numero de Tarea: '
                       + CAST(ISNULL(IdTarea, 0) AS VARCHAR(20)) AS Mensaje
              FROM dbo.EB_TransferDepositoLote
             WHERE IdLote = @IdLote;

            RETURN 0;
        END

        /* ============ FASE 1: validación, FUERA de la transacción ==========
           Las lecturas remotas son lo caro; no queremos sostener locks sobre
           sta19 mientras corren.                                            */
        EXEC dbo.EB_TransferDeposito_Validar @IdLote, 0;

        SELECT @Errores = COUNT(*)
          FROM dbo.EB_TransferDepositoDet
         WHERE IdLote = @IdLote AND Estado > 0;

        IF @Errores > 0
        BEGIN
            UPDATE dbo.EB_TransferDepositoLote SET Estado = 3, Mensaje = NULL WHERE IdLote = @IdLote;
            SET @Mensaje = CAST(@Errores AS VARCHAR(10)) + ' fila(s) con errores. No se aplicó ningún movimiento.';
            GOTO Salida;
        END

        IF @SoloValidar = 1
        BEGIN
            UPDATE dbo.EB_TransferDepositoLote SET Estado = 1, Mensaje = NULL WHERE IdLote = @IdLote;
            SET @Mensaje = 'Validación OK.';
            GOTO Salida;
        END

        /* ============ FASE 2: aplicación, serializada y transaccional ====== */
        BEGIN TRANSACTION;

            /* Serializa SOLO el aplicado; cargar y validar siguen en paralelo.
               Resuelve tres cosas de una: la carrera del MAX(id_Tarea), los
               deadlocks entre lotes que tocan las mismas filas de sta19 en
               orden inverso, y la ventana entre validar y aplicar. */
            EXEC @lock = sp_getapplock
                 @Resource = 'EB_TransferDeposito_Aplicar',
                 @LockMode = 'Exclusive',
                 @LockOwner = 'Transaction',
                 @LockTimeout = 60000;

            IF @lock < 0
                THROW 51001, 'Otro usuario está aplicando una transferencia en este momento. Reintentá en unos segundos.', 1;

            /* Recheck bajo lock: el stock pudo cambiar entre la fase 1 y la 2
               (TOCTOU). Acá sta19/sta10 se leen con UPDLOCK/HOLDLOCK. */
            EXEC dbo.EB_TransferDeposito_Validar @IdLote, 1;

            SELECT @Errores = COUNT(*)
              FROM dbo.EB_TransferDepositoDet
             WHERE IdLote = @IdLote AND Estado > 0;

            IF @Errores > 0
            BEGIN
                ROLLBACK TRANSACTION;
                /* El rollback deshizo las marcas del recheck, así que se
                   vuelven a estampar para poder devolverlas al usuario. */
                EXEC dbo.EB_TransferDeposito_Validar @IdLote, 0;
                UPDATE dbo.EB_TransferDepositoLote SET Estado = 3,
                       Mensaje = 'El stock cambió durante el proceso; no se aplicó nada.'
                 WHERE IdLote = @IdLote;
                SELECT @Errores = COUNT(*) FROM dbo.EB_TransferDepositoDet
                 WHERE IdLote = @IdLote AND Estado > 0;
                SET @Mensaje = 'El stock cambió durante el proceso; no se aplicó nada. Volvé a validar.';
                GOTO Salida;
            END

            /* Los OUTPUT se capturan en variables porque sobreviven a un
               ROLLBACK; el CATCH los necesita para borrar con precisión lo
               que se haya escrito en el WMS. */
            EXEC dbo.EB_TransferDeposito_Aplicar
                 @IdLote, @Usuario, @Host,
                 @IdTareaOut = @IdTareaAplic OUTPUT,
                 @ComprobIntOut = @ComprobIntAplic OUTPUT;

        COMMIT TRANSACTION;

        SET @Aplicado = 1;

        SELECT @IdTarea = IdTarea, @Prox = NroComprobante, @ProxInt = ComprobInterno
          FROM dbo.EB_TransferDepositoLote WHERE IdLote = @IdLote;

        SET @Mensaje = 'Numero de Tarea: ' + CAST(ISNULL(@IdTarea, 0) AS VARCHAR(20));

        BEGIN TRY
            EXEC dbo.EB_LogOperation
                 @ProcedureName = 'EB_TransferDeposito_Procesar',
                 @Action = 'COMPLETE',
                 @Parameters = @Mensaje;
        END TRY
        BEGIN CATCH
            /* El log no debe hacer fallar una transferencia ya aplicada. */
        END CATCH

Salida:
        SELECT Fila, DepOrigen, UbicOrigen, DepDestino, UbicDestino,
               Articulo, Cantidad, Resultado
          FROM dbo.EB_TransferDepositoDet
         WHERE IdLote = @IdLote AND Estado > 0
         ORDER BY Fila;

        SELECT CAST(@Aplicado AS BIT)                     AS Ok,
               (SELECT COUNT(*) FROM dbo.EB_TransferDepositoDet WHERE IdLote = @IdLote) AS FilasProcesadas,
               @Errores                                    AS FilasConError,
               @IdTarea                                    AS IdTarea,
               @Prox                                       AS NroComprobante,
               @ProxInt                                    AS ComprobInterno,
               @Mensaje                                    AS Mensaje;

        RETURN 0;
    END TRY
    BEGIN CATCH
        DECLARE @xs INT = XACT_STATE();
        IF @xs <> 0 ROLLBACK TRANSACTION;

        /* COMPENSACIÓN: si el rollback distribuido no llegó al linked server
           (MSDTC caído, promoción deshabilitada), se borran las filas que
           escribimos en el WMS. Best-effort y fuera de transacción: es la red
           de seguridad para que Tango y el WMS no queden descuadrados.

           OJO, ESTO SE VERIFICÓ EN PRODUCCIÓN Y ES IMPORTANTE: id_Tarea NO
           identifica un lote de forma única. Se calcula como MAX(id_Tarea)+1 y
           otros procesos del WMS hacen lo mismo en paralelo, así que hay
           colisiones reales (se observó una fila 'Ajuste Masivo PICKING-...'
           ajena compartiendo id_Tarea con una transferencia nuestra). Un
           DELETE solo por id_Tarea BORRARÍA MOVIMIENTOS DE OTROS.
           Por eso se discrimina además por NCompInt, que es el comprobante
           interno del talonario 850 y sí es único de este lote — y que además
           las filas ajenas dejan en NULL. */
        IF @IdTareaAplic IS NOT NULL AND NULLIF(LTRIM(RTRIM(@ComprobIntAplic)), '') IS NOT NULL
        BEGIN
            BEGIN TRY
                DELETE FROM [XL-SALES\SQLEXPRESS].[UbicacionesStockMvc].dbo.Movimientos
                 WHERE id_Tarea = @IdTareaAplic
                   AND NCompInt = @ComprobIntAplic;
            END TRY
            BEGIN CATCH
                /* Se registra abajo; no re-lanzar acá. */
            END CATCH
        END

        DECLARE @ErrMsg NVARCHAR(MAX) = ERROR_MESSAGE();
        DECLARE @ErrLine INT = ERROR_LINE();

        UPDATE dbo.EB_TransferDepositoLote
           SET Estado = 4, FechaProceso = GETDATE(), Mensaje = LEFT(@ErrMsg, 500)
         WHERE IdLote = @IdLote;

        BEGIN TRY
            EXEC dbo.EB_LogError
                 @ErrorProcedure = 'EB_TransferDeposito_Procesar',
                 @ErrorLine = @ErrLine,
                 @ErrorMessage = @ErrMsg,
                 @RootCause = 'Transferencia entre depositos';
        END TRY
        BEGIN CATCH
        END CATCH

        ;THROW;
    END CATCH
END
GO
