from django.db import models

class Kdm1(models.Model):
    sucursal = models.CharField(db_column='C1', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')
    genero = models.CharField(db_column='C2', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    naturaleza = models.CharField(db_column='C3', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    numero_grupo_documento = models.DecimalField(db_column='C4', max_digits=2, decimal_places=0)
    numero_tipo_documento = models.DecimalField(db_column='C5', max_digits=2, decimal_places=0)
    folio_documento = models.CharField(db_column='C6', max_length=7, db_collation='Traditional_Spanish_CI_AS')
    moneda = models.CharField(db_column='C7', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    almacen = models.DecimalField(db_column='C8', max_digits=4, decimal_places=0, blank=True, null=True)
    fecha = models.DateTimeField(db_column='C9', blank=True, null=True)
    cliente_proveedor = models.CharField(db_column='C10', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    referencia = models.CharField(db_column='C11', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    vendedor_comprador = models.CharField(db_column='C12', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    descuento = models.DecimalField(db_column='C13', max_digits=15, decimal_places=2, blank=True, null=True)
    iva = models.DecimalField(db_column='C14', max_digits=15, decimal_places=2, blank=True, null=True)
    ieps_retencion_isr = models.DecimalField(db_column='C15', max_digits=15, decimal_places=2, blank=True, null=True)
    importe = models.DecimalField(db_column='C16', max_digits=15, decimal_places=2, blank=True, null=True)
    plazo_dias = models.DecimalField(db_column='C17', max_digits=4, decimal_places=0, blank=True, null=True)
    fecha_pago_entrega = models.DateTimeField(db_column='C18', blank=True, null=True)
    descuento_porcentual_1 = models.CharField(db_column='C19', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    descuento_porcentual_2 = models.CharField(db_column='C20', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    descuento_porcentual_3 = models.CharField(db_column='C21', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    registro_federal_causantes = models.CharField(db_column='C22', max_length=16, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    iva_retenido = models.DecimalField(db_column='C23', max_digits=15, decimal_places=2, blank=True, null=True)
    comentario_1 = models.CharField(db_column='C24', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentario_2 = models.CharField(db_column='C25', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentario_3 = models.CharField(db_column='C26', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    pedimento_aduanal = models.CharField(db_column='C27', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_comentarios_partida = models.DecimalField(db_column='C28', max_digits=2, decimal_places=0, blank=True, null=True)
    caracteres_comentarios_partida = models.DecimalField(db_column='C29', max_digits=2, decimal_places=0, blank=True, null=True)
    condiciones_pago = models.CharField(db_column='C30', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    tipo_movimiento = models.CharField(db_column='C31', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    nombre_cliente = models.CharField(db_column='C32', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    calle_cliente = models.CharField(db_column='C33', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    colonia_cliente = models.CharField(db_column='C34', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    poblacion_cliente = models.CharField(db_column='C35', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    naturaleza_documento_anexar = models.CharField(db_column='C36', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    grupo_documento_anexar = models.DecimalField(db_column='C37', max_digits=2, decimal_places=0, blank=True, null=True)
    tipo_documento_anexar = models.DecimalField(db_column='C38', max_digits=2, decimal_places=0, blank=True, null=True)
    folio_documento_anexar = models.CharField(db_column='C39', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    paridad = models.FloatField(db_column='C40', blank=True, null=True)
    fecha_referencia = models.DateTimeField(db_column='C41', blank=True, null=True)
    saldo_documento = models.DecimalField(db_column='C42', max_digits=15, decimal_places=2, blank=True, null=True)
    estado_documento = models.CharField(db_column='C43', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_proyecto = models.CharField(db_column='C44', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_banco_subcuenta = models.CharField(db_column='C45', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_cliente_proveedor_secundario = models.CharField(db_column='C46', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    destinatario_cheque = models.CharField(db_column='C47', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    persona_solicitante = models.CharField(db_column='C48', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    monto_anticipos = models.DecimalField(db_column='C49', max_digits=15, decimal_places=2, blank=True, null=True)
    porcentaje_comision_vendedor = models.FloatField(db_column='C50', blank=True, null=True)
    monto_extra_1 = models.FloatField(db_column='C51', blank=True, null=True)
    monto_extra_2 = models.FloatField(db_column='C52', blank=True, null=True)
    monto_extra_3 = models.FloatField(db_column='C53', blank=True, null=True)
    monto_extra_4 = models.FloatField(db_column='C54', blank=True, null=True)
    monto_extra_5 = models.FloatField(db_column='C55', blank=True, null=True)
    monto_extra_6 = models.FloatField(db_column='C56', blank=True, null=True)
    monto_extra_7 = models.FloatField(db_column='C57', blank=True, null=True)
    monto_extra_8 = models.FloatField(db_column='C58', blank=True, null=True)
    monto_extra_9 = models.FloatField(db_column='C59', blank=True, null=True)
    monto_extra_10 = models.FloatField(db_column='C60', blank=True, null=True)
    clave_departamento = models.CharField(db_column='C61', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    hora_pago_entrega = models.DateTimeField(db_column='C62', blank=True, null=True)
    base_crear_folio = models.CharField(db_column='C63', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    no_usar_reservado_futuras_versiones = models.CharField(db_column='C65', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    proveedor_real = models.CharField(db_column='C66', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    usuario_captura_documento = models.CharField(db_column='C67', max_length=23, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_captura = models.DateTimeField(db_column='C68', blank=True, null=True)
    hora_captura = models.TimeField(db_column='C69', blank=True, null=True)
    clave_confirmacion_punto_venta = models.CharField(db_column='C80', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_validacion_1 = models.CharField(db_column='C81', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_validacion_2 = models.CharField(db_column='C82', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_validacion_3 = models.CharField(db_column='C83', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_validacion_4 = models.CharField(db_column='C84', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_validacion_5 = models.CharField(db_column='C85', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_autorizacion_1 = models.CharField(db_column='C86', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_autorizacion_2 = models.CharField(db_column='C87', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_autorizacion_3 = models.CharField(db_column='C88', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_autorizacion_4 = models.CharField(db_column='C89', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentarios_autorizacion_5 = models.CharField(db_column='C90', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_reprogramacion = models.DateTimeField(db_column='C91', blank=True, null=True)
    departamento_cliente_lista_precios = models.CharField(db_column='C94', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    lista_precios_especial_cliente = models.CharField(db_column='C95', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    tipo_cobro_caja = models.CharField(db_column='C99', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    uso_cfdi = models.CharField(db_column='C161', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    metodo_pago = models.CharField(db_column='C162', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    forma_pago = models.CharField(db_column='C163', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    tipo_relacion = models.CharField(db_column='C164', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_envio_buro_entrega = models.DateTimeField(db_column='C165', blank=True, null=True)
    fecha_orden_compra = models.DateTimeField(db_column='C166', blank=True, null=True)
    folio_confirmacion = models.CharField(db_column='C167', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    empaque = models.CharField(db_column='C168', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_remision = models.DecimalField(db_column='C169', max_digits=4, decimal_places=0, blank=True, null=True)
    gln_tienda = models.DecimalField(db_column='C170', max_digits=13, decimal_places=0, blank=True, null=True)
    cantidad_pedidos_folio_recibo = models.DecimalField(db_column='C171', max_digits=4, decimal_places=0, blank=True, null=True)
    fecha_contrarecibo = models.DateTimeField(db_column='C172', blank=True, null=True)
    baucher = models.CharField(db_column='C173', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_pago = models.DateTimeField(db_column='C174', blank=True, null=True)
    hora_pago = models.TimeField(db_column='C175', blank=True, null=True)
    banco_origen = models.CharField(db_column='C176', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_origen = models.CharField(db_column='C177', max_length=8, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    banco_destino = models.CharField(db_column='C178', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_destino = models.CharField(db_column='C179', max_length=8, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    orden_compra = models.CharField(db_column='C180', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_tienda_consignatario = models.CharField(db_column='C181', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    contrarecibo = models.CharField(db_column='C182', max_length=15, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_parametro_anterior = models.DateTimeField(db_column='C188', blank=True, null=True)
    valor_parametro_anterior = models.CharField(db_column='C189', max_length=15, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    valor_parametro_disparo = models.CharField(db_column='C190', max_length=15, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_lectura_disparo = models.DateTimeField(db_column='C191', blank=True, null=True)
    clave_parametro = models.CharField(db_column='C192', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    reporte_falla = models.CharField(db_column='C193', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    causa_mantenimiento = models.CharField(db_column='C194', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_inicial_realizar = models.DateTimeField(db_column='C195', blank=True, null=True)
    hora_inicial_realizar = models.TimeField(db_column='C196', blank=True, null=True)
    fecha_final_realizar = models.DateTimeField(db_column='C197', blank=True, null=True)
    hora_final_realizar = models.TimeField(db_column='C198', blank=True, null=True)
    descripcion_parametro = models.CharField(db_column='C199', max_length=255, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    orden_anterior_mantenimiento_correctivo = models.CharField(db_column='C200', max_length=15, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'KDM1'
        
class Kdm2(models.Model):
    clave_sucursal = models.CharField(db_column='C1', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')
    genero = models.CharField(db_column='C2', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    naturaleza = models.CharField(db_column='C3', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    num_grupo_movimiento = models.DecimalField(db_column='C4', max_digits=2, decimal_places=0)
    num_tipo_movimiento = models.DecimalField(db_column='C5', max_digits=2, decimal_places=0)
    folio_documento = models.CharField(db_column='C6', max_length=7, db_collation='Traditional_Spanish_CI_AS')
    num_partida = models.DecimalField(db_column='C7', max_digits=6, decimal_places=0)
    clave_producto = models.CharField(db_column='C8', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cantidad_unidades = models.FloatField(db_column='C9', blank=True, null=True)
    descripcion_producto = models.CharField(db_column='C10', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    unidad = models.CharField(db_column='C11', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    precio_unitario = models.DecimalField(db_column='C12', max_digits=25, decimal_places=6, blank=True, null=True)
    importe_partida = models.DecimalField(db_column='C13', max_digits=15, decimal_places=2, blank=True, null=True)
    descuento_pct1 = models.FloatField(db_column='C14', blank=True, null=True)
    descuento_pct2 = models.FloatField(db_column='C15', blank=True, null=True)
    descuento_pct3 = models.FloatField(db_column='C16', blank=True, null=True)
    iva_pct = models.CharField(db_column='C17', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    ieps_pct = models.FloatField(db_column='C18', blank=True, null=True)
    naturaleza_docto_anterior = models.CharField(db_column='C19', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    grupo_docto_anterior = models.DecimalField(db_column='C20', max_digits=2, decimal_places=0, blank=True, null=True)
    tipo_docto_anterior = models.DecimalField(db_column='C21', max_digits=2, decimal_places=0, blank=True, null=True)
    folio_docto_anterior = models.CharField(db_column='C22', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    partida_docto_anterior = models.DecimalField(db_column='C23', max_digits=3, decimal_places=0, blank=True, null=True)
    saldo_unidades_partida = models.FloatField(db_column='C24', blank=True, null=True)
    clave_cliente = models.CharField(db_column='C25', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    costo_venta_partida = models.FloatField(db_column='C26', blank=True, null=True)
    clave_vendedor_comprador = models.CharField(db_column='C27', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    referencia = models.CharField(db_column='C28', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_almacen = models.DecimalField(db_column='C29', max_digits=5, decimal_places=0, blank=True, null=True)
    num_cargos = models.DecimalField(db_column='C30', max_digits=4, decimal_places=0, blank=True, null=True)
    cantidad_resta_docto_anterior = models.FloatField(db_column='C31', blank=True, null=True)
    fecha = models.DateTimeField(db_column='C32', blank=True, null=True)
    monto_costo = models.DecimalField(db_column='C33', max_digits=15, decimal_places=2, blank=True, null=True)
    existencia_previa_unidades = models.DecimalField(db_column='C34', max_digits=15, decimal_places=2, blank=True, null=True)
    existencia_previa_pesos = models.DecimalField(db_column='C35', max_digits=15, decimal_places=2, blank=True, null=True)
    moneda = models.CharField(db_column='C36', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    costo_en_moneda = models.DecimalField(db_column='C37', max_digits=15, decimal_places=2, blank=True, null=True)
    venta_en_moneda = models.DecimalField(db_column='C38', max_digits=15, decimal_places=2, blank=True, null=True)
    orden_trabajo = models.CharField(db_column='C39', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    concepto = models.CharField(db_column='C40', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    linea = models.CharField(db_column='C45', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    envio = models.CharField(db_column='C46', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    release = models.CharField(db_column='C47', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    descuento_pct = models.CharField(db_column='C48', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    descuento_dls = models.DecimalField(db_column='C49', max_digits=15, decimal_places=3, blank=True, null=True)
    transportacion = models.CharField(db_column='C51', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    operador = models.CharField(db_column='C52', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    hora_salida = models.CharField(db_column='C53', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    num_sellos = models.CharField(db_column='C54', max_length=15, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    num_lotes = models.CharField(db_column='C55', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_caducidad = models.DateTimeField(db_column='C56', blank=True, null=True)
    conteo_fisico = models.DecimalField(db_column='C57', max_digits=20, decimal_places=0, blank=True, null=True)
    diferencia = models.DecimalField(db_column='C58', max_digits=20, decimal_places=0, blank=True, null=True)
    vacio = models.CharField(db_column='C59', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    razon_social = models.DecimalField(db_column='C60', max_digits=15, decimal_places=6, blank=True, null=True)
    valor_total = models.DecimalField(db_column='C61', max_digits=15, decimal_places=6, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'KDM2'

class Kdij(models.Model):
    clave_sucursal = models.CharField(db_column='C1', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')
    clave_almacen = models.DecimalField(db_column='C2', max_digits=4, decimal_places=0)
    clave_producto = models.CharField(db_column='C3', max_length=18, db_collation='Traditional_Spanish_CI_AS')
    genero = models.CharField(db_column='C4', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    naturaleza = models.CharField(db_column='C5', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    grupo_movimiento = models.DecimalField(db_column='C6', max_digits=2, decimal_places=0)
    tipo_movimiento = models.DecimalField(db_column='C7', max_digits=2, decimal_places=0)
    folio_movimiento = models.CharField(db_column='C8', max_length=7, db_collation='Traditional_Spanish_CI_AS')
    numero_partida = models.DecimalField(db_column='C9', max_digits=3, decimal_places=0)
    fecha = models.DateTimeField(db_column='C10', blank=True, null=True)
    cantidad_unidades_entrada = models.FloatField(db_column='C11', blank=True, null=True)
    unidad_medida_kdij = models.CharField(db_column='C12', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    monto_costo_pesos = models.DecimalField(db_column='C13', max_digits=15, decimal_places=2, blank=True, null=True)
    monto_venta = models.DecimalField(db_column='C14', max_digits=15, decimal_places=2, blank=True, null=True)
    clave_cliente = models.CharField(db_column='C15', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_vendedor = models.CharField(db_column='C16', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    existencia_previa_unidades = models.FloatField(db_column='C17', blank=True, null=True)
    existencia_previa_ueps_pesos = models.DecimalField(db_column='C18', max_digits=15, decimal_places=2, blank=True, null=True)
    referencia = models.CharField(db_column='C19', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    moneda_transaccion = models.CharField(db_column='C20', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    monto_costo_moneda_movimiento = models.FloatField(db_column='C21', blank=True, null=True)
    monto_venta_moneda_movimiento = models.FloatField(db_column='C22', blank=True, null=True)
    clave_orden_trabajo = models.CharField(db_column='C23', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_concepto = models.CharField(db_column='C24', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    descuento_porcentual_1 = models.FloatField(db_column='C25', blank=True, null=True)
    descuento_porcentual_2 = models.FloatField(db_column='C26', blank=True, null=True)
    descuento_porcentual_3 = models.FloatField(db_column='C27', blank=True, null=True)
    naturaleza_anterior = models.CharField(db_column='C37', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    grupo_movimiento_anterior = models.DecimalField(db_column='C38', max_digits=2, decimal_places=0, blank=True, null=True)
    tipo_movimiento_anterior = models.DecimalField(db_column='C39', max_digits=2, decimal_places=0, blank=True, null=True)
    folio_movimiento_anterior = models.CharField(db_column='C40', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_partida_anterior = models.DecimalField(db_column='C41', max_digits=3, decimal_places=0, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'KDIJ'

class Kdii(models.Model):
    clave_producto = models.CharField(db_column='C1', primary_key=True, max_length=18, db_collation='Traditional_Spanish_CI_AS')
    descripcion_producto = models.CharField(db_column='C2', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    linea_producto = models.CharField(db_column='C3', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    tipo_producto = models.CharField(db_column='C4', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    grupo_producto = models.CharField(db_column='C5', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    codigo_proveedor = models.CharField(db_column='C6', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    codigo_barras = models.CharField(db_column='C7', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_proveedor_principal = models.CharField(db_column='C8', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_proveedor_secundario = models.CharField(db_column='C9', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_ubicacion_almacen = models.CharField(db_column='C10', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    unidad_medida = models.CharField(db_column='C11', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    unidad_alternativa = models.CharField(db_column='C12', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    factor_conversion = models.FloatField(db_column='C13', blank=True, null=True)
    primer_precio = models.DecimalField(db_column='C14', max_digits=13, decimal_places=2, blank=True, null=True)
    segundo_precio = models.DecimalField(db_column='C15', max_digits=13, decimal_places=2, blank=True, null=True)
    tercer_precio = models.DecimalField(db_column='C16', max_digits=13, decimal_places=2, blank=True, null=True)
    cuarto_precio = models.DecimalField(db_column='C17', max_digits=13, decimal_places=2, blank=True, null=True)
    iva_porcentual = models.FloatField(db_column='C18', blank=True, null=True)
    impuesto_especial = models.FloatField(db_column='C19', blank=True, null=True)
    clave_moneda_precios_venta = models.CharField(db_column='C20', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    requiere_numero_serie = models.CharField(db_column='C21', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    control_lotes = models.CharField(db_column='C22', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    precio_lista_proveedor = models.DecimalField(db_column='C23', max_digits=13, decimal_places=2, blank=True, null=True)
    descuento_proveedor = models.DecimalField(db_column='C24', max_digits=13, decimal_places=2, blank=True, null=True)
    clave_producto_sustituto = models.CharField(db_column='C25', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_producto_equivalente = models.CharField(db_column='C26', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    producto_importacion = models.CharField(db_column='C27', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fraccion_arancelaria = models.CharField(db_column='C28', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    porcentaje_dta = models.FloatField(db_column='C29', blank=True, null=True)
    clave_pais_origen = models.CharField(db_column='C30', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_moneda_compra = models.CharField(db_column='C31', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    descripcion_idioma_origen = models.CharField(db_column='C32', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    nivel_inventario_minimo = models.FloatField(db_column='C33', blank=True, null=True)
    cantidad_minima_orden_compra = models.FloatField(db_column='C34', blank=True, null=True)
    nivel_inventario_maximo = models.FloatField(db_column='C35', blank=True, null=True)
    medida_producto = models.CharField(db_column='C36', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    quinta_clasificacion = models.CharField(db_column='C37', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    sexta_clasificacion = models.CharField(db_column='C38', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentario_producto_1 = models.CharField(db_column='C39', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentario_producto_2 = models.CharField(db_column='C40', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comentario_producto_3 = models.CharField(db_column='C41', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    lote_compra_fabricacion = models.CharField(db_column='C42', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    control_ubicacion = models.CharField(db_column='C43', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campos_modelo_talla_color = models.IntegerField(db_column='C44', blank=True, null=True)
    clave_dibujo = models.CharField(db_column='C45', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_ruta_fabricacion = models.CharField(db_column='C46', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    nivel_ingenieria = models.FloatField(db_column='C47', blank=True, null=True)
    tipo_inventario = models.CharField(db_column='C48', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    movimiento_producto = models.CharField(db_column='C49', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_inicio_vigencia = models.DateField(db_column='C50', blank=True, null=True)
    estatus_producto = models.CharField(db_column='C51', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    tiempo_entrega = models.CharField(db_column='C52', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    minimo_estacion_2 = models.FloatField(db_column='C53', blank=True, null=True)
    maximo_estacion_2 = models.FloatField(db_column='C54', blank=True, null=True)
    punto_reorden_estacion_2 = models.FloatField(db_column='C55', blank=True, null=True)
    fecha_inicio_estacion_2 = models.DateField(db_column='C56', blank=True, null=True)
    minimo_estacion_3 = models.FloatField(db_column='C57', blank=True, null=True)
    maximo_estacion_3 = models.FloatField(db_column='C58', blank=True, null=True)
    punto_reorden_estacion_3 = models.FloatField(db_column='C59', blank=True, null=True)
    fecha_inicio_estacion_3 = models.DateField(db_column='C60', blank=True, null=True)
    minimo_estacion_4 = models.FloatField(db_column='C61', blank=True, null=True)
    maximo_estacion_4 = models.FloatField(db_column='C62', blank=True, null=True)
    punto_reorden_estacion_4 = models.FloatField(db_column='C63', blank=True, null=True)
    fecha_inicio_estacion_4 = models.DateField(db_column='C64', blank=True, null=True)
    fecha_inicio_estacion_1 = models.DateField(db_column='C65', blank=True, null=True)
    porcentaje_merma = models.FloatField(db_column='C66', blank=True, null=True)
    control_inventario = models.IntegerField(db_column='C67', blank=True, null=True)
    lote_transferencia = models.CharField(db_column='C68', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    nombre_imagen = models.CharField(db_column='C70', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    necesita_autorizacion = models.CharField(db_column='C71', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    producto_indirecto = models.CharField(db_column='C72', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_indirecto = models.CharField(db_column='C73', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    monto_max_autorizable = models.DecimalField(db_column='C74', max_digits=13, decimal_places=2, blank=True, null=True)
    estandar_producto = models.CharField(db_column='C75', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    upc = models.CharField(db_column='C76', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_producto_servicio = models.CharField(db_column='C80', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    grupo2 = models.CharField(db_column='C82', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_unidad = models.CharField(db_column='C87', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_producto_terminado = models.CharField(db_column='C88', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    titulo_precio_venta_1 = models.CharField(db_column='C90', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    titulo_precio_venta_2 = models.CharField(db_column='C91', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    titulo_precio_venta_3 = models.CharField(db_column='C92', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    titulo_precio_venta_4 = models.CharField(db_column='C93', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    factor_precios_venta = models.FloatField(db_column='C94', blank=True, null=True)
    titulo_precio_renta_1 = models.CharField(db_column='C95', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    titulo_precio_renta_2 = models.CharField(db_column='C96', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    titulo_precio_renta_3 = models.CharField(db_column='C97', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    titulo_precio_renta_4 = models.CharField(db_column='C98', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    tipo_costo = models.CharField(db_column='C100', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    precio_renta_1 = models.DecimalField(db_column='C101', max_digits=13, decimal_places=2, blank=True, null=True)
    precio_renta_2 = models.DecimalField(db_column='C102', max_digits=13, decimal_places=2, blank=True, null=True)
    precio_renta_3 = models.DecimalField(db_column='C103', max_digits=13, decimal_places=2, blank=True, null=True)
    precio_renta_4 = models.DecimalField(db_column='C104', max_digits=13, decimal_places=2, blank=True, null=True)
    tiempo_estimado_tarea = models.FloatField(db_column='C110', blank=True, null=True)
    costo_por_hora = models.DecimalField(db_column='C111', max_digits=13, decimal_places=2, blank=True, null=True)
    costo_operacion = models.DecimalField(db_column='C112', max_digits=13, decimal_places=2, blank=True, null=True)
    personal_necesario = models.FloatField(db_column='C113', blank=True, null=True)
    tipo_cambio = models.CharField(db_column='C115', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_tipo_cambio = models.DateField(db_column='C116', blank=True, null=True)
    campo_generico1 = models.CharField(db_column='C120', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico2 = models.CharField(db_column='C121', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico3 = models.CharField(db_column='C122', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico4 = models.CharField(db_column='C123', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico5 = models.CharField(db_column='C124', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico6 = models.CharField(db_column='C125', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico7 = models.CharField(db_column='C126', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico8 = models.CharField(db_column='C127', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico9 = models.CharField(db_column='C128', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico10 = models.CharField(db_column='C129', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    campo_generico11 = models.CharField(db_column='C130', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KDII'

class Kdie(models.Model):
    clave_producto = models.CharField(db_column='C1', primary_key=True, max_length=5, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    descripcion_producto = models.CharField(db_column='C2', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    almacen_defecto = models.DecimalField(db_column='C4', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    almacen_defecto_salidas = models.DecimalField(db_column='C5', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDIE'
        
class Kdib(models.Model):
    clave_sucursal = models.CharField(db_column='C1', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase. The composite primary key (C1, C2, C3) found, that is not supported. The first column is selected.
    clave_almacen = models.DecimalField(db_column='C2', max_digits=4, decimal_places=0)  # Field name made lowercase.
    clave_ubicacion = models.CharField(db_column='C3', max_length=7, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    descripcion = models.CharField(db_column='C4', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDIB'

class Kdid(models.Model):
    clave_unidad = models.CharField(db_column='C1', primary_key=True, max_length=3, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    descripcion_unidad = models.CharField(db_column='C2', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDID'

class Kdiq(models.Model):
    clave_sucursal = models.CharField(db_column='C1', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase. The composite primary key (C1, C2) found, that is not supported. The first column is selected.
    clave_almacen = models.DecimalField(db_column='C2', max_digits=5, decimal_places=0)  # Field name made lowercase.
    descripcion = models.CharField(db_column='C3', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    estado_mercancia = models.CharField(db_column='C4', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    estatus = models.CharField(db_column='C5', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDIQ'

class Kduv(models.Model):
    clave_sucursal = models.CharField(db_column='C1', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_vendedor = models.CharField(db_column='C2', primary_key=True, max_length=5, db_collation='Traditional_Spanish_CI_AS')
    nombre_vendedor = models.CharField(db_column='C3', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    comision_venta = models.FloatField(db_column='C4', max_length=7, blank=True, null=True)
    comision_utilidad = models.FloatField(db_column='C5', max_length=7, blank=True, null=True)
    comision_cobros = models.FloatField(db_column='C6', max_length=7, blank=True, null=True)
    comision_productos = models.FloatField(db_column='C7', max_length=7, blank=True, null=True)
    telefono1_oficina = models.CharField(db_column='C9', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    telefono2_oficina = models.CharField(db_column='C10', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    celular = models.CharField(db_column='C11', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    nextel = models.CharField(db_column='C12', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    correo_electronico1 = models.CharField(db_column='C14', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    correo_electronico2 = models.CharField(db_column='C15', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    usuario_kepler = models.CharField(db_column='C16', max_length=23, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    supervisor = models.CharField(db_column='C17', max_length=23, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    bandera_supervisor = models.CharField(db_column='C18', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    twitter = models.CharField(db_column='C19', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    facebook = models.CharField(db_column='C20', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    linkedin = models.CharField(db_column='C21', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    zona = models.CharField(db_column='C22', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    giro = models.CharField(db_column='C23', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    almacen_correspondiente = models.DecimalField(db_column='C24', max_digits=5, decimal_places=0, blank=True, null=True)
    estatus = models.CharField(db_column='C30', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KDUV'

class Kdmm(models.Model):
    genero = models.CharField(db_column='C1', primary_key=True, max_length=1, db_collation='Traditional_Spanish_CI_AS')
    naturaleza = models.CharField(db_column='C2', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    num_grupo_movimientos = models.DecimalField(db_column='C3', max_digits=2, decimal_places=0)
    tipo_movimiento = models.DecimalField(db_column='C4', max_digits=2, decimal_places=0)
    descripcion_movimiento = models.CharField(db_column='C5', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_contabilidad_general = models.CharField(db_column='C6', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_ctas_cobrar_pagar = models.CharField(db_column='C7', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_inventarios = models.CharField(db_column='C8', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_estadistica_ventas_brutas = models.CharField(db_column='C9', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_estadistica_devoluciones = models.CharField(db_column='C10', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_estadistica_bonificaciones = models.CharField(db_column='C11', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_estadistica_notas_cargo = models.CharField(db_column='C12', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_estadistica_notas_credito = models.CharField(db_column='C13', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    afecta_fecha_ultimo_cobro = models.CharField(db_column='C14', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    porcentaje_retencion_isr = models.CharField(db_column='C15', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    iva_porcentual = models.CharField(db_column='C16', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    nombre_archivo_folio = models.CharField(db_column='C17', max_length=8, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    tipo_poliza_producir = models.CharField(db_column='C18', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_cargo = models.CharField(db_column='C19', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_abono = models.CharField(db_column='C20', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_iva = models.CharField(db_column='C21', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_ieps = models.CharField(db_column='C22', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra1 = models.CharField(db_column='C23', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra2 = models.CharField(db_column='C24', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    num_campo_cuenta_principal = models.DecimalField(db_column='C25', max_digits=2, decimal_places=0, blank=True, null=True)
    num_campo_cuenta_secundaria = models.DecimalField(db_column='C26', max_digits=2, decimal_places=0, blank=True, null=True)
    restriccion_no_facturar_rojo = models.CharField(db_column='C27', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    divide_cta_principal_cuentas_complementarias = models.CharField(db_column='C28', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    divide_cta_secundaria_cuentas_complementarias = models.CharField(db_column='C29', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    divide_cta_iva_cuentas_complementarias = models.CharField(db_column='C30', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    divide_cta_ieps_cuentas_complementarias = models.CharField(db_column='C31', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    num_campo_nombre_archivo_folio = models.DecimalField(db_column='C32', max_digits=2, decimal_places=0, blank=True, null=True)
    porcentaje_iva_retenido = models.CharField(db_column='C33', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra3 = models.CharField(db_column='C34', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra4 = models.CharField(db_column='C35', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra5 = models.CharField(db_column='C36', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra6 = models.CharField(db_column='C37', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra7 = models.CharField(db_column='C38', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra8 = models.CharField(db_column='C39', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra9 = models.CharField(db_column='C40', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_contable_extra10 = models.CharField(db_column='C41', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_cliente_extra1 = models.DecimalField(db_column='C50', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra2 = models.DecimalField(db_column='C51', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra3 = models.DecimalField(db_column='C52', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra4 = models.DecimalField(db_column='C53', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra5 = models.DecimalField(db_column='C54', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra6 = models.DecimalField(db_column='C55', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra7 = models.DecimalField(db_column='C56', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra8 = models.DecimalField(db_column='C57', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra9 = models.DecimalField(db_column='C58', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_cliente_extra10 = models.DecimalField(db_column='C59', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra1 = models.DecimalField(db_column='C60', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra2 = models.DecimalField(db_column='C61', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra3 = models.DecimalField(db_column='C62', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra4 = models.DecimalField(db_column='C63', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra5 = models.DecimalField(db_column='C64', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra6 = models.DecimalField(db_column='C65', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra7 = models.DecimalField(db_column='C66', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra8 = models.DecimalField(db_column='C67', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra9 = models.DecimalField(db_column='C68', max_digits=3, decimal_places=0, blank=True, null=True)
    clave_proveedor_extra10 = models.DecimalField(db_column='C69', max_digits=3, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KDMM'

class Kdms(models.Model):
    clave_sucursal = models.CharField(db_column='C1', primary_key=True, max_length=10, db_collation='Traditional_Spanish_CI_AS')
    descripcion = models.CharField(db_column='C2', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    identificacion = models.CharField(db_column='C3', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    calle = models.CharField(db_column='C4', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    colonia = models.CharField(db_column='C5', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    pais = models.CharField(db_column='C6', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_estado = models.CharField(db_column='C7', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_municipio = models.CharField(db_column='C8', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    codigo_postal = models.CharField(db_column='C9', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    telefono1 = models.CharField(db_column='C10', max_length=16, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    telefono2 = models.CharField(db_column='C11', max_length=16, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    sitio_web = models.CharField(db_column='C12', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_exterior = models.CharField(db_column='C20', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_interior = models.CharField(db_column='C21', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    localidad = models.CharField(db_column='C22', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    referencia = models.CharField(db_column='C23', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    municipio = models.CharField(db_column='C24', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_folios_facturacion_cfdi = models.CharField(db_column='C25', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_aprobacion_folios_facturacion_cfdi = models.CharField(db_column='C26', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    ano_aprobacion_folios_facturacion_cfdi = models.CharField(db_column='C27', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    regimen_fiscal_facturacion_cfdi = models.CharField(db_column='C28', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_folios_notas_credito_cfdi = models.CharField(db_column='C29', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_aprobacion_notas_credito_cfdi = models.CharField(db_column='C30', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    ano_aprobacion_notas_credito_cfdi = models.CharField(db_column='C31', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    regimen_fiscal_notas_credito_cfdi = models.CharField(db_column='C32', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_folios_notas_cargo_cfdi = models.CharField(db_column='C33', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    numero_aprobacion_notas_cargo_cfdi = models.CharField(db_column='C34', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    ano_aprobacion_notas_cargo_cfdi = models.CharField(db_column='C35', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    regimen_fiscal_notas_cargo_cfdi = models.CharField(db_column='C36', max_length=100, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_factura_cfd = models.CharField(db_column='C37', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_notas_credito_cfd = models.CharField(db_column='C38', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_notas_cargo_cfd = models.CharField(db_column='C39', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_complemento_pago_cfdi = models.CharField(db_column='C40', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_anticipo_pago_cfdi = models.CharField(db_column='C41', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_traslado_cfdi = models.CharField(db_column='C42', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    cuenta_tercer_nivel_clientes_ventas = models.CharField(db_column='C43', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_facturacion_app = models.CharField(db_column='C44', max_length=6, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    region = models.CharField(db_column='C49', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    servicio_o_referencia = models.CharField(db_column='C50', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clabe_interbancaria = models.CharField(db_column='C51', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'KDMS'

class Kdud(models.Model):
    sucursal_dado_alta = models.CharField(db_column='C1', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Sucursal donde está dado de alta
    clave_cliente = models.CharField(db_column='C2', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')  # Clave del cliente
    nombre_cliente = models.CharField(db_column='C3', max_length=170, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Nombre del cliente
    calle_numero_direccion = models.CharField(db_column='C4', max_length=90, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Calle y el número de la dirección
    colonia_cliente = models.CharField(db_column='C5', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Colonia donde está el cliente
    poblacion_ubica = models.CharField(db_column='C6', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Población donde se ubica
    telefono = models.CharField(db_column='C7', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Número de su teléfono
    segundo_telefono = models.CharField(db_column='C8', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Segundo número telefónico
    razon_bloqueo = models.CharField(db_column='C9', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Razon de bloqueo
    rfc = models.CharField(db_column='C10', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # RFC
    direccion_internet = models.CharField(db_column='C11', max_length=150, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Dirección de Internet
    clave_vendedor_atiende = models.CharField(db_column='C12', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clave del vendedor que lo atiende
    clave_grupo_pertenece = models.CharField(db_column='C13', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clave del grupo al que pertenece
    raz = models.CharField(db_column='C14', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Raz
    apellido_materno = models.DecimalField(db_column='C15', max_digits=15, decimal_places=2, blank=True, null=True)  # Apellido Materno
    plazo_credito = models.CharField(db_column='C16', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Plazo de crédito que se le dá
    descuento_ordinariamente = models.CharField(db_column='C17', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Descuento que ordinariamente se le dá (%)
    segundo_descuento = models.CharField(db_column='C18', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Segundo descuento porcentual
    tercer_descuento = models.CharField(db_column='C19', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Tercer descuento porcentual
    dia_revision = models.CharField(db_column='C20', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Día de revisión
    hora_revision = models.CharField(db_column='C21', max_length=11, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Hora de revisión
    dia_pago = models.CharField(db_column='C22', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Día de pago
    hora_pago = models.CharField(db_column='C23', max_length=11, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Hora de pago
    lugar_entrega_mercancia1 = models.CharField(db_column='C24', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Lugar de entrega de mercancía
    lugar_entrega_mercancia2 = models.CharField(db_column='C25', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Lugar de entrega de mercancía
    lugar_entrega_mercancia3 = models.CharField(db_column='C26', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Lugar de entrega de mercancía
    codigo_postal = models.CharField(db_column='C27', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Código postal
    comision_porcentual1 = models.DecimalField(db_column='C28', max_digits=7, decimal_places=4, blank=True, null=True)  # Comisión porcentual
    comision_porcentual2 = models.DecimalField(db_column='C29', max_digits=7, decimal_places=4, blank=True, null=True)  # Comisión porcentual sobre cobranza
    curp_cliente = models.CharField(db_column='C30', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Teclee el CURP del Cliente
    bloqueado_credito_facturacion = models.CharField(db_column='C31', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Bloqueado por credito y cobranza Facturacion
    bloqueado_credito_remision = models.CharField(db_column='C32', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Bloqueado por Credito y Cobranza Remision
    giro_cliente = models.CharField(db_column='C33', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Teclee el giro del cliente
    descuento_confidencial1 = models.DecimalField(db_column='C34', max_digits=4, decimal_places=0, blank=True, null=True)  # DESCUENTO CONFIDENCIAL 1 PARA COBRO
    descuento_confidencial2 = models.DecimalField(db_column='C35', max_digits=4, decimal_places=0, blank=True, null=True)  # DESCUENTO CONFIDENCIAL 2 PARA COBRO
    descuento_confidencial3 = models.DecimalField(db_column='C36', max_digits=4, decimal_places=0, blank=True, null=True)  # DESCUENTO CONFIDENCIAL 3 PARA COBRO
    requiere_validar_orden_compra = models.CharField(db_column='C40', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Requiere validar orden de compra para no se repita
    tipo_cliente = models.CharField(db_column='C41', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Tipo de Cliente [C]rédito / Conta[D]o
    dias_vencida_cargo_suspende = models.DecimalField(db_column='C42', max_digits=3, decimal_places=0, blank=True, null=True)  # Después de x días de vencida un cargo suspender
    observaciones_ultima_suspension = models.CharField(db_column='C43', max_length=250, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Observaciones de la ultima Suspensión
    estatus = models.CharField(db_column='C45', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Status:  [ACT]ivo / [SUS]pendido / [BAJ]a
    numero_exterior = models.CharField(db_column='C50', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Numero Exterior
    numero_interior = models.CharField(db_column='C51', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Numero Interior
    localidad = models.CharField(db_column='C52', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Localidad
    referencia = models.CharField(db_column='C53', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Notas al cliente
    municipio = models.CharField(db_column='C54', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Tienda de Tornillos
    estado = models.CharField(db_column='C55', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Dirección de Domicilio
    pais = models.CharField(db_column='C56', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Datos Fiscales
    trading_partner = models.CharField(db_column='C57', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Despacho a Domicilio
    calif_trading_partner = models.CharField(db_column='C58', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Pagina de Internet
    EAN_proveedor = models.CharField(db_column='C59', max_length=13, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clasificacion del cliente
    numero_proveedor = models.CharField(db_column='C60', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Orden de Compra minima
    formato_factura = models.CharField(db_column='C61', max_length=8, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Respaldo
    clave_metodo_pago = models.CharField(db_column='C62', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Dato a desplegar en el artículo
    referencia_bancaria = models.CharField(db_column='C63', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Descuento adicional
    contacto_compra = models.CharField(db_column='C65', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Anotaciones
    clave_corporativo = models.CharField(db_column='C66', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Tipo de Venta
    nombre_corporativo = models.CharField(db_column='C67', max_length=80, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Comentarios
    digito_verificador_banco = models.CharField(db_column='C68', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Domicilio Fiscal
    referencia_bancaria = models.CharField(db_column='C69', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Teléfono Adicional
    pago_SAT1 = models.CharField(db_column='C70', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Zona / País
    pago_SAT2 = models.CharField(db_column='C71', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Contacto
    pago_SAT3 = models.CharField(db_column='C72', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Orden de Compra máxima
    cfdi = models.CharField(db_column='C73', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # OC Tipo
    control_lista_precios = models.CharField(db_column='C74', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # OC Grupo
    control_lista_preciosAPP = models.DecimalField(db_column='C75', max_digits=1, decimal_places=0, blank=True, null=True)  # Inicio de crédito
    respaldo_nombre_cliente = models.CharField(db_column='C77', max_length=120, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Observaciones de bloqueo al cliente
    regimen_capital_social = models.CharField(db_column='C78', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Tipo de orden de compra
    estatus_vigente = models.CharField(db_column='C79', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Validación de domicilio
    clave_del_banco1 = models.CharField(db_column='C80', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Fecha de actualización
    clave_del_banco2 = models.CharField(db_column='C81', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Fecha de modificación
    numero_de_la_cuenta1 = models.CharField(db_column='C82', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Artículo a desplegar
    numero_de_la_cuenta2 = models.CharField(db_column='C83', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clave del Producto o Servicio
    revisado_validado = models.CharField(db_column='C90', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Vence la obra que tiene dado de alta
    fecha_revision_validacion = models.DateTimeField(db_column='C91', blank=True, null=True)  # Fecha de bloqueo por crédito
    fecha_ultima_modificacion = models.DateTimeField(db_column='C92', blank=True, null=True)  # Fecha de bloqueo de remisión
    ultimo_usuario_en_modificar = models.CharField(db_column='C93', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Seguimiento Atractivo
    ultima_hora_revision = models.CharField(db_column='C94', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Identificación
    lista_precios_asignados = models.CharField(db_column='C95', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Cuenta
    fecha_captura = models.DateTimeField(db_column='C96', blank=True, null=True)  # Fecha de la última revisión
    cliente_credito_contado = models.CharField(db_column='C97', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Enviado por
    hora_ultima_modificacion = models.CharField(db_column='C98', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Código postal secundario
    apellido_paterno = models.CharField(db_column='C99', max_length=120, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Serie de remisión
    apellido_materno = models.CharField(db_column='C100', max_length=120, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Nombre del cliente del vendedor
    nombre_cliente_cb = models.CharField(db_column='C101', max_length=170, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Dirección de correo electrónico
    plazo2 = models.CharField(db_column='C102', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Requisito de Venta
    razon_bloqueo = models.CharField(db_column='C103', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Tiempo de Respuesta
    estatus_limites_credito = models.CharField(db_column='C104', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Autoriza Pago
    porcentaje_limite_credito = models.CharField(db_column='C105', max_length=4, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Impuesto Local
    cliente_repsico = models.CharField(db_column='C106', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Horario de Entrega
    class Meta:
        managed = False
        db_table = 'KDUD'

class Kdvdiremb(models.Model):
    clave_cliente = models.CharField(db_column='C1', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')  # Clave del Cliente
    clave_direccion = models.CharField(db_column='C2', max_length=7, db_collation='Traditional_Spanish_CI_AS')  # Clave de la dirección
    direccion_embarque = models.CharField(db_column='C3', max_length=80, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Dirección de Embarque
    calle_numero = models.CharField(db_column='C4', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Calle y Número
    colonia = models.CharField(db_column='C5', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Colonia
    poblacion = models.CharField(db_column='C6', max_length=40, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Población
    codigo_postal = models.CharField(db_column='C7', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Código Postal
    telefono1 = models.CharField(db_column='C8', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Teléfono 1
    telefono2 = models.CharField(db_column='C9', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Teléfono 2
    fax = models.CharField(db_column='C10', max_length=14, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Fax
    lada = models.CharField(db_column='C11', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Lada
    cobrador = models.CharField(db_column='C13', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Cobrador
    responsable = models.CharField(db_column='C14', max_length=50, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Responsable
    dias_recibo = models.CharField(db_column='C15', max_length=25, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Días de Recibo
    hora_recibo_inicial = models.CharField(db_column='C16', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Hora de Recibo (inicial)
    hora_recibo_final = models.CharField(db_column='C17', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Hora de Recibo (final)
    email = models.CharField(db_column='C18', max_length=150, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Email
    agrupacion_clientes = models.CharField(db_column='C19', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Agrupación de Clientes
    sucursal_pertenece = models.CharField(db_column='C20', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Sucursal a la que pertenece
    ruta_pertenece = models.DecimalField(db_column='C21', max_digits=3, decimal_places=0, blank=True, null=True)  # Ruta a la que pertenece
    giro = models.CharField(db_column='C22', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Giro
    analista = models.CharField(db_column='C23', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Analista
    zona_consignatario = models.CharField(db_column='C25', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Zona del Consignatario
    clave_vendedor = models.CharField(db_column='C26', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clave del Vendedor
    clave_degustador = models.CharField(db_column='C27', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clave del Degustador
    codigo_tp_proveedor = models.CharField(db_column='C30', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Código t.p. del proveedor
    calificacion_tp_proveedor = models.CharField(db_column='C31', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Calificación t.p. del proveedor
    ean_proveedor = models.CharField(db_column='C32', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # EAN proveedor
    numero_proveedor = models.CharField(db_column='C33', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Número de proveedor
    ean_tienda = models.CharField(db_column='C34', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # EAN tienda
    numero_tienda = models.CharField(db_column='C35', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Número de tienda
    numero_exterior_tienda = models.CharField(db_column='C36', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Número Exterior tienda
    numero_interior_tienda = models.CharField(db_column='C37', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Número Interior tienda
    localidad_tienda = models.CharField(db_column='C38', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Localidad Tienda
    referencia_tienda = models.CharField(db_column='C39', max_length=60, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Referencia Tienda
    municipio_tienda = models.CharField(db_column='C40', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Municipio Tienda
    estado_tienda = models.CharField(db_column='C41', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Estado Tienda
    pais_tienda = models.CharField(db_column='C42', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # País Tienda
    rfc_tienda = models.CharField(db_column='C43', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # RFC tienda
    codigo_zona = models.CharField(db_column='C44', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Código Zona
    gln = models.CharField(db_column='C45', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # GLN
    clave_promotora = models.CharField(db_column='C46', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clave Promotora
    clave_supervisor = models.CharField(db_column='C47', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clave Supervisor
    clave_tipo_tienda = models.CharField(db_column='C49', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Clave Tipo de Tienda
    nombre_tipo_tienda = models.CharField(db_column='C50', max_length=80, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Nombre Tipo de Tienda
    dias_revision = models.CharField(db_column='C51', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Días Revisión
    hora_revision = models.CharField(db_column='C52', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Hora Revisión
    dias_pago = models.CharField(db_column='C53', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Días Pago
    hora_pago = models.CharField(db_column='C54', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Hora Pago
    dias_visita = models.CharField(db_column='C55', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Días Visita
    hora_visita = models.CharField(db_column='C56', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Hora Visita
    contacto_cuenta = models.CharField(db_column='C57', max_length=80, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Contacto cUENTA
    estatus_comunicacion = models.CharField(db_column='C64', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Status de comunicación
    estatus_vigente = models.CharField(db_column='C65', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Status Vigente
    digito_verificador_banco = models.CharField(db_column='C68', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Digito Verificador Banco
    referencia_bancaria = models.CharField(db_column='C69', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Referencia Bancaria
    lunes = models.CharField(db_column='C71', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # LUNES
    martes = models.CharField(db_column='C72', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # MARTES
    miercoles = models.CharField(db_column='C73', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # MIÉRCOLES
    jueves = models.CharField(db_column='C74', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # JUEVES
    viernes = models.CharField(db_column='C75', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # VIERNES
    sabado = models.CharField(db_column='C76', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # SÁBADO
    domingo = models.CharField(db_column='C77', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # DOMINGO
    segmentacion = models.CharField(db_column='C78', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # SEGMENTACIÓN

    class Meta:
        managed = False
        db_table = 'KDVDIREMB'
        
class Festivo(models.Model):
    numero = models.CharField(db_column='C1', primary_key=True, max_length=10, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    dia_festivo = models.DateTimeField(db_column='C2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FESTIVO'

class Kdfecfdivta(models.Model):
    clave_sucursal = models.CharField(db_column='C1', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')
    genero_movimiento = models.CharField(db_column='C2', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    naturaleza = models.CharField(db_column='C3', max_length=1, db_collation='Traditional_Spanish_CI_AS')
    numero_grupo_movimiento = models.DecimalField(db_column='C4', max_digits=2, decimal_places=0)
    numero_tipo_movimiento = models.DecimalField(db_column='C5', max_digits=2, decimal_places=0)
    folio_documento = models.CharField(db_column='C6', max_length=7, db_collation='Traditional_Spanish_CI_AS')
    fecha_documento = models.DateTimeField(db_column='C7', blank=True, null=True)
    serie_sucursal = models.CharField(db_column='C8', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    clave_cliente = models.CharField(db_column='C9', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    rfc_cliente = models.CharField(db_column='C10', max_length=13, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    serie_ekomercio = models.CharField(db_column='C11', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    folio_ekomercio = models.CharField(db_column='C12', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    rfc_receptor_ekomercio = models.CharField(db_column='C13', max_length=13, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    folio_fiscal_uuid_ekomercio = models.CharField(db_column='C14', max_length=36, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)
    fecha_timbrado_ekomercio = models.DateTimeField(db_column='C15', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KDFECFDIVTA'

class Kdsegmentacion(models.Model):
    clave_segmentacion = models.CharField(db_column='C1', primary_key=True, max_length=5, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    descripcion_segmentacion = models.CharField(db_column='C2', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDSEGMENTACION'

class Kdif(models.Model):
    clave_grupo = models.CharField(db_column='C1', primary_key=True, max_length=5, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    descripcion_grupo = models.CharField(db_column='C2', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    campo_informativo = models.CharField(db_column='C3', max_length=16, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    almacen_default = models.DecimalField(db_column='C4', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDIF'

class Kdig(models.Model):
    clave_linea = models.CharField(db_column='C1', primary_key=True, max_length=5, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    descripcion_linea = models.CharField(db_column='C2', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    almacen_default = models.DecimalField(db_column='C4', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDIG'

class Kdcorpo(models.Model):
    clave_corporativo = models.CharField(db_column='C1', primary_key=True, max_length=7, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    descripcion_corporativo = models.CharField(db_column='C2', max_length=80, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    tipo_grupo = models.CharField(db_column='C3', max_length=2, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDCORPO'
        
class Kdregiones(models.Model):
    clave_region = models.CharField(db_column='C1', primary_key=True, max_length=3, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    descripcion_region = models.CharField(db_column='C2', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDREGIONES'

class Kdpord(models.Model):
    order_trabajo = models.CharField(db_column='C1', primary_key=True, max_length=10, db_collation='Traditional_Spanish_CI_AS')  # Field name made lowercase.
    estatus = models.CharField(db_column='C2', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    producto = models.CharField(db_column='C3', max_length=18, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    c4 = models.CharField(db_column='C4', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fecha_compromiso = models.DateTimeField(db_column='C6', blank=True, null=True)  # Field name made lowercase.
    hora_compromiso = models.CharField(db_column='C7', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nivel_ingenieria_orden = models.DecimalField(db_column='C8', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    cantidad_unidades = models.FloatField(db_column='C9', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='C10', max_length=3, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    factor = models.DecimalField(db_column='C11', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    entrega_sugerida = models.CharField(db_column='C12', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cantidad_acumulada = models.FloatField(db_column='C13', blank=True, null=True)  # Field name made lowercase.
    fecha_inicial = models.DateTimeField(db_column='C14', blank=True, null=True)  # Field name made lowercase.
    hora_inicial = models.CharField(db_column='C15', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fecha_final = models.DateTimeField(db_column='C16', blank=True, null=True)  # Field name made lowercase.
    hora_final = models.CharField(db_column='C17', max_length=5, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sucursal_de_orden = models.CharField(db_column='C19', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    genero_de_orden = models.CharField(db_column='C20', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    naturaleza = models.CharField(db_column='C21', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    grupo = models.DecimalField(db_column='C22', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tipo = models.DecimalField(db_column='C23', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    folio_orden = models.CharField(db_column='C24', max_length=7, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    partida = models.DecimalField(db_column='C25', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    consecutivo = models.DecimalField(db_column='C26', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    talla = models.CharField(db_column='C28', max_length=20, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    modelo = models.CharField(db_column='C29', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='C30', max_length=10, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    campo_tmc_4 = models.CharField(db_column='C31', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    campo_tmc_5 = models.CharField(db_column='C32', max_length=1, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ruta_a_seguir = models.DecimalField(db_column='C33', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='C35', max_length=30, db_collation='Traditional_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KDPORD'
