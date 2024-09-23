# Description: Consulta de clientes por grupo corporativo
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaClientesPorGrupo(grupoCorporativo_inicial, grupoCorporativo_final):
    print(f"Consulta de clientes por grupo corporativo desde {grupoCorporativo_inicial} hasta {grupoCorporativo_final}")

    # Query principal
    queryClientesporGrupo = Kdud.objects.filter(
        clave_corporativo__gte=grupoCorporativo_inicial,
        clave_corporativo__lte=grupoCorporativo_final,
    ).annotate(
        id_grupo=Subquery(
            Kdcorpo.objects.filter(
                clave_corporativo=OuterRef('clave_corporativo')
            ).values(
                'clave_corporativo'
            )[:1]
        ),
        grupo=Subquery(
            Kdcorpo.objects.filter(
                clave_corporativo=OuterRef('clave_corporativo')
            ).values(
                'descripcion_corporativo'
            )[:1]
        ),
    ).values(
        id_grupo=F('id_grupo'),
        grupo=F('grupo'),
        clave=LTrim(RTrim('clave_cliente')),
        cliente=LTrim(RTrim('nombre_cliente')),
    ).order_by(
        'id_grupo',
        'clave',
    )
    
    return list(queryClientesporGrupo)