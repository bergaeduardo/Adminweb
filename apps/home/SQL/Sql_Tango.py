from django.db import connections

def validar_factManualCargada(sucursal,factura):
    with connections['mi_db_4'].cursor() as cursor:
        sql = '''
            SET DATEFORMAT DMY 
            DECLARE @COMPROBANTE VARCHAR(14) = ''' + "'" + factura + "'"+''';
            DECLARE @sucursal VARCHAR(5) = ''' + "'" + sucursal + "'"+''';
            DECLARE @terminal VARCHAR(20);
            DECLARE @factura INT;
            SET @terminal = SUBSTRING(@COMPROBANTE, 2, CHARINDEX('-', @COMPROBANTE) - 2);
            SET @factura = CAST(SUBSTRING(@COMPROBANTE, CHARINDEX('-', @COMPROBANTE) + 1, LEN(@COMPROBANTE))AS INT)-1;
            select COUNT(A.NComp) 
            from (
                SELECT CTA02.N_COMP AS NComp 
                FROM 
                CTA02 (NOLOCK)  
                LEFT JOIN CTA_TIPO_COMPROBANTE_VENTAS ON CTA02.T_COMP = CTA_TIPO_COMPROBANTE_VENTAS.IDENT_COMP 
                and CTA02.NRO_SUCURS = CTA_TIPO_COMPROBANTE_VENTAS.NRO_SUCURS  
                LEFT JOIN CTA_VENDEDOR ON CTA02.COD_VENDED = CTA_VENDEDOR.COD_VENDEDOR  
                LEFT JOIN CTA_CLIENTE ON CTA02.COD_CLIENT = CTA_CLIENTE.COD_CLIENTE 
                WHERE
                CTA02.ESTADO <> 'ANU' AND CTA02.T_COMP <> 'REC'  AND CTA02.COD_VENDED <> '**' 
                AND 
                ( (Fecha_Emis BETWEEN '01/01/2024' AND '31/12/2024')) AND TIPO_TALONARIO IN ( 'Manual' )
                AND CTA02.NRO_SUCURS = @sucursal
                AND CTA02.N_COMP LIKE '%'+CAST(@factura AS varchar(10))
                AND SUBSTRING(CTA02.N_COMP, 3, 4) = @terminal
                GROUP BY 
                CTA02.TIPO_TALONARIO , CTA02.TIPO_AUTORIZACION , SUBSTRING(CTA02.N_COMP, 3, 4) , 
                CTA02.T_COMP , CTA02.N_COMP , CTA02.TALONARIO  , CTA_TIPO_COMPROBANTE_VENTAS.DESCRIPCIO , 
                CTA02.IMPORTE , CTA02.NRO_SUCURS , CTA02.FECHA_EMIS
            ) A'''
        cursor.execute(sql)
        # print('Parametros de consulta: ' + str(sucursal) + ' ' + str(factura))
        resulatado = cursor.fetchone()
        # print(resulatado[0])
    return resulatado[0]

def validar_articulo(articulo):
    # verificar si es kit
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''select PROMO_MENU from STA11
                WHERE COD_ARTICU LIKE ''' + "'" + articulo + "%'"
        cursor.execute(sql)
        esKit = cursor.fetchone()

    if esKit[0] == 'P':
        with connections['mi_db_2'].cursor() as cursor:
            sql = '''SELECT COALESCE(
                        (SELECT TOP 1 DESCRIPCIO 
                        FROM SJ_ETIQUETAS_FINAL 
                        WHERE COD_ARTICU LIKE ''' + "'" + articulo + "'" + '''),
                    'ERROR') AS RESULT'''
            cursor.execute(sql)
            resultado = cursor.fetchone()
    else:
        with connections['mi_db_2'].cursor() as cursor:
            sql = '''SELECT COALESCE(
                        (SELECT TOP 1 DESCRIPCIO 
                        FROM SJ_ETIQUETAS_FINAL 
                        WHERE COD_ARTICU LIKE ''' + "'" + articulo[:11] + "%'" + '''),
                    'ERROR') AS RESULT'''
            cursor.execute(sql)
            resultado = cursor.fetchone()
    return resultado[0]

def obtenerInformacionArticulo(CodigoArt,DescripcionMetaTag):
    with connections['mi_db_2'].cursor() as cursor:
        sql = ''' EXEC SP_EB_DescArt_VtxAr '''+ "'" + CodigoArt + "'" + ',' + "'" + DescripcionMetaTag + "'"
        cursor.execute(sql)
        # print(sql)
        resulatado = cursor.fetchone()
        # print(resulatado[0])
    return resulatado[0]

def cargar_articulo(articulo, descripcion):
    # print('Cargar articulo: ' + articulo + ' ' + descripcion)
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''INSERT INTO SJ_T_ETIQUETAS_FINAL (COD_ARTICU, DESCRIPCIO) VALUES (''' + "'" + articulo + "'" + ',' + "'" + descripcion + "'" + ')'
        # print('sql: ' + sql)
        cursor.execute(sql)

def borrar_contTabla(nombre_tabla):
    with connections['mi_db_2'].cursor() as cursor:        
        sql = '''DELETE FROM '''+ nombre_tabla
        cursor.execute(sql)
    print('Se borro la tabla ' + nombre_tabla)

def validar_pedido(pedido,talon_pedido):
    talon_pedido = str(talon_pedido)
    pedido = ' 0000' + str(pedido)[-9:]
    with connections['mi_db_2'].cursor() as cursor:
        
        sql = '''SELECT COUNT(*) CONTAR FROM 
                    (
                    SELECT * FROM GVA21 WHERE TALON_PED = '''+ "'" + talon_pedido + "'"''' AND NRO_PEDIDO = '''+ "'" + pedido + "'"''' AND ESTADO = 2) A
                    '''
        cursor.execute(sql)
        # print(sql)
        resulatado = cursor.fetchone()
        # print(resulatado[0])
    return int(resulatado[0])

def validar_pedidoAsignado(pedido):
    with connections['mi_db_2'].cursor() as cursor:
        
        sql = """
                select count(NumeroPedido) from EB_TrackDetallePedidos_Mob
                WHERE NumeroPedido LIKE '%"""+ pedido + "'"""
        
        cursor.execute(sql)
        # print(sql)
        resulatado = cursor.fetchone()
        # print(resulatado[0])
    return int(resulatado[0])

def cerrar_pedido(talon_pedido,pedido):
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''EXEC RO_CERRAR_PEDIDOS '''+ "'" + talon_pedido + "','" + pedido + "'"
        # print(sql)
        cursor.execute(sql) # Guarda los cambios en la base de datos


# --- Categorias ---
def obtener_categorias():
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute("SELECT id_Categoria_VtxAr, nombre, codigo, PalabrasClave FROM EB_Categoria_VtxAr")
        return cursor.fetchall()
def crear_categoria(nombre, codigo, palabras_clave):
    with connections['mi_db_2'].cursor() as cursor:
        sql = "INSERT INTO EB_Categoria_VtxAr (nombre, codigo, PalabrasClave) VALUES (%s, %s, %s)"
        cursor.execute(sql, [nombre, codigo, palabras_clave])

def obtener_categoria(id_categoria):
    with connections['mi_db_2'].cursor() as cursor:
         sql = "SELECT id_Categoria_VtxAr, nombre, codigo, PalabrasClave FROM EB_Categoria_VtxAr WHERE id_Categoria_VtxAr = %s"
         cursor.execute(sql, [id_categoria])
         return cursor.fetchone()

def editar_categoria(id_categoria, nombre, codigo, palabras_clave):
    with connections['mi_db_2'].cursor() as cursor:
        sql = "UPDATE EB_Categoria_VtxAr SET nombre = %s, codigo = %s, PalabrasClave = %s WHERE id_Categoria_VtxAr = %s"
        cursor.execute(sql, [nombre, codigo, palabras_clave, id_categoria])
def eliminar_categoria(id_categoria):
    with connections['mi_db_2'].cursor() as cursor:
        sql = "DELETE FROM EB_Categoria_VtxAr WHERE id_Categoria_VtxAr = %s"
        cursor.execute(sql, [id_categoria])


# --- Subcategorias ---
def obtener_subcategorias():
    with connections['mi_db_2'].cursor() as cursor:
        sql = """
            SELECT 
                sub.id_subCat_VtxAr, sub.codigo, sub.nombre, sub.Keywords, 
                cat.nombre as categoria_nombre,st.DESC_CATEGORIA as categoria_tango_nombre
            FROM EB_subCat_VtxAr sub
             LEFT JOIN EB_Categoria_VtxAr cat ON sub.id_categoria_VtxAr = cat.id_Categoria_VtxAr
             LEFT JOIN SJ_CATEGORIAS st ON sub.id_categoria_Tango = st.ID

        """
        cursor.execute(sql)
        return cursor.fetchall()


def crear_subcategoria(codigo, nombre, keywords, id_categoria_vtxar, id_categoria_tango):
        with connections['mi_db_2'].cursor() as cursor:
            sql = """INSERT INTO EB_subCat_VtxAr (codigo, nombre, Keywords, id_categoria_VtxAr, id_categoria_Tango)
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, [codigo, nombre, keywords, id_categoria_vtxar, id_categoria_tango])

def obtener_subcategoria(id_subcategoria):
    with connections['mi_db_2'].cursor() as cursor:
         sql = "SELECT id_subCat_VtxAr, codigo, nombre, Keywords, id_categoria_VtxAr, id_categoria_Tango FROM EB_subCat_VtxAr WHERE id_subCat_VtxAr = %s"
         cursor.execute(sql, [id_subcategoria])
         return cursor.fetchone()
def editar_subcategoria(id_subcategoria, codigo, nombre, keywords, id_categoria_vtxar, id_categoria_tango):
     with connections['mi_db_2'].cursor() as cursor:
          sql = """UPDATE EB_subCat_VtxAr SET codigo = %s, nombre = %s, Keywords = %s,
                    id_categoria_VtxAr = %s, id_categoria_Tango = %s
                    WHERE id_subCat_VtxAr = %s
          """
          cursor.execute(sql, [codigo, nombre, keywords, id_categoria_vtxar, id_categoria_tango, id_subcategoria])

def eliminar_subcategoria(id_subcategoria):
     with connections['mi_db_2'].cursor() as cursor:
          sql = "DELETE FROM EB_subCat_VtxAr WHERE id_subCat_VtxAr = %s"
          cursor.execute(sql, [id_subcategoria])


# --- Relaciones ---
def obtener_relaciones():
    with connections['mi_db_2'].cursor() as cursor:
        sql = """
            SELECT
                ISNULL(SJ_CATEGORIAS.ID, '') AS ID,
                ISNULL(SJ_CATEGORIAS.DESC_CATEGORIA, '') AS CATEGORIA_Tango,
                ISNULL(Rubro.DESC_RUBRO, '') AS RUBRO_Tango,
                ISNULL(SubCatVtx.nombre, '') AS SUB_CATEGORIA_Vtex,
                ISNULL(SubCatVtx.codigo, '') AS codigo,
                ISNULL(SubCatVtx.id_subCat_VtxAr, 0) AS id_subCat_VtxAr,
                ISNULL(CatVtx.nombre, '') AS CATEGORIA_Vtex,
                ISNULL(CatVtx.codigo, '') AS codigo
            FROM
                SJ_CATEGORIAS
                LEFT JOIN EB_relacionCat_VtxAr AS Relacion ON SJ_CATEGORIAS.ID = Relacion.id_categoria_Tango
                LEFT JOIN EB_subCat_VtxAr AS SubCatVtx ON Relacion.id_subCat_VtxAr = SubCatVtx.id_subCat_VtxAr
                LEFT JOIN EB_Categoria_VtxAr AS CatVtx ON SubCatVtx.id_categoria_VtxAr = CatVtx.id_Categoria_VtxAr
                LEFT JOIN RO_V_RUBROS_CATEGORIAS_CODIFICACION AS Rubro ON SJ_CATEGORIAS.RUBRO = Rubro.RUBRO AND SJ_CATEGORIAS.CATEGORIA = Rubro.CATEGORIA
            """
        cursor.execute(sql)
        return cursor.fetchall()
def crear_relacion(id_categoria_tango, id_subcategoria):
    with connections['mi_db_2'].cursor() as cursor:
        sql = "INSERT INTO EB_relacionCat_VtxAr (id_categoria_Tango, id_subCat_VtxAr) VALUES (%s, %s)"
        cursor.execute(sql, [id_categoria_tango, id_subcategoria])
def obtener_relacion(id_categoria_tango, id_subcategoria):
    with connections['mi_db_2'].cursor() as cursor:
        sql = """
                select R.id_categoria_Tango,R.id_subCat_VtxAr,STR(CAT.ID) + ' - ' + CAT.DESC_CATEGORIA AS CAT_TANGO ,SUBCAT.nombre AS SUBCAT_Vtex 
                from EB_relacionCat_VtxAr AS R
                left join SJ_CATEGORIAS AS CAT ON R.id_categoria_Tango = CAT.ID
                LEFT JOIN EB_subCat_VtxAr SUBCAT ON R.id_subCat_VtxAr = SUBCAT.id_subCat_VtxAr
                WHERE R.id_categoria_Tango = %s AND R.id_subCat_VtxAr = %s
            """
        cursor.execute(sql, [id_categoria_tango,id_subcategoria])
        return cursor.fetchone()
def editar_relacion(id_categoria_tango_old,id_subcategoria_old, id_categoria_tango, id_subcategoria):
     with connections['mi_db_2'].cursor() as cursor:
          sql = """UPDATE EB_relacionCat_VtxAr SET id_categoria_Tango = %s, id_subCat_VtxAr = %s
                    WHERE id_categoria_Tango = %s AND id_subCat_VtxAr = %s"""
          cursor.execute(sql, [id_categoria_tango, id_subcategoria,id_categoria_tango_old,id_subcategoria_old])

def eliminar_relacion(id_categoria_tango, id_subcategoria):
    with connections['mi_db_2'].cursor() as cursor:
          sql = "DELETE FROM EB_relacionCat_VtxAr WHERE id_categoria_Tango = %s AND id_subCat_VtxAr = %s"
          cursor.execute(sql, [id_categoria_tango,id_subcategoria])

def obtener_sucursales_ecommerce():
    """Obtener todas las sucursales de ecommerce desde la tabla RO_T_DEPOSITOS_ECOMMERCE_TIENDAS"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = """SELECT NRO_SUCURSAL, SUCURSAL, COD_DEPOSI_PRINC, COD_DEPOSI_ECOMM, 
                        ACTIVO, FECHA_MODIF 
                 FROM RO_T_DEPOSITOS_ECOMMERCE_TIENDAS 
                 ORDER BY NRO_SUCURSAL"""
        cursor.execute(sql)
        return cursor.fetchall()

def activar_sucursal_ecommerce(nro_sucursal):
    """Activar una sucursal específica y desactivar todas las demás"""
    with connections['mi_db_2'].cursor() as cursor:
        # Primero desactivar todas las sucursales
        sql_desactivar = "UPDATE RO_T_DEPOSITOS_ECOMMERCE_TIENDAS SET ACTIVO = 0"
        cursor.execute(sql_desactivar)
        
        # Luego activar la sucursal específica y actualizar fecha
        sql_activar = """UPDATE RO_T_DEPOSITOS_ECOMMERCE_TIENDAS 
                        SET ACTIVO = 1, FECHA_MODIF = GETDATE() 
                        WHERE NRO_SUCURSAL = %s"""
        cursor.execute(sql_activar, [nro_sucursal])

def obtener_sucursal_activa():
    """Obtener la sucursal que está actualmente activa"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = """SELECT NRO_SUCURSAL, SUCURSAL, COD_DEPOSI_PRINC, COD_DEPOSI_ECOMM, 
                        ACTIVO, FECHA_MODIF 
                 FROM RO_T_DEPOSITOS_ECOMMERCE_TIENDAS 
                 WHERE ACTIVO = 1"""
        cursor.execute(sql)
        return cursor.fetchone()

def agregar_estado_no_confirmado():
    """Agregar estado NO CONFIRMADO a la tabla EstadoTurno si no existe"""
    with connections['mi_db_2'].cursor() as cursor:
        # Verificar si ya existe
        cursor.execute("SELECT id_estado FROM EstadoTurno WHERE nombre = 'NO CONFIRMADO'")
        resultado = cursor.fetchone()
        
        if resultado:
            return resultado[0]
        
        # Insertar nuevo estado
        sql = """
        INSERT INTO EstadoTurno 
        (nombre, descripcion, orden_ejecucion, es_requerido, permite_editar, color, activo, fecha_creacion, fecha_modificacion)
        VALUES 
        ('NO CONFIRMADO', 'Turno no confirmado a tiempo (30 min antes)', 99, 0, 0, '#dc3545', 0, GETDATE(), GETDATE())
        """
        cursor.execute(sql)
        
        # Obtener el ID insertado
        cursor.execute("SELECT id_estado FROM EstadoTurno WHERE nombre = 'NO CONFIRMADO'")
        nuevo_id = cursor.fetchone()[0]
        
        return nuevo_id

def obtener_estado_por_nombre(nombre_estado):
    """Obtener un estado por su nombre"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = "SELECT id_estado, nombre, orden_ejecucion, permite_editar, activo FROM EstadoTurno WHERE nombre = %s"
        cursor.execute(sql, [nombre_estado])
        return cursor.fetchone()

def marcar_turnos_no_confirmados():
    """
    Marca turnos RESERVADOS como NO CONFIRMADO si no se confirmaron 30 min antes
    Retorna cantidad de turnos marcados
    """
    from datetime import datetime, timedelta
    
    with connections['mi_db_2'].cursor() as cursor:
        # Obtener IDs de estados
        cursor.execute("SELECT id_estado FROM EstadoTurno WHERE nombre = 'RESERVADO'")
        estado_reservado_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id_estado FROM EstadoTurno WHERE nombre = 'NO CONFIRMADO'")
        estado_no_confirmado_id = cursor.fetchone()[0]
        
        # Calcular fecha y hora límite (30 minutos atrás)
        limite = datetime.now() - timedelta(minutes=30)
        
        # Buscar turnos RESERVADOS que ya pasaron el límite
        sql_buscar = """
        SELECT id_turno_reserva, codigo_proveedor, fecha, hora_inicio
        FROM TurnoReserva
        WHERE id_estado = %s
        AND DATEADD(MINUTE, 0, CAST(CONCAT(CONVERT(VARCHAR, fecha, 23), ' ', CONVERT(VARCHAR, hora_inicio, 108)) AS DATETIME)) <= %s
        """
        cursor.execute(sql_buscar, [estado_reservado_id, limite])
        turnos_a_marcar = cursor.fetchall()
        
        # Actualizar turnos
        turnos_actualizados = 0
        for turno in turnos_a_marcar:
            id_turno = turno[0]
            
            # Actualizar estado
            sql_update = """
            UPDATE TurnoReserva
            SET id_estado = %s, estado_actual_desde = GETDATE()
            WHERE id_turno_reserva = %s
            """
            cursor.execute(sql_update, [estado_no_confirmado_id, id_turno])
            
            # Registrar en historial
            sql_historial = """
            INSERT INTO HistorialEstadoTurno 
            (id_turno_reserva, id_estado_anterior, id_estado_nuevo, usuario, observaciones, fecha_cambio)
            VALUES (%s, %s, %s, %s, %s, GETDATE())
            """
            cursor.execute(sql_historial, [
                id_turno,
                estado_reservado_id,
                estado_no_confirmado_id,
                'SISTEMA',
                'Cambio automático: turno no confirmado 30 min antes del horario'
            ])
            
            turnos_actualizados += 1


def obtener_nombre_proveedor_por_codigo(codigo_proveedor):
    """
    Obtiene nombre de proveedor desde tabla CPA01 de base Tango (mi_db_2)
    
    Args:
        codigo_proveedor (str): Código del proveedor a buscar
    
    Returns:
        str: Nombre del proveedor o None si no existe
    """
    try:
        with connections['mi_db_2'].cursor() as cursor:
            sql = "SELECT NOM_PROVEE FROM dbo.CPA01 WHERE COD_CPA01 = %s"
            cursor.execute(sql, [codigo_proveedor.strip().upper()])
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener nombre de proveedor: {str(e)}")
        return None


def obtener_ordenes_compra_activas_proveedor(codigo_proveedor):
    """
    Obtiene órdenes de compra activas de un proveedor desde tablas de Tango (mi_db_2)
    
    Consulta las tablas CPA35 (encabezado OC), CPA36 (detalle OC), CPA01 (proveedores)
    y ESTADO_ORDEN_COMPRA para obtener OCs activas de los últimos 12 meses
    
    Args:
        codigo_proveedor (str): Código del proveedor
    
    Returns:
        list: Lista de tuplas (numero_oc, fecha_emision, estado_desc)
              Formato del número de OC: " 0000100012634" (string con espacio inicial)
    """
    try:
        with connections['mi_db_2'].cursor() as cursor:
            sql = """
            SELECT DISTINCT
                oc.N_ORDEN_CO AS NumeroOrdenCompra,
                oc.FEC_EMISIO AS FechaEmision,
                est.DESC_ESTADO_ORDEN_COMPRA AS EstadoOrden
            FROM dbo.CPA35 oc
            INNER JOIN dbo.CPA01 prov ON oc.ID_CPA01 = prov.ID_CPA01
            INNER JOIN dbo.ESTADO_ORDEN_COMPRA est ON oc.ID_ESTADO_ORDEN_COMPRA = est.ID_ESTADO_ORDEN_COMPRA
            INNER JOIN dbo.CPA36 det ON oc.ID_CPA35 = det.ID_CPA35
            WHERE prov.COD_CPA01 = %s
              AND oc.ID_ESTADO_ORDEN_COMPRA IN (1, 2, 3, 9)
              AND det.COD_DEPOSI = '01'
              AND oc.FEC_EMISIO >= DATEADD(MONTH, -12, GETDATE())
            ORDER BY oc.FEC_EMISIO DESC
            """
            cursor.execute(sql, [codigo_proveedor.strip().upper()])
            return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener órdenes de compra activas: {str(e)}")
        return []
        
        return turnos_actualizados
