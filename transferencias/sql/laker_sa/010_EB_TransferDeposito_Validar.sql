/* ============================================================================
   EB_TransferDeposito_Validar
   Servidor: XL-TANGO   Base: LAKER_SA

   Valida un lote completo en UNA pasada set-based. No devuelve resultset (así
   se puede llamar desde otro SP sin contaminar su salida): deja el veredicto
   en EB_TransferDepositoDet.Estado / .Resultado.

   Por qué no se recorre fila por fila como EB_ActualizarTemAjusteRecodificacion:
   ese SP hace ~4 viajes remotos y una agregación sobre 2,8M de filas POR FILA.
   Acá los datos de referencia se traen en 3 viajes y todo lo demás son joins
   locales, así el costo es casi independiente de la cantidad de filas.

   @DentroDeTran = 1 -> relee sta19/sta10 con UPDLOCK/HOLDLOCK, para el recheck
   dentro de la transacción de aplicación (el stock pudo cambiar en el medio).
   ============================================================================ */

CREATE OR ALTER PROCEDURE dbo.EB_TransferDeposito_Validar
    @IdLote       UNIQUEIDENTIFIER,
    @DentroDeTran BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    /* La collation explícita también acá: una tabla variable sin COLLATE toma
       la default de LAKER_SA (Modern_Spanish_CI_AI) y chocaría contra las
       columnas del staging, que son Latin1_General_BIN. */
    DECLARE @DepHabilitados TABLE (Cod CHAR(2) COLLATE Latin1_General_BIN PRIMARY KEY);
    INSERT @DepHabilitados (Cod) VALUES ('04'), ('06'), ('10'), ('20');

    /* ---------------------------------------------------------------- 0
       Reset y normalización. Se limpia el veredicto anterior para que el SP
       sea re-ejecutable sobre el mismo lote.                                */
    UPDATE d SET
        Estado        = 0,
        Resultado     = NULL,
        DepOrigenN    = CASE WHEN LEN(LTRIM(RTRIM(ISNULL(d.DepOrigen, '')))) BETWEEN 1 AND 2
                             THEN RIGHT('00' + LTRIM(RTRIM(d.DepOrigen)), 2) END,
        DepDestinoN   = CASE WHEN LEN(LTRIM(RTRIM(ISNULL(d.DepDestino, '')))) BETWEEN 1 AND 2
                             THEN RIGHT('00' + LTRIM(RTRIM(d.DepDestino)), 2) END,
        ArticuloN     = CASE WHEN LEN(LTRIM(RTRIM(ISNULL(d.Articulo, '')))) BETWEEN 1 AND 15
                             THEN UPPER(LTRIM(RTRIM(d.Articulo))) END,
        UbicOrigen    = UPPER(LTRIM(RTRIM(ISNULL(d.UbicOrigen, '')))),
        UbicDestino   = UPPER(LTRIM(RTRIM(ISNULL(d.UbicDestino, '')))),
        IdUbicOrigen  = NULL,
        IdUbicDestino = NULL,
        IdArticuloWms = NULL,
        UsaPartida    = NULL
    FROM dbo.EB_TransferDepositoDet d
    WHERE d.IdLote = @IdLote;

    IF NOT EXISTS (SELECT 1 FROM dbo.EB_TransferDepositoDet WHERE IdLote = @IdLote)
        RETURN 0;

    /* ---------------------------------------------------------------- 1
       Datos de referencia del WMS: se traen ENTEROS de un viaje y se indexan
       localmente. Medido: 2.327 ubicaciones en 0,04 s y 71.078 artículos en
       0,05 s. Esto además resuelve que Cod_Ubicacion no tenga índice en el
       WMS: nunca se hace seek remoto sobre esa columna.
       El COLLATE explícito evita "Cannot resolve the collation conflict" al
       joinear strings que vienen de la otra base.                            */
    CREATE TABLE #Ubic (
        id_Ubicacion  INT PRIMARY KEY,
        Cod_Ubicacion VARCHAR(30) COLLATE Latin1_General_BIN,
        Num_Deposito  CHAR(2) COLLATE Latin1_General_BIN
    );
    INSERT #Ubic (id_Ubicacion, Cod_Ubicacion, Num_Deposito)
    SELECT u.id_Ubicacion,
           UPPER(LTRIM(RTRIM(u.Cod_Ubicacion))) COLLATE Latin1_General_BIN,
           RIGHT('00' + LTRIM(RTRIM(ISNULL(u.Num_Deposito, ''))), 2)
    FROM [XL-SALES\SQLEXPRESS].[UbicacionesStockMvc].dbo.Ubicacion u
    WHERE LEN(LTRIM(RTRIM(ISNULL(u.Cod_Ubicacion, '')))) > 0;

    CREATE UNIQUE INDEX IX_Ubic_Cod ON #Ubic (Cod_Ubicacion);

    CREATE TABLE #ArtWms (
        id_Articulo  INT PRIMARY KEY,
        Cod_Articulo VARCHAR(30) COLLATE Latin1_General_BIN
    );
    INSERT #ArtWms (id_Articulo, Cod_Articulo)
    SELECT a.id_Articulo, UPPER(LTRIM(RTRIM(a.Cod_Articulo))) COLLATE Latin1_General_BIN
    FROM [XL-SALES\SQLEXPRESS].[UbicacionesStockMvc].dbo.Articulo a
    WHERE LEN(LTRIM(RTRIM(ISNULL(a.Cod_Articulo, '')))) > 0;

    CREATE INDEX IX_ArtWms_Cod ON #ArtWms (Cod_Articulo);

    /* ---------------------------------------------------------------- 2
       Resolución de ids.                                                    */
    UPDATE d SET IdUbicOrigen = u.id_Ubicacion
    FROM dbo.EB_TransferDepositoDet d
    JOIN #Ubic u ON u.Cod_Ubicacion = d.UbicOrigen
    WHERE d.IdLote = @IdLote;

    UPDATE d SET IdUbicDestino = u.id_Ubicacion
    FROM dbo.EB_TransferDepositoDet d
    JOIN #Ubic u ON u.Cod_Ubicacion = d.UbicDestino
    WHERE d.IdLote = @IdLote;

    UPDATE d SET IdArticuloWms = a.id_Articulo
    FROM dbo.EB_TransferDepositoDet d
    JOIN #ArtWms a ON a.Cod_Articulo = d.ArticuloN
    WHERE d.IdLote = @IdLote;

    /* ---------------------------------------------------------------- 3
       Artículos válidos en Tango. Misma consulta que usa la herramienta de
       muestras (excluye carpetas ocultas con DESCRIP NOT LIKE '[_]%'), pero
       una sola vez para todo el lote.
       El DISTINCT es imprescindible: STA11ITC/STA11FLD es una relación de
       pertenencia a carpetas, así que un artículo en varias carpetas da filas
       repetidas y sin DISTINCT multiplicaría el lote en los joins.           */
    CREATE TABLE #ArtTango (
        COD_ARTICU VARCHAR(15) COLLATE Latin1_General_BIN PRIMARY KEY,
        usa_partid BIT
    );
    INSERT #ArtTango (COD_ARTICU, usa_partid)
    SELECT LTRIM(RTRIM(A.COD_ARTICU)) COLLATE Latin1_General_BIN,
           MAX(CAST(ISNULL(A.usa_partid, 0) AS TINYINT))
    FROM SJ_VIEW_STA11 A
    JOIN STA11ITC B ON A.COD_ARTICU = B.CODE
    JOIN STA11FLD C ON B.IDFOLDER = C.IDFOLDER
    WHERE C.DESCRIP NOT LIKE '[_]%'
      AND EXISTS (SELECT 1 FROM dbo.EB_TransferDepositoDet d
                  WHERE d.IdLote = @IdLote
                    AND d.ArticuloN = LTRIM(RTRIM(A.COD_ARTICU)) COLLATE Latin1_General_BIN)
    GROUP BY LTRIM(RTRIM(A.COD_ARTICU));

    UPDATE d SET UsaPartida = t.usa_partid
    FROM dbo.EB_TransferDepositoDet d
    JOIN #ArtTango t ON t.COD_ARTICU = d.ArticuloN
    WHERE d.IdLote = @IdLote;

    /* ---------------------------------------------------------------- 4
       Saldo por ubicación en el WMS.
       Se EMPUJA el agregado al servidor remoto con OPENQUERY. Joinear una
       tabla local contra [linked].Movimientos hace que el optimizador
       distribuido traiga las 2,8M de filas o emita una llamada por fila.
       Las listas son de enteros YA RESUELTOS, así que no hay texto del
       usuario en el SQL dinámico: no hay superficie de inyección.
       El producto cartesiano de las dos listas sobre-trae pares que no
       interesan, y está bien: se joinea localmente contra los pares exactos.
       Sobre-traer es mucho más barato que correlacionar remotamente.         */
    CREATE TABLE #SaldoUbic (
        id_Articulo  INT,
        id_Ubicacion INT,
        Saldo        DECIMAL(18,4),
        PRIMARY KEY (id_Articulo, id_Ubicacion)
    );

    DECLARE @arts VARCHAR(MAX), @ubis VARCHAR(MAX), @remoto NVARCHAR(MAX), @sql NVARCHAR(MAX);

    SELECT @arts = STRING_AGG(CAST(x AS VARCHAR(12)), ',')
    FROM (SELECT DISTINCT IdArticuloWms AS x FROM dbo.EB_TransferDepositoDet
          WHERE IdLote = @IdLote AND IdArticuloWms IS NOT NULL) a;

    SELECT @ubis = STRING_AGG(CAST(x AS VARCHAR(12)), ',')
    FROM (SELECT DISTINCT IdUbicOrigen AS x FROM dbo.EB_TransferDepositoDet
          WHERE IdLote = @IdLote AND IdUbicOrigen IS NOT NULL) u;

    IF @arts IS NOT NULL AND @ubis IS NOT NULL
    BEGIN
        SET @remoto = N'SELECT id_Articulo, id_Ubic, SUM(q) AS Saldo FROM ('
            + N'SELECT id_Articulo, id_ubicacionDestino AS id_Ubic, Cantidad_Asosciada AS q '
            + N'FROM UbicacionesStockMvc.dbo.Movimientos '
            + N'WHERE id_Articulo IN (' + @arts + N') AND id_ubicacionDestino IN (' + @ubis + N') '
            + N'UNION ALL '
            + N'SELECT id_Articulo, id_ubicacionOrigen, -Cantidad_Asosciada '
            + N'FROM UbicacionesStockMvc.dbo.Movimientos '
            + N'WHERE id_Articulo IN (' + @arts + N') AND id_ubicacionOrigen IN (' + @ubis + N')'
            + N') t GROUP BY id_Articulo, id_Ubic';

        SET @sql = N'INSERT #SaldoUbic (id_Articulo, id_Ubicacion, Saldo) '
                 + N'SELECT id_Articulo, id_Ubic, Saldo FROM OPENQUERY([XL-SALES\SQLEXPRESS], '''
                 + REPLACE(@remoto, '''', '''''') + N''')';

        EXEC sp_executesql @sql;
    END

    /* ---------------------------------------------------------------- 5
       Stock de depósito (sta19) y partidas (sta10) del ORIGEN.
       El predicado compara las columnas sin envolverlas en RTRIM para que el
       índice IX_0 (COD_DEPOSI, COD_ARTICU) siga siendo seekable; los CHAR de
       Tango comparan con semántica de blank-padding, así que matchean igual. */
    CREATE TABLE #Sta19 (
        COD_DEPOSI CHAR(2) COLLATE Latin1_General_BIN,
        COD_ARTICU VARCHAR(15) COLLATE Latin1_General_BIN,
        cant_stock DECIMAL(18,4),
        PRIMARY KEY (COD_DEPOSI, COD_ARTICU)
    );

    CREATE TABLE #Sta10 (
        COD_DEPOSI CHAR(2) COLLATE Latin1_General_BIN,
        COD_ARTICU VARCHAR(15) COLLATE Latin1_General_BIN,
        Disponible DECIMAL(18,4),
        PRIMARY KEY (COD_DEPOSI, COD_ARTICU)
    );

    IF @DentroDeTran = 1
    BEGIN
        INSERT #Sta19 (COD_DEPOSI, COD_ARTICU, cant_stock)
        SELECT s.COD_DEPOSI, LTRIM(RTRIM(s.COD_ARTICU)), ISNULL(s.cant_stock, 0)
        FROM dbo.sta19 s WITH (UPDLOCK, HOLDLOCK)
        WHERE EXISTS (SELECT 1 FROM dbo.EB_TransferDepositoDet d
                      WHERE d.IdLote = @IdLote
                        AND d.DepOrigenN = s.COD_DEPOSI
                        AND d.ArticuloN = s.COD_ARTICU);

        INSERT #Sta10 (COD_DEPOSI, COD_ARTICU, Disponible)
        SELECT p.COD_DEPOSI, LTRIM(RTRIM(p.COD_ARTICU)), SUM(p.cantidad)
        FROM dbo.sta10 p WITH (UPDLOCK, HOLDLOCK)
        WHERE p.cantidad > 0
          AND EXISTS (SELECT 1 FROM dbo.EB_TransferDepositoDet d
                      WHERE d.IdLote = @IdLote
                        AND d.DepOrigenN = p.COD_DEPOSI
                        AND d.ArticuloN = p.COD_ARTICU
                        AND d.UsaPartida = 1)
        GROUP BY p.COD_DEPOSI, LTRIM(RTRIM(p.COD_ARTICU));
    END
    ELSE
    BEGIN
        INSERT #Sta19 (COD_DEPOSI, COD_ARTICU, cant_stock)
        SELECT s.COD_DEPOSI, LTRIM(RTRIM(s.COD_ARTICU)), ISNULL(s.cant_stock, 0)
        FROM dbo.sta19 s
        WHERE EXISTS (SELECT 1 FROM dbo.EB_TransferDepositoDet d
                      WHERE d.IdLote = @IdLote
                        AND d.DepOrigenN = s.COD_DEPOSI
                        AND d.ArticuloN = s.COD_ARTICU);

        INSERT #Sta10 (COD_DEPOSI, COD_ARTICU, Disponible)
        SELECT p.COD_DEPOSI, LTRIM(RTRIM(p.COD_ARTICU)), SUM(p.cantidad)
        FROM dbo.sta10 p
        WHERE p.cantidad > 0
          AND EXISTS (SELECT 1 FROM dbo.EB_TransferDepositoDet d
                      WHERE d.IdLote = @IdLote
                        AND d.DepOrigenN = p.COD_DEPOSI
                        AND d.ArticuloN = p.COD_ARTICU
                        AND d.UsaPartida = 1)
        GROUP BY p.COD_DEPOSI, LTRIM(RTRIM(p.COD_ARTICU));
    END

    /* ---------------------------------------------------------------- 6
       Demanda AGREGADA. Un control fila por fila es insuficiente: tres filas
       que sacan 2 unidades cada una de una ubicación que tiene 5 deben fallar.

       La asimetría entre los dos controles es intencional:
         - UBICACIÓN: demanda BRUTA. No se acreditan los ingresos del mismo
           lote porque Movimientos no tiene orden intra-lote y acreditarlos
           permitiría validar ciclos físicamente imposibles (A->B y B->A).
         - DEPÓSITO: demanda NETA. sta19 no conoce ubicaciones, así que una
           reubicación interna (04/UB1 -> 04/UB2) no consume stock de
           depósito; usar demanda bruta acá daría rechazos falsos.            */
    CREATE TABLE #DemUbic (
        IdUbicOrigen  INT,
        IdArticuloWms INT,
        Requerido     DECIMAL(18,4),
        Disponible    DECIMAL(18,4),
        PRIMARY KEY (IdUbicOrigen, IdArticuloWms)
    );
    INSERT #DemUbic (IdUbicOrigen, IdArticuloWms, Requerido, Disponible)
    SELECT d.IdUbicOrigen, d.IdArticuloWms, SUM(d.Cantidad), ISNULL(s.Saldo, 0)
    FROM dbo.EB_TransferDepositoDet d
    LEFT JOIN #SaldoUbic s
           ON s.id_Articulo = d.IdArticuloWms AND s.id_Ubicacion = d.IdUbicOrigen
    WHERE d.IdLote = @IdLote
      AND d.IdUbicOrigen IS NOT NULL
      AND d.IdArticuloWms IS NOT NULL
      AND d.Cantidad > 0
    GROUP BY d.IdUbicOrigen, d.IdArticuloWms, ISNULL(s.Saldo, 0);

    CREATE TABLE #DemDep (
        COD_DEPOSI CHAR(2) COLLATE Latin1_General_BIN,
        COD_ARTICU VARCHAR(15) COLLATE Latin1_General_BIN,
        NetoSalida DECIMAL(18,4),
        PRIMARY KEY (COD_DEPOSI, COD_ARTICU)
    );
    INSERT #DemDep (COD_DEPOSI, COD_ARTICU, NetoSalida)
    SELECT x.COD_DEPOSI, x.COD_ARTICU, SUM(x.Cant)
    FROM (
        SELECT DepOrigenN AS COD_DEPOSI, ArticuloN AS COD_ARTICU, Cantidad AS Cant
        FROM dbo.EB_TransferDepositoDet
        WHERE IdLote = @IdLote AND DepOrigenN IS NOT NULL AND ArticuloN IS NOT NULL AND Cantidad > 0
        UNION ALL
        SELECT DepDestinoN, ArticuloN, -Cantidad
        FROM dbo.EB_TransferDepositoDet
        WHERE IdLote = @IdLote AND DepDestinoN IS NOT NULL AND ArticuloN IS NOT NULL AND Cantidad > 0
    ) x
    GROUP BY x.COD_DEPOSI, x.COD_ARTICU
    HAVING SUM(x.Cant) > 0;   -- solo importan los depósitos que quedan netos negativos

    /* ---------------------------------------------------------------- 7
       Un único conjunto de errores, y después un solo UPDATE.
       Cada fila acumula TODOS sus mensajes, no solo el primero, para que el
       usuario corrija el Excel de una sola pasada.                           */
    CREATE TABLE #Err (Fila INT, Prioridad TINYINT, Mensaje VARCHAR(300));

    /* --- estructurales --- */
    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT Fila, 10, 'la cantidad debe ser un entero mayor a cero'
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote AND (Cantidad IS NULL OR Cantidad <= 0 OR Cantidad <> FLOOR(Cantidad));

    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT Fila, 10, 'faltan datos obligatorios (ubicaciones y artículo)'
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote
      AND (NULLIF(UbicOrigen, '') IS NULL OR NULLIF(UbicDestino, '') IS NULL OR ArticuloN IS NULL);

    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT Fila, 11, 'el depósito de origen "' + ISNULL(DepOrigen, '') + '" no está habilitado (04/06/10/20)'
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote
      AND (DepOrigenN IS NULL OR DepOrigenN NOT IN (SELECT Cod FROM @DepHabilitados));

    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT Fila, 11, 'el depósito de destino "' + ISNULL(DepDestino, '') + '" no está habilitado (04/06/10/20)'
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote
      AND (DepDestinoN IS NULL OR DepDestinoN NOT IN (SELECT Cod FROM @DepHabilitados));

    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT Fila, 12, 'el origen y el destino son la misma ubicación'
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote AND UbicOrigen = UbicDestino AND DepOrigenN = DepDestinoN;

    /* --- existencia de ubicaciones --- */
    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT Fila, 20, 'la ubicación de origen "' + UbicOrigen + '" no existe en el WMS'
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote AND IdUbicOrigen IS NULL AND NULLIF(UbicOrigen, '') IS NOT NULL;

    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT Fila, 20, 'la ubicación de destino "' + UbicDestino + '" no existe en el WMS'
    FROM dbo.EB_TransferDepositoDet
    WHERE IdLote = @IdLote AND IdUbicDestino IS NULL AND NULLIF(UbicDestino, '') IS NOT NULL;

    /* --- cross-check ubicación <-> depósito declarado --- */
    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT d.Fila, 21,
           'la ubicación ' + d.UbicOrigen + ' pertenece al depósito ' + u.Num_Deposito
           + ', no al ' + d.DepOrigenN
    FROM dbo.EB_TransferDepositoDet d
    JOIN #Ubic u ON u.id_Ubicacion = d.IdUbicOrigen
    WHERE d.IdLote = @IdLote AND d.DepOrigenN IS NOT NULL AND u.Num_Deposito <> d.DepOrigenN;

    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT d.Fila, 21,
           'la ubicación ' + d.UbicDestino + ' pertenece al depósito ' + u.Num_Deposito
           + ', no al ' + d.DepDestinoN
    FROM dbo.EB_TransferDepositoDet d
    JOIN #Ubic u ON u.id_Ubicacion = d.IdUbicDestino
    WHERE d.IdLote = @IdLote AND d.DepDestinoN IS NOT NULL AND u.Num_Deposito <> d.DepDestinoN;

    /* --- artículo --- */
    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT d.Fila, 30, 'el artículo "' + d.ArticuloN + '" no existe en Tango'
    FROM dbo.EB_TransferDepositoDet d
    WHERE d.IdLote = @IdLote AND d.ArticuloN IS NOT NULL
      AND NOT EXISTS (SELECT 1 FROM #ArtTango t WHERE t.COD_ARTICU = d.ArticuloN);

    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT d.Fila, 30, 'el artículo "' + d.ArticuloN + '" no existe en el WMS'
    FROM dbo.EB_TransferDepositoDet d
    WHERE d.IdLote = @IdLote AND d.ArticuloN IS NOT NULL AND d.IdArticuloWms IS NULL;

    /* --- stock: ubicación de origen (bruto) --- */
    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT d.Fila, 40,
           'stock insuficiente en la ubicación ' + d.UbicOrigen + ' para ' + d.ArticuloN
           + ': el lote requiere ' + CONVERT(VARCHAR(20), CAST(m.Requerido AS DECIMAL(18,2)))
           + ' y hay ' + CONVERT(VARCHAR(20), CAST(m.Disponible AS DECIMAL(18,2)))
    FROM dbo.EB_TransferDepositoDet d
    JOIN #DemUbic m ON m.IdUbicOrigen = d.IdUbicOrigen AND m.IdArticuloWms = d.IdArticuloWms
    WHERE d.IdLote = @IdLote AND m.Requerido > m.Disponible;

    /* --- stock: depósito de origen (neto) --- */
    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT d.Fila, 41,
           'stock insuficiente en el depósito ' + d.DepOrigenN + ' para ' + d.ArticuloN
           + ': el lote requiere (neto) ' + CONVERT(VARCHAR(20), CAST(m.NetoSalida AS DECIMAL(18,2)))
           + ' y Tango tiene ' + CONVERT(VARCHAR(20), CAST(ISNULL(s.cant_stock, 0) AS DECIMAL(18,2)))
    FROM dbo.EB_TransferDepositoDet d
    JOIN #DemDep m ON m.COD_DEPOSI = d.DepOrigenN AND m.COD_ARTICU = d.ArticuloN
    LEFT JOIN #Sta19 s ON s.COD_DEPOSI = d.DepOrigenN AND s.COD_ARTICU = d.ArticuloN
    WHERE d.IdLote = @IdLote AND m.NetoSalida > ISNULL(s.cant_stock, 0);

    /* --- stock: partidas del origen (neto), solo para artículos con partidas.
       Cubre el caso en que sta19 dice que hay stock pero las partidas no lo
       respaldan (ya hay 22 partidas con cantidad negativa en estos depósitos,
       así que no se puede asumir que sta10 y sta19 estén cuadrados).         */
    INSERT #Err (Fila, Prioridad, Mensaje)
    SELECT d.Fila, 42,
           'partidas insuficientes en el depósito ' + d.DepOrigenN + ' para ' + d.ArticuloN
           + ': el lote requiere (neto) ' + CONVERT(VARCHAR(20), CAST(m.NetoSalida AS DECIMAL(18,2)))
           + ' y las partidas suman ' + CONVERT(VARCHAR(20), CAST(ISNULL(p.Disponible, 0) AS DECIMAL(18,2)))
    FROM dbo.EB_TransferDepositoDet d
    JOIN #DemDep m ON m.COD_DEPOSI = d.DepOrigenN AND m.COD_ARTICU = d.ArticuloN
    LEFT JOIN #Sta10 p ON p.COD_DEPOSI = d.DepOrigenN AND p.COD_ARTICU = d.ArticuloN
    WHERE d.IdLote = @IdLote AND d.UsaPartida = 1 AND m.NetoSalida > ISNULL(p.Disponible, 0);

    /* --- veredicto: un solo UPDATE, todos los mensajes de la fila --- */
    UPDATE d
       SET Estado    = 1,
           Resultado = LEFT('Fila N° ' + CAST(d.Fila AS VARCHAR(10)) + ': ' + e.Msgs, 500)
    FROM dbo.EB_TransferDepositoDet d
    CROSS APPLY (
        SELECT STRING_AGG(x.Mensaje, ' | ') WITHIN GROUP (ORDER BY x.Prioridad) AS Msgs
        FROM #Err x WHERE x.Fila = d.Fila
    ) e
    WHERE d.IdLote = @IdLote AND e.Msgs IS NOT NULL;

    RETURN 0;
END
GO
