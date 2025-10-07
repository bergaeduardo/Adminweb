from django.db import connections

def obtener_articulos_volumen(filtro_estado=None, filtro_rubro=None):
    """Obtiene todos los registros de la tabla EB_sincArt_volumen con filtros opcionales"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''
            SELECT 
                COD_ARTICULO,
                DESCRIPCION,
                Rubro,
                FECHA_ALTA,
                Activo as ESTADO,
                FECHA_SINC,
                altoEmbalaje,
                anchoEmbalaje,
                largoEmbalaje,
                altoReal,
                anchoReal,
                largoReal,
                pesoEmbalaje,
                pesoReal
            FROM EB_sincArt_volumen
            WHERE 1=1
        '''
        
        params = []
        
        # Aplicar filtro de estado si se proporciona
        if filtro_estado is not None:
            if filtro_estado == 'activo':
                sql += ' AND Activo = 1'
            elif filtro_estado == 'inactivo':
                sql += ' AND Activo = 0'
        
        # Aplicar filtro de rubro si se proporciona
        if filtro_rubro:
            sql += ' AND Rubro = %s'
            params.append(filtro_rubro)
        
        sql += ' ORDER BY COD_ARTICULO'
        
        cursor.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        
        # Convertir a lista de diccionarios
        articulos = []
        for row in results:
            articulo = dict(zip(columns, row))
            articulos.append(articulo)
        
        return articulos

def obtener_articulo_volumen_por_codigo(cod_articulo):
    """Obtiene un artículo específico por su código"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''
            SELECT 
                COD_ARTICULO,
                DESCRIPCION,
                Rubro,
                FECHA_ALTA,
                Activo as ESTADO,
                FECHA_SINC,
                altoEmbalaje,
                anchoEmbalaje,
                largoEmbalaje,
                altoReal,
                anchoReal,
                largoReal,
                pesoEmbalaje,
                pesoReal
            FROM EB_sincArt_volumen
            WHERE COD_ARTICULO = %s
        '''
        cursor.execute(sql, [cod_articulo])
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchone()
        
        if result:
            return dict(zip(columns, result))
        return None

def actualizar_articulo_volumen(cod_articulo, datos):
    """Actualiza los campos editables de un artículo"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''
            UPDATE EB_sincArt_volumen
            SET 
                altoEmbalaje = %s,
                anchoEmbalaje = %s,
                largoEmbalaje = %s,
                altoReal = %s,
                anchoReal = %s,
                largoReal = %s,
                pesoEmbalaje = %s,
                pesoReal = %s,
                FECHA_SINC = GETDATE()
            WHERE COD_ARTICULO = %s
        '''
        cursor.execute(sql, [
            datos['alto_embalaje'],
            datos['ancho_embalaje'],
            datos['largo_embalaje'],
            datos['alto_real'],
            datos['ancho_real'],
            datos['largo_real'],
            datos['peso_embalaje'],
            datos['peso_real'],
            cod_articulo
        ])

def crear_articulo_volumen(datos):
    """Crea un nuevo artículo en la tabla EB_sincArt_volumen"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''
            INSERT INTO EB_sincArt_volumen (
                COD_ARTICULO,
                DESCRIPCION,
                FECHA_ALTA,
                ESTADO,
                FECHA_SINC,
                altoEmbalaje,
                anchoEmbalaje,
                largoEmbalaje,
                altoReal,
                anchoReal,
                largoReal,
                pesoEmbalaje,
                pesoReal
            ) VALUES (
                %s, %s, GETDATE(), 1, GETDATE(),
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        '''
        cursor.execute(sql, [
            datos['cod_articulo'],
            datos['descripcion'],
            datos['alto_embalaje'],
            datos['ancho_embalaje'],
            datos['largo_embalaje'],
            datos['alto_real'],
            datos['ancho_real'],
            datos['largo_real'],
            datos['peso_embalaje'],
            datos['peso_real']
        ])

def eliminar_articulo_volumen(cod_articulo):
    """Elimina un artículo de la tabla EB_sincArt_volumen"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = 'DELETE FROM EB_sincArt_volumen WHERE COD_ARTICULO = %s'
        cursor.execute(sql, [cod_articulo])

def buscar_articulos_volumen(termino_busqueda, filtro_estado=None, filtro_rubro=None):
    """Busca artículos por código o descripción con filtros opcionales"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''
            SELECT 
                COD_ARTICULO,
                DESCRIPCION,
                Rubro,
                FECHA_ALTA,
                Activo as ESTADO,
                FECHA_SINC,
                altoEmbalaje,
                anchoEmbalaje,
                largoEmbalaje,
                altoReal,
                anchoReal,
                largoReal,
                pesoEmbalaje,
                pesoReal
            FROM EB_sincArt_volumen
            WHERE (COD_ARTICULO LIKE %s OR DESCRIPCION LIKE %s)
        '''
        
        params = [f'%{termino_busqueda}%', f'%{termino_busqueda}%']
        
        # Aplicar filtro de estado si se proporciona
        if filtro_estado is not None:
            if filtro_estado == 'activo':
                sql += ' AND Activo = 1'
            elif filtro_estado == 'inactivo':
                sql += ' AND Activo = 0'
        
        # Aplicar filtro de rubro si se proporciona
        if filtro_rubro:
            sql += ' AND Rubro = %s'
            params.append(filtro_rubro)
        
        sql += ' ORDER BY COD_ARTICULO'
        
        cursor.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        
        # Convertir a lista de diccionarios
        articulos = []
        for row in results:
            articulo = dict(zip(columns, row))
            articulos.append(articulo)
        
        return articulos

def obtener_rubros_disponibles():
    """Obtiene todos los rubros únicos disponibles para filtros"""
    with connections['mi_db_2'].cursor() as cursor:
        sql = '''
            SELECT DISTINCT Rubro
            FROM EB_sincArt_volumen
            WHERE Rubro IS NOT NULL AND Rubro != ''
            ORDER BY Rubro
        '''
        cursor.execute(sql)
        results = cursor.fetchall()
        return [row[0] for row in results if row[0]]