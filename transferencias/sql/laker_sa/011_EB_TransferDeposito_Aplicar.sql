/* ============================================================================
   EB_TransferDeposito_Aplicar
   Servidor: XL-TANGO   Base: LAKER_SA

   Aplica un lote YA VALIDADO. No valida nada: el orquestador
   (EB_TransferDeposito_Procesar) garantiza que se llama sin filas en error y
   dentro de una transacción con applock.

   Registra la transferencia como AJUSTE DOBLE bajo un único comprobante
   (talonario 850 / TCOMP_IN_S='AJ'): un renglón 'S' en el depósito de origen y
   un renglón 'E' en el de destino, que es lo pedido.

   Qué se reusa y qué no:
     - EB_InsertarEncMovimientoV1.2  -> SE REUSA (dueño del contrato de sta14 y
       de la numeración del talonario 850). Devuelve un resultset, no OUTPUT
       params, así que se captura con INSERT ... EXEC igual que hace
       EB_RecodificacionV1.2.
     - EB_InsertardetallecomprobanteAjuste -> NO se llama. Se copia su lista de
       columnas de sta20, pero es fila-por-fila, deriva el tipo_mov del signo
       (acá cada pata necesita su propio cod_deposi y un S/E explícito) y llama
       dos veces a GuardarLogEnTXTConValor: I/O de archivo DENTRO de la
       transacción, no transaccional, y un lock de archivo abortaría el lote.
     - EB_InsertarMovimientosWMS -> NO se llama: hardcodea
       id_ubicacionOrigen = 0 y hace un INSERT remoto por fila.
     - ProcesarPartidas -> NO se llama: solo sabe incrementar/crear una partida
       en el destino, no descontarla del origen. Ver sección 5.

   ORDEN DELIBERADO: todo lo de Tango primero, la escritura remota al WMS
   ÚLTIMA. Si algo falla antes, el rollback local alcanza y nunca se escribió
   nada remoto.
   ============================================================================ */

CREATE OR ALTER PROCEDURE dbo.EB_TransferDeposito_Aplicar
    @IdLote     UNIQUEIDENTIFIER,
    @Usuario    VARCHAR(50),
    @Host       VARCHAR(50),
    /* OUTPUT y no solo grabados en la tabla del lote: si algo falla, el
       ROLLBACK deshace el UPDATE de la tabla, pero el valor de una variable
       sobrevive. El orquestador los necesita en su CATCH para poder borrar
       con precisión lo que hayamos escrito en el WMS. */
    @IdTareaOut     INT         = NULL OUTPUT,
    @ComprobIntOut  VARCHAR(8)  = NULL OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @Fecha DATETIME = GETDATE();

    /* ---------------------------------------------------------------- 1
       Cabecera en Tango: un solo comprobante para todo el lote.             */
    DECLARE @enc TABLE (proximo VARCHAR(100), proxinterno VARCHAR(500));
    INSERT @enc (proximo, proxinterno)
    EXEC [dbo].[EB_InsertarEncMovimientoV1.2] @Usuario, 1, @Host;

    /* Sin LTRIM: Tango guarda n_comp con un espacio inicial (p.ej.
       ' 0200500012893'), así que se conserva textual para que el comprobante
       que registramos coincida exactamente con el de sta14. */
    DECLARE @PROXIMO     VARCHAR(20) = (SELECT proximo     FROM @enc);
    DECLARE @PROXINTERNO VARCHAR(8)  = (SELECT proxinterno FROM @enc);

    IF NULLIF(LTRIM(RTRIM(@PROXINTERNO)), '') IS NULL
        THROW 51010, 'No se pudo generar el comprobante interno del ajuste.', 1;

    /* Se publica en cuanto se conoce, antes de cualquier escritura remota. */
    SET @ComprobIntOut = @PROXINTERNO;

    /* ---------------------------------------------------------------- 2
       id_Tarea del WMS.

       OJO: id_Tarea NO identifica un lote de forma única. Otros procesos del
       WMS calculan MAX(id_Tarea)+1 igual que nosotros y hay colisiones reales
       (se observó en producción una fila 'Ajuste Masivo PICKING-...' ajena
       compartiendo id_Tarea con una transferencia de esta herramienta). El
       applock serializa solo nuestras propias corridas, no las de terceros.
       Para identificar NUESTRAS filas en el WMS se usa NCompInt, que es el
       comprobante interno del talonario 850 y sí es único de este lote.      */
    DECLARE @IdTarea INT = (
        SELECT ISNULL(MAX(id_Tarea), 0) + 1
        FROM [XL-SALES\SQLEXPRESS].[UbicacionesStockMvc].dbo.Movimientos
    );

    SET @IdTareaOut = @IdTarea;

    /* ---------------------------------------------------------------- 3
       sta20: DOS renglones por fila del lote, en un solo INSERT set-based.
       deposi_dde lleva el depósito de la contraparte, igual que hace Tango en
       una transferencia nativa (verificado en un comprobante TI real: la fila
       'E' del depósito 05 lleva deposi_dde='01' y la 'S' del 01 lleva '05').
       Ningún AJ existente lo usa, pero V_ResumenStock_WC lo consume con LEFT
       JOIN, así que llenarlo solo enriquece estas filas nuevas.             */
    INSERT INTO dbo.sta20 (
        can_equi_v, cant_dev, cant_oc, cant_pend, cant_scrap, cantidad,
        cod_articu, cod_deposi, deposi_dde, equivalenc, fecha_mov,
        n_rengl_oc, n_rengl_s, ncomp_in_s, plista_rem, ppp_ex, ppp_lo,
        precio, precio_rem, tcomp_in_s, tipo_mov, cant_factu, dcto_factu,
        cant_dev_2, cant_pend_2, cantidad_2, cant_factu_2, id_medida_stock,
        unidad_medida_seleccionada, precio_remito_ventas, cant_oc_2,
        rengl_padr, promocion, precio_adicional_kit, talonario_oc
    )
    SELECT
        1, 0, 0, 0, 0, l.Cantidad,
        l.ArticuloN, l.CodDeposi, l.DeposiDde, 1, @Fecha,
        0, ROW_NUMBER() OVER (ORDER BY l.Fila, l.Orden), @PROXINTERNO, 0, 0, 0,
        0, 0, 'AJ', l.TipoMov, 0, 0,
        0, 0, 0, 0, 7,
        'P', 0, 0,
        0, 0, 0, 0
    FROM (
        /* La pata 'S' lleva el código y la cantidad de ORIGEN, la 'E' los de
           DESTINO. Si el código cambia, en el comprobante se ve el viejo
           saliendo y el nuevo entrando: eso es una recodificación. */
        SELECT Fila, 1 AS Orden, 'S' AS TipoMov,
               DepOrigenN  AS CodDeposi, DepDestinoN AS DeposiDde,
               ArticuloN, Cantidad
        FROM dbo.EB_TransferDepositoDet WHERE IdLote = @IdLote
        UNION ALL
        SELECT Fila, 2, 'E',
               DepDestinoN, DepOrigenN,
               ArtDestinoN, CantAlta
        FROM dbo.EB_TransferDepositoDet WHERE IdLote = @IdLote
    ) l;

    /* ---------------------------------------------------------------- 4
       sta19: delta agregado por (depósito, artículo).
       Una reubicación del MISMO código dentro del MISMO depósito da delta 0 y
       se descarta con el HAVING: sta19 no conoce ubicaciones. En cambio una
       recodificación en el lugar (mismo depósito, código distinto) sí produce
       dos deltas: -1 al código viejo y +1 al nuevo.                          */
    DECLARE @Delta TABLE (
        COD_DEPOSI CHAR(2)     COLLATE Latin1_General_BIN,
        COD_ARTICU VARCHAR(15) COLLATE Latin1_General_BIN,
        Delta      DECIMAL(18,4),
        PRIMARY KEY (COD_DEPOSI, COD_ARTICU)
    );
    INSERT @Delta (COD_DEPOSI, COD_ARTICU, Delta)
    SELECT x.COD_DEPOSI, x.COD_ARTICU, SUM(x.Cant)
    FROM (
        SELECT DepOrigenN AS COD_DEPOSI, ArticuloN AS COD_ARTICU, -Cantidad AS Cant
        FROM dbo.EB_TransferDepositoDet WHERE IdLote = @IdLote
        UNION ALL
        SELECT DepDestinoN, ArtDestinoN, CantAlta
        FROM dbo.EB_TransferDepositoDet WHERE IdLote = @IdLote
    ) x
    GROUP BY x.COD_DEPOSI, x.COD_ARTICU
    HAVING SUM(x.Cant) <> 0;

    UPDATE s
       SET s.cant_stock = ISNULL(s.cant_stock, 0) + d.Delta
    FROM dbo.sta19 s
    JOIN @Delta d ON s.COD_DEPOSI = d.COD_DEPOSI AND s.COD_ARTICU = d.COD_ARTICU;

    /* Filas de sta19 que no existían. Solo pueden ser altas en el destino
       (Delta > 0): la validación garantizó que el origen tiene stock, y para
       tenerlo su fila de sta19 tiene que existir. Se delega en ActualizarStock
       para no duplicar la lista de columnas NOT NULL de sta19. */
    DECLARE @dep CHAR(2), @art VARCHAR(15), @cant DECIMAL(18,4);
    DECLARE cFaltantes CURSOR LOCAL FAST_FORWARD FOR
        SELECT d.COD_DEPOSI, d.COD_ARTICU, d.Delta
        FROM @Delta d
        WHERE d.Delta > 0
          AND NOT EXISTS (SELECT 1 FROM dbo.sta19 s
                          WHERE s.COD_DEPOSI = d.COD_DEPOSI AND s.COD_ARTICU = d.COD_ARTICU);
    OPEN cFaltantes;
    FETCH NEXT FROM cFaltantes INTO @dep, @art, @cant;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        EXEC dbo.ActualizarStock @dep, @art, @cant;
        FETCH NEXT FROM cFaltantes INTO @dep, @art, @cant;
    END
    CLOSE cFaltantes;
    DEALLOCATE cFaltantes;

    /* ---------------------------------------------------------------- 5
       sta10: partidas. Se separa en dos casos, porque UNA PARTIDA PERTENECE A
       UN ARTÍCULO y por lo tanto no se puede arrastrar a otro código:

       5a. MISMO CÓDIGO, distinto depósito -> la partida se MUEVE conservando su
           número, fecha y fecha_vto. Es el comportamiento de la v1.
       5b. CÓDIGO DISTINTO (recodificación) -> las dos puntas son independientes:
           se descuenta la partida del código viejo y el código nuevo recibe SU
           PROPIA partida (la última conocida en sof_partidas, vía
           CrearNuevaPartida). Además cada punta se hace solo si ESE artículo
           usa partidas: origen y destino pueden diferir en usa_partid.

       No se toca nada si el código y el depósito son los mismos: ahí la partida
       no se mueve de (artículo, depósito), solo cambia de estante.

       Se recorre la demanda AGREGADA, no fila por fila: en estos depósitos el
       91% de los pares tiene una sola partida y ninguno más de dos, así que son
       1-2 iteraciones internas.
       Orden de consumo: FIFO por vencimiento real, dejando al final las que
       tienen el centinela 1800-01-01 (muy comunes acá), con id_sta10 como
       desempate determinístico.                                             */
    DECLARE @idOrigen INT, @nPart VARCHAR(25), @dispo DECIMAL(18,4),
            @fec DATETIME, @fecVto DATETIME, @toma DECIMAL(18,4),
            @resta DECIMAL(18,4),
            @pArt VARCHAR(15), @pOri CHAR(2), @pDes CHAR(2), @pCant DECIMAL(18,4),
            @msgPart VARCHAR(200), @tipoPart INT;

    /* ---- 5a. mismo código, se mueve la partida ---- */
    DECLARE @MoveIgual TABLE (
        COD_ARTICU  VARCHAR(15) COLLATE Latin1_General_BIN,
        DEP_ORIGEN  CHAR(2)     COLLATE Latin1_General_BIN,
        DEP_DESTINO CHAR(2)     COLLATE Latin1_General_BIN,
        Cantidad    DECIMAL(18,4),
        PRIMARY KEY (COD_ARTICU, DEP_ORIGEN, DEP_DESTINO)
    );
    INSERT @MoveIgual (COD_ARTICU, DEP_ORIGEN, DEP_DESTINO, Cantidad)
    SELECT ArticuloN, DepOrigenN, DepDestinoN, SUM(Cantidad)
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote
      AND UsaPartida = 1
      AND ArticuloN = ArtDestinoN
      AND DepOrigenN <> DepDestinoN
    GROUP BY ArticuloN, DepOrigenN, DepDestinoN;

    DECLARE cMove CURSOR LOCAL FAST_FORWARD FOR
        SELECT COD_ARTICU, DEP_ORIGEN, DEP_DESTINO, Cantidad FROM @MoveIgual;
    OPEN cMove;
    FETCH NEXT FROM cMove INTO @pArt, @pOri, @pDes, @pCant;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @resta = @pCant;

        WHILE @resta > 0
        BEGIN
            SET @idOrigen = NULL;

            SELECT TOP (1)
                   @idOrigen = p.id_sta10, @nPart = p.n_partida,
                   @dispo = p.cantidad, @fec = p.fecha, @fecVto = p.fecha_vto
            FROM dbo.sta10 p
            WHERE p.COD_ARTICU = @pArt AND p.COD_DEPOSI = @pOri AND p.cantidad > 0
            ORDER BY CASE WHEN p.fecha_vto <= '18010101' THEN 1 ELSE 0 END,
                     p.fecha_vto, p.id_sta10;

            IF @idOrigen IS NULL
                THROW 51011, 'No hay partidas suficientes en el origen para completar la transferencia.', 1;

            SET @toma = CASE WHEN @dispo < @resta THEN @dispo ELSE @resta END;

            UPDATE dbo.sta10 SET cantidad = cantidad - @toma WHERE id_sta10 = @idOrigen;

            /* Destino: MISMA partida. Si ya existe se incrementa, si no se crea
               con el mismo n_partida, fecha y fecha_vto que la del origen. */
            IF EXISTS (SELECT 1 FROM dbo.sta10
                       WHERE COD_ARTICU = @pArt AND COD_DEPOSI = @pDes
                         AND n_partida = @nPart COLLATE Modern_Spanish_CI_AI)
                UPDATE dbo.sta10
                   SET cantidad = cantidad + @toma
                 WHERE id_sta10 = (
                        SELECT MAX(id_sta10) FROM dbo.sta10
                        WHERE COD_ARTICU = @pArt AND COD_DEPOSI = @pDes
                          AND n_partida = @nPart COLLATE Modern_Spanish_CI_AI);
            ELSE
                INSERT INTO dbo.sta10
                    (filler, cant_despa, cantidad, cod_articu, cod_deposi,
                     costo_bloq, costo_ex, costo_lo, n_partida, saldo_ant,
                     exp_saldo, fecha, fecha_vto, cantidad_2,
                     saldo_ant_stock_2, cant_despa_2)
                VALUES
                    ('', 0, @toma, @pArt, @pDes,
                     0, 0, 0, @nPart, 0,
                     0, @fec, @fecVto, 0,
                     0, 0);

            SET @resta = @resta - @toma;
        END

        FETCH NEXT FROM cMove INTO @pArt, @pOri, @pDes, @pCant;
    END
    CLOSE cMove;
    DEALLOCATE cMove;

    /* ---- 5b-i. código distinto: BAJA de la partida del código viejo ---- */
    DECLARE @BajaDistinto TABLE (
        COD_ARTICU VARCHAR(15) COLLATE Latin1_General_BIN,
        COD_DEPOSI CHAR(2)     COLLATE Latin1_General_BIN,
        Cantidad   DECIMAL(18,4),
        PRIMARY KEY (COD_ARTICU, COD_DEPOSI)
    );
    INSERT @BajaDistinto (COD_ARTICU, COD_DEPOSI, Cantidad)
    SELECT ArticuloN, DepOrigenN, SUM(Cantidad)
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote AND UsaPartida = 1 AND ArticuloN <> ArtDestinoN
    GROUP BY ArticuloN, DepOrigenN;

    DECLARE cBaja CURSOR LOCAL FAST_FORWARD FOR
        SELECT COD_ARTICU, COD_DEPOSI, Cantidad FROM @BajaDistinto;
    OPEN cBaja;
    FETCH NEXT FROM cBaja INTO @pArt, @pOri, @pCant;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @resta = @pCant;

        WHILE @resta > 0
        BEGIN
            SET @idOrigen = NULL;

            SELECT TOP (1) @idOrigen = p.id_sta10, @dispo = p.cantidad
            FROM dbo.sta10 p
            WHERE p.COD_ARTICU = @pArt AND p.COD_DEPOSI = @pOri AND p.cantidad > 0
            ORDER BY CASE WHEN p.fecha_vto <= '18010101' THEN 1 ELSE 0 END,
                     p.fecha_vto, p.id_sta10;

            IF @idOrigen IS NULL
                THROW 51012, 'No hay partidas suficientes del codigo de origen para completar la recodificacion.', 1;

            SET @toma = CASE WHEN @dispo < @resta THEN @dispo ELSE @resta END;
            UPDATE dbo.sta10 SET cantidad = cantidad - @toma WHERE id_sta10 = @idOrigen;
            SET @resta = @resta - @toma;
        END

        FETCH NEXT FROM cBaja INTO @pArt, @pOri, @pCant;
    END
    CLOSE cBaja;
    DEALLOCATE cBaja;

    /* ---- 5b-ii. código distinto: ALTA en la partida propia del código nuevo ---- */
    DECLARE @AltaDistinto TABLE (
        COD_ARTICU VARCHAR(15) COLLATE Latin1_General_BIN,
        COD_DEPOSI CHAR(2)     COLLATE Latin1_General_BIN,
        Cantidad   DECIMAL(18,4),
        PRIMARY KEY (COD_ARTICU, COD_DEPOSI)
    );
    INSERT @AltaDistinto (COD_ARTICU, COD_DEPOSI, Cantidad)
    SELECT ArtDestinoN, DepDestinoN, SUM(CantAlta)
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote AND UsaPartidaDestino = 1 AND ArticuloN <> ArtDestinoN
    GROUP BY ArtDestinoN, DepDestinoN;

    DECLARE cAlta CURSOR LOCAL FAST_FORWARD FOR
        SELECT COD_ARTICU, COD_DEPOSI, Cantidad FROM @AltaDistinto;
    OPEN cAlta;
    FETCH NEXT FROM cAlta INTO @pArt, @pDes, @pCant;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        IF EXISTS (SELECT 1 FROM dbo.sta10
                   WHERE COD_ARTICU = @pArt AND COD_DEPOSI = @pDes AND cantidad > 0)
        BEGIN
            /* Ya tiene partida en ese depósito: se acredita en la última. */
            UPDATE dbo.sta10
               SET cantidad = cantidad + @pCant
             WHERE id_sta10 = (
                    SELECT MAX(id_sta10) FROM dbo.sta10
                    WHERE COD_ARTICU = @pArt AND COD_DEPOSI = @pDes AND cantidad > 0);
        END
        ELSE
        BEGIN
            /* No tiene: se le crea una a partir de SU propia última partida
               conocida (sof_partidas). La validación ya garantizó que existe;
               igual se chequea el resultado y se aborta si no — que es
               justamente el error que la herramienta de muestras se come en
               silencio y por el que sta10 quedó desfasado contra sta19. */
            SET @msgPart = NULL;
            SET @tipoPart = 0;

            EXEC dbo.CrearNuevaPartida
                 @COD_ARTICU = @pArt,
                 @DEP_DESTINO = @pDes,
                 @CANTIDAD = @pCant,
                 @MENSAJERESULTADO = @msgPart OUTPUT,
                 @TIPORESULTADO = @tipoPart OUTPUT;

            IF @tipoPart = 1
                THROW 51013, 'No se pudo crear la partida del codigo de destino: no tiene ninguna partida de referencia.', 1;
        END

        FETCH NEXT FROM cAlta INTO @pArt, @pDes, @pCant;
    END
    CLOSE cAlta;
    DEALLOCATE cAlta;

    /* ---------------------------------------------------------------- 6
       WMS: un solo INSERT ... SELECT para todo el lote. Va ÚLTIMO a propósito
       (ver cabecera).

       Movimientos tiene UN SOLO artículo por fila, así que:
         - código y cantidad iguales -> UNA fila con ambas ubicaciones reales,
           que es como el WMS representa una transferencia (un evento);
         - código o cantidad distintos -> DOS filas: la salida del código viejo
           (id_ubicacionDestino = 0) y la entrada del nuevo
           (id_ubicacionOrigen = 0). Es el mismo patrón con el que la
           herramienta de muestras registra las altas.
       El saldo por ubicación se calcula como SUM(destino) - SUM(origen), así
       que las dos formas dan el mismo resultado en los saldos.               */
    DECLARE @HashUsuario NVARCHAR(500) = (
        SELECT TOP (1) CAST(au.Id AS NVARCHAR(500))
        FROM [XL-SALES\SQLEXPRESS].[UbicacionesStockMvc].dbo.AspNetUsers au
        WHERE au.UserName = @Usuario
    );

    /* Fallback al usuario 'admin' del WMS: de los usuarios habilitados de esta
       herramienta solo algunos existen en el WMS. El usuario real queda igual
       registrado en sta14.usuario y en la auditoría de Django. */
    IF @HashUsuario IS NULL
        SET @HashUsuario = '8a0f9e14-7804-4b6b-8b2d-24fc16d7512a';

    INSERT INTO [XL-SALES\SQLEXPRESS].[UbicacionesStockMvc].dbo.Movimientos
        (id_ubicacionDestino, id_ubicacionOrigen, id_Articulo, id_usuarios,
         id_Comprobante, Cantidad_Asosciada, Origen_Tango, detalle, Fecha,
         NCompInt, NComp, id_Tarea, IdEstadoArticuloOrigen, IdEstadoArticuloDestino)
    SELECT m.IdUbicDestino, m.IdUbicOrigen, m.IdArticulo, @HashUsuario,
           0, m.Cantidad, '',
           LEFT(m.Detalle, 100),
           @Fecha,
           @PROXINTERNO, @PROXIMO, @IdTarea, 1, 1
    FROM (
        /* Caso simple: mismo código y misma cantidad -> un solo evento. */
        SELECT d.IdUbicDestino, d.IdUbicOrigen, d.IdArticuloWms AS IdArticulo, d.Cantidad,
               'Transferencia ' + d.DepOrigenN + '->' + d.DepDestinoN + ' ' + d.ArticuloN AS Detalle
        FROM dbo.EB_TransferDepositoDet d
        WHERE d.IdLote = @IdLote
          AND d.ArticuloN = d.ArtDestinoN
          AND d.Cantidad = d.CantAlta

        UNION ALL

        /* Recodificación: salida del código viejo. */
        SELECT 0, d.IdUbicOrigen, d.IdArticuloWms, d.Cantidad,
               'Recodif salida ' + d.DepOrigenN + ' ' + d.ArticuloN + '=>' + d.ArtDestinoN
        FROM dbo.EB_TransferDepositoDet d
        WHERE d.IdLote = @IdLote
          AND NOT (d.ArticuloN = d.ArtDestinoN AND d.Cantidad = d.CantAlta)

        UNION ALL

        /* Recodificación: entrada del código nuevo. */
        SELECT d.IdUbicDestino, 0, d.IdArtDestinoWms, d.CantAlta,
               'Recodif entrada ' + d.DepDestinoN + ' ' + d.ArtDestinoN + '<=' + d.ArticuloN
        FROM dbo.EB_TransferDepositoDet d
        WHERE d.IdLote = @IdLote
          AND NOT (d.ArticuloN = d.ArtDestinoN AND d.Cantidad = d.CantAlta)
    ) m;

    /* ---------------------------------------------------------------- 7
       Cierre del lote.                                                       */
    UPDATE dbo.EB_TransferDepositoLote
       SET Estado         = 2,
           FechaProceso   = @Fecha,
           IdTarea        = @IdTarea,
           NroComprobante = @PROXIMO,
           ComprobInterno = @PROXINTERNO,
           Filas          = (SELECT COUNT(*) FROM dbo.EB_TransferDepositoDet WHERE IdLote = @IdLote),
           Mensaje        = NULL
     WHERE IdLote = @IdLote;

    RETURN 0;
END
GO
