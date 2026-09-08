/* ============================================================================
   Transferencias entre depósitos - tablas de staging
   Servidor: XL-TANGO   Base: LAKER_SA
   Idempotente: se puede re-ejecutar sin efecto.

   NOTA SOBRE COLLATIONS (hay cuatro distintas en juego, y muerden):
     - tablas de Tango (sta19/sta20/sta10): Latin1_General_BIN
       ... salvo sta10.N_PARTIDA, que es Modern_Spanish_CI_AI
     - base LAKER_SA (default):             Modern_Spanish_CI_AI
     - tempdb (o sea COLLATE DATABASE_DEFAULT en una #tabla): Modern_Spanish_CI_AS
     - WMS UbicacionesStockMvc:             Modern_Spanish_CI_AS
   Las columnas de texto de estas tablas se declaran con Latin1_General_BIN
   EXPLÍCITO para que joineen directo contra las de Tango sin "Cannot resolve
   the collation conflict". Es binaria (case y accent sensitive), y por eso
   todo se normaliza a UPPER + TRIM antes de comparar — que es además cómo
   compara Tango internamente.
   ============================================================================ */

IF OBJECT_ID('dbo.EB_TransferDepositoLote') IS NULL
BEGIN
    CREATE TABLE dbo.EB_TransferDepositoLote (
        IdLote          UNIQUEIDENTIFIER NOT NULL,
        Usuario         VARCHAR(50)      NOT NULL,
        Host            VARCHAR(50)      NULL,
        FechaAlta       DATETIME         NOT NULL CONSTRAINT DF_EBTDL_Fecha DEFAULT GETDATE(),
        FechaProceso    DATETIME         NULL,
        /* 0=cargado 1=validado_ok 2=aplicado 3=error_validacion 4=error_tecnico */
        Estado          TINYINT          NOT NULL CONSTRAINT DF_EBTDL_Estado DEFAULT 0,
        Filas           INT              NULL,
        IdTarea         INT              NULL,          -- id_Tarea del WMS
        NroComprobante  VARCHAR(20)      NULL,          -- @PROXIMO      (talonario 850)
        ComprobInterno  VARCHAR(8)       NULL,          -- @PROXINTERNO  -> sta20.ncomp_in_s
        Mensaje         VARCHAR(500)     NULL,
        CONSTRAINT PK_EB_TransferDepositoLote PRIMARY KEY CLUSTERED (IdLote)
    );

    /* Solo para la purga por antigüedad. */
    CREATE NONCLUSTERED INDEX IX_EBTDL_FechaAlta
        ON dbo.EB_TransferDepositoLote (FechaAlta);
END
GO

IF OBJECT_ID('dbo.EB_TransferDepositoDet') IS NULL
BEGIN
    CREATE TABLE dbo.EB_TransferDepositoDet (
        IdLote          UNIQUEIDENTIFIER NOT NULL,
        Fila            INT              NOT NULL,   -- número de fila que ve el usuario

        /* --- entrada, TAL COMO VINO ---------------------------------------
           A propósito más anchas que las columnas reales (un depósito son 2
           caracteres, un artículo 15): la basura que venga del Excel tiene que
           ENTRAR y reportarse como error de fila, no reventar el INSERT con
           "String or binary data would be truncated", que no es atribuible a
           ninguna fila en particular.                                       */
        DepOrigen       VARCHAR(10)      COLLATE Latin1_General_BIN NULL,
        UbicOrigen      VARCHAR(30)      COLLATE Latin1_General_BIN NULL,
        DepDestino      VARCHAR(10)      COLLATE Latin1_General_BIN NULL,
        UbicDestino     VARCHAR(30)      COLLATE Latin1_General_BIN NULL,
        Articulo        VARCHAR(30)      COLLATE Latin1_General_BIN NULL,
        /* DECIMAL y no INT: sta19.cant_stock y sta10.cantidad son DECIMAL_TG.
           El contrato de entrada es entero positivo, pero eso se valida y se
           informa, no se trunca en silencio. */
        Cantidad        DECIMAL(18,4)    NULL,

        /* --- normalizado / resuelto por la validación --------------------- */
        DepOrigenN      CHAR(2)          COLLATE Latin1_General_BIN NULL,
        DepDestinoN     CHAR(2)          COLLATE Latin1_General_BIN NULL,
        ArticuloN       VARCHAR(15)      COLLATE Latin1_General_BIN NULL,
        IdUbicOrigen    INT              NULL,
        IdUbicDestino   INT              NULL,
        IdArticuloWms   INT              NULL,
        UsaPartida      BIT              NULL,

        Estado          TINYINT          NOT NULL CONSTRAINT DF_EBTDD_Estado DEFAULT 0, -- 0 ok / 1 error
        Resultado       VARCHAR(500)     NULL,

        /* Única PK necesaria: todo acceso es WHERE IdLote = @IdLote, o sea un
           rango contiguo. */
        CONSTRAINT PK_EB_TransferDepositoDet PRIMARY KEY CLUSTERED (IdLote, Fila),
        CONSTRAINT FK_EBTDD_Lote FOREIGN KEY (IdLote)
            REFERENCES dbo.EB_TransferDepositoLote (IdLote) ON DELETE CASCADE
    );
END
GO
