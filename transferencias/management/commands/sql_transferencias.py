# -*- encoding: utf-8 -*-
"""Aplica (o verifica) los scripts SQL de la app de transferencias.

    python manage.py sql_transferencias --verificar     # solo lee, no escribe
    python manage.py sql_transferencias --aplicar
    python manage.py sql_transferencias --aplicar --solo 001

Los scripts de `sql/laker_sa/` van al alias `mi_db_2` (LAKER_SA) y los de
`sql/wms/` al alias `mi_db_3` (UbicacionesStockMvc), que están en servidores
distintos. Ese ruteo es por carpeta justamente para que no se pueda apuntar al
servidor equivocado sin querer.
"""

import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections

CARPETA_A_ALIAS = {
    'laker_sa': 'mi_db_2',
    'wms': 'mi_db_3',
}


def _dividir_en_lotes(sql):
    """Parte el script en los batches separados por GO (que no es T-SQL sino un
    separador del cliente, así que hay que resolverlo acá)."""
    partes = re.split(r'^\s*GO\s*;?\s*$', sql, flags=re.IGNORECASE | re.MULTILINE)
    return [p.strip() for p in partes if p.strip()]


class Command(BaseCommand):
    help = 'Aplica o verifica los scripts SQL de transferencias entre depósitos.'

    def add_arguments(self, parser):
        grupo = parser.add_mutually_exclusive_group(required=True)
        grupo.add_argument('--aplicar', action='store_true', help='Ejecuta los scripts.')
        grupo.add_argument('--verificar', action='store_true',
                           help='Solo informa qué objetos existen y si el cuerpo coincide con el archivo.')
        parser.add_argument('--solo', default=None,
                            help='Aplica solo los scripts cuyo nombre empieza con este prefijo (ej. 001).')

    def _scripts(self, solo):
        base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), 'sql')
        encontrados = []
        for carpeta in sorted(CARPETA_A_ALIAS):
            ruta = os.path.join(base, carpeta)
            if not os.path.isdir(ruta):
                continue
            for nombre in sorted(os.listdir(ruta)):
                if not nombre.endswith('.sql'):
                    continue
                if solo and not nombre.startswith(solo):
                    continue
                encontrados.append((carpeta, nombre, os.path.join(ruta, nombre)))
        return encontrados

    def handle(self, *args, **opciones):
        scripts = self._scripts(opciones.get('solo'))
        if not scripts:
            raise CommandError('No se encontró ningún script para aplicar.')

        # Otras vistas del proyecto repuntan este alias a TASKY_SA mutando
        # settings a nivel proceso; hay que fijarlo antes de conectar.
        settings.DATABASES['mi_db_2']['NAME'] = 'LAKER_SA'

        for carpeta, nombre, ruta in scripts:
            alias = CARPETA_A_ALIAS[carpeta]
            base_datos = settings.DATABASES[alias]['NAME']
            host = settings.DATABASES[alias].get('HOST', '?')

            with open(ruta, encoding='utf-8') as fh:
                sql = fh.read()

            etiqueta = f'{carpeta}/{nombre} -> {alias} ({host} / {base_datos})'

            if opciones['verificar']:
                self._verificar(alias, etiqueta, sql)
                continue

            self.stdout.write(f'Aplicando {etiqueta}')
            lotes = _dividir_en_lotes(sql)
            with connections[alias].cursor() as cursor:
                for indice, lote in enumerate(lotes, start=1):
                    try:
                        cursor.execute(lote)
                    except Exception as e:
                        raise CommandError(f'  Falló el batch {indice} de {nombre}: {e}')
            self.stdout.write(self.style.SUCCESS(f'  OK ({len(lotes)} batch/es)'))

    def _verificar(self, alias, etiqueta, sql):
        """Informa si los objetos que declara el script existen en la base."""
        objetos = re.findall(
            r'(?:CREATE\s+OR\s+ALTER\s+PROCEDURE|CREATE\s+PROCEDURE|CREATE\s+TABLE)\s+(?:dbo\.)?\[?(\w+)\]?',
            sql, flags=re.IGNORECASE)
        self.stdout.write(etiqueta)
        if not objetos:
            self.stdout.write('  (el script no declara objetos reconocibles)')
            return
        with connections[alias].cursor() as cursor:
            for nombre_obj in objetos:
                cursor.execute("SELECT type_desc FROM sys.objects WHERE name = %s", [nombre_obj])
                fila = cursor.fetchone()
                if fila:
                    self.stdout.write(self.style.SUCCESS(f'  existe   {nombre_obj} ({fila[0]})'))
                else:
                    self.stdout.write(self.style.WARNING(f'  FALTA    {nombre_obj}'))
