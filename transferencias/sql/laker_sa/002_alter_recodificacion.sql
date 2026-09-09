/* ============================================================================
   v2: el artículo puede CAMBIAR entre origen y destino (recodificación con
   movimiento). Agrega el lado destino al staging.
   Servidor: XL-TANGO   Base: LAKER_SA
   Idempotente y aditivo: se puede re-ejecutar, y no rompe los lotes que ya
   están aplicados (todas las columnas nuevas son NULLables).

   POR QUÉ NO SE RENOMBRAN LAS COLUMNAS VIEJAS:
   `Articulo`, `ArticuloN`, `IdArticuloWms`, `Cantidad` y `UsaPartida` pasan a
   ser EL LADO DE ORIGEN. Renombrarlas a Art*Origen obligaría a migrar los
   lotes ya aplicados en producción sin ganar nada funcional, así que se dejan
   con el nombre que tienen y la asimetría queda documentada acá y en el README.

   La collation va EXPLÍCITA (Latin1_General_BIN, la de las tablas de Tango)
   por el mismo motivo que en 001_tablas.sql: hay cuatro collations en juego y
   la default de la base no coincide con la de sta19/sta20/sta10.
   ============================================================================ */

/* --- entrada, tal como viene del Excel -------------------------------------
   Más ancha que los 15 caracteres reales de un código: la basura tiene que
   ENTRAR y reportarse como error de fila, no reventar el INSERT. */
IF COL_LENGTH('dbo.EB_TransferDepositoDet', 'ArtDestino') IS NULL
    ALTER TABLE dbo.EB_TransferDepositoDet
        ADD ArtDestino VARCHAR(30) COLLATE Latin1_General_BIN NULL;
GO

/* Cantidad de alta. Se pide por separado de la baja como doble control de
   tipeo: la validación exige que coincidan. DECIMAL y no INT porque
   sta19.cant_stock y sta10.cantidad son DECIMAL_TG. */
IF COL_LENGTH('dbo.EB_TransferDepositoDet', 'CantAlta') IS NULL
    ALTER TABLE dbo.EB_TransferDepositoDet
        ADD CantAlta DECIMAL(18,4) NULL;
GO

/* --- resueltos por la validación ------------------------------------------ */
IF COL_LENGTH('dbo.EB_TransferDepositoDet', 'ArtDestinoN') IS NULL
    ALTER TABLE dbo.EB_TransferDepositoDet
        ADD ArtDestinoN VARCHAR(15) COLLATE Latin1_General_BIN NULL;
GO

IF COL_LENGTH('dbo.EB_TransferDepositoDet', 'IdArtDestinoWms') IS NULL
    ALTER TABLE dbo.EB_TransferDepositoDet
        ADD IdArtDestinoWms INT NULL;
GO

IF COL_LENGTH('dbo.EB_TransferDepositoDet', 'UsaPartidaDestino') IS NULL
    ALTER TABLE dbo.EB_TransferDepositoDet
        ADD UsaPartidaDestino BIT NULL;
GO

/* --- compatibilidad con los lotes viejos ----------------------------------
   Los lotes creados por la v1 tienen ArtDestino/CantAlta en NULL porque en esa
   versión el código y la cantidad no podían cambiar. Se rellenan con los
   valores de origen para que signifiquen lo mismo que significaban, y para que
   cualquier consulta histórica sobre el lado destino no devuelva NULL. */
UPDATE dbo.EB_TransferDepositoDet
   SET ArtDestino = Articulo,
       CantAlta   = Cantidad
 WHERE ArtDestino IS NULL
   AND CantAlta IS NULL
   AND Articulo IS NOT NULL;
GO
