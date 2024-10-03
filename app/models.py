# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Abastecimentos(models.Model):
    tattica_veiculo = models.ForeignKey('TatticaVeiculos', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    tipos_abastecimento = models.ForeignKey('TiposAbastecimentos', on_delete=models.PROTECT, blank=True, null=True)
    data_abastecimento = models.DateField()
    km_atual = models.CharField(max_length=45, blank=True, null=True)
    numero_bloco = models.CharField(max_length=45, blank=True, null=True)
    qtd_litros = models.CharField(max_length=45, blank=True, null=True)
    total = models.CharField(max_length=45, blank=True, null=True)
    valor_por_litro = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'abastecimentos'

    def __str__(self):
        veiculo = self.tattica_veiculo if self.tattica_veiculo else "Veículo não especificado"
        funcionario = self.tattica_funcionario if self.tattica_funcionario else "Funcionário não especificado"
        return f"{veiculo} - {funcionario} - {self.data_abastecimento}"


class AberturasPortas(models.Model):
    pgm = models.ForeignKey('Pgms', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    condominios_funcionario = models.ForeignKey('CondominiosFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    liberacoes_chave = models.ForeignKey('LiberacoesChaves', on_delete=models.PROTECT, blank=True, null=True)
    lat = models.CharField(max_length=45, blank=True, null=True)
    lng = models.CharField(max_length=45, blank=True, null=True)
    distancia = models.IntegerField(blank=True, null=True)
    qrcode = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.CharField(max_length=225, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aberturas_portas'

    def __str__(self):
        return f"{self.pessoa} - {self.condominios_funcionario}"


class AcessosApp(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True)
    data_acesso = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acessos_app'

    def __str__(self):
        return f"Acesso de {self.user} em {self.data_acesso}" if self.user else f"Acesso não atribuído em {self.data_acesso}"



class AgendamentoHorarios(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.PROTECT, blank=True, null=True)
    area = models.ForeignKey('Areas', on_delete=models.PROTECT, blank=True, null=True)
    horario_inicio = models.CharField(max_length=20)
    horario_fim = models.CharField(max_length=20)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agendamento_horarios'

    def __str__(self):
        return f"{self.condominio} - {self.area} - {self.horario_inicio} - {self.horario_fim}"



class Agendamentos(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.PROTECT, blank=True, null=True)
    area = models.ForeignKey('Areas', on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey('Apartamentos', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    hora_inicio = models.CharField(max_length=20, blank=True, null=True)
    hora_fim = models.CharField(max_length=20, blank=True, null=True)
    mudanca = models.IntegerField(blank=True, null=True)
    outrostext = models.TextField(blank=True, null=True)
    adm = models.IntegerField(db_comment='1 - Informar; 2 - Ciente ')
    zelador = models.IntegerField(db_comment='1 - Informar; 2 - Ciente')
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agendamentos'

    def __str__(self):
        return f"{self.condominio} - {self.area} - {self.apartamento} - {self.tattica_funcionario}"



class Apartamentos(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.CASCADE, blank=True, null=True)
    nome_apartamento = models.CharField(max_length=45)
    ramal_apartamento = models.CharField(max_length=45, blank=True, null=True)
    telefone = models.CharField(max_length=45, blank=True, null=True)
    senha = models.CharField(max_length=10, blank=True, null=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apartamentos'

    def __str__(self):
        return f"{self.condominio} - {self.nome_apartamento}"


class Areas(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.CASCADE, blank=True, null=True)
    nome_area = models.CharField(max_length=220, db_collation='latin1_swedish_ci')
    andar = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    limite_pessoas = models.IntegerField(blank=True, null=True)
    valor = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    normas = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    info = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    cor = models.CharField(max_length=20, db_collation='latin1_swedish_ci', blank=True, null=True)
    pgm = models.ForeignKey('Pgms', on_delete=models.CASCADE, blank=True, null=True)
    hora_min = models.CharField(max_length=6, db_collation='latin1_swedish_ci', blank=True, null=True)
    hora_max = models.CharField(max_length=6, db_collation='latin1_swedish_ci', blank=True, null=True)
    antecedencia_min = models.CharField(max_length=9, db_collation='latin1_swedish_ci', blank=True, null=True)
    antecedencia_max = models.IntegerField(blank=True, null=True)
    intervalo_entre_reservas = models.CharField(max_length=6, db_collation='latin1_swedish_ci', blank=True, null=True)
    max_abertos = models.IntegerField(blank=True, null=True)
    tempo_entre_reservas = models.IntegerField(blank=True, null=True)
    tipo_reserva = models.IntegerField(blank=True, null=True)
    hora_inicio_permitido = models.CharField(max_length=6, db_collation='latin1_swedish_ci', blank=True, null=True)
    hora_fim_permitido = models.CharField(max_length=6, db_collation='latin1_swedish_ci', blank=True, null=True)
    hora_inicio_permitido_fds = models.CharField(max_length=6, blank=True, null=True)
    hora_fim_permitido_fds = models.CharField(max_length=6, blank=True, null=True)
    segunda = models.IntegerField(blank=True, null=True)
    terca = models.IntegerField(blank=True, null=True)
    quarta = models.IntegerField(blank=True, null=True)
    quinta = models.IntegerField(blank=True, null=True)
    sexta = models.IntegerField(blank=True, null=True)
    sabado = models.IntegerField(blank=True, null=True)
    domingo = models.IntegerField(blank=True, null=True)
    tem_feriados = models.IntegerField(blank=True, null=True)
    permite_convidados = models.IntegerField(blank=True, null=True)
    necessita_aprovacao = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'areas'

    def __str__(self):
        return f"{self.condominio} - {self.nome_area}"


class AreasParalelas(models.Model):
    area = models.ForeignKey(Areas, on_delete=models.CASCADE, blank=True, null=True)
    area2 = models.ForeignKey(Areas, models.CASCADE, related_name='areasparalelas_area2_set')
    tipo = models.IntegerField(db_comment='1 - Concorrente / 2 - Conjunto')
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'areas_paralelas'

    def __str__(self):
        return f"{self.area} - {self.area2}"


class Atendimentos(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.PROTECT, blank=True, null=True)
    chamada = models.ForeignKey('Chamadas', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    liberacoes_acesso = models.ForeignKey('LiberacoesAcessos', on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    condominios_funcionario = models.ForeignKey('CondominiosFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    funcionario = models.ForeignKey('Funcionarios', on_delete=models.PROTECT, blank=True, null=True)
    empresa = models.ForeignKey('Empresas', on_delete=models.PROTECT, blank=True, null=True)
    tipo_atendimento = models.IntegerField(blank=True, null=True)
    busca = models.CharField(max_length=100, blank=True, null=True)
    acoes = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atendimentos'

    def __str__(self):
        return f"{self.condominio} - {self.chamada}"


class Atividades(models.Model):
    ocorrencia = models.ForeignKey('Ocorrencias', on_delete=models.PROTECT, blank=True, null=True)
    departamento = models.ForeignKey('Departamentos', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    colaborador = models.ForeignKey('TatticaFuncionarios', models.DO_NOTHING, related_name='atividades_colaborador_set', blank=True, null=True)
    atividade = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    descricao = models.TextField()
    observacao = models.TextField(blank=True, null=True)
    local = models.IntegerField(db_comment='1 - Interno; 2 - Externo')
    pin_status = models.IntegerField(blank=True, null=True, db_comment='1 - pinned; 0 - unpinned;')
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    observacao_cli = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atividades'

    def __str__(self):
        return f"{self.condominio} - {self.chamada}"


class AtividadesMateriaisProdutos(models.Model):
    atividade = models.ForeignKey(Atividades, on_delete=models.PROTECT, blank=True, null=True)
    materiais_produto = models.ForeignKey('MateriaisProdutos', on_delete=models.PROTECT, blank=True, null=True)
    qtd = models.CharField(max_length=45)
    data_saida = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atividades_materiais_produtos'

    def __str__(self):
        return f"{self.condominio} - {self.chamada}"


class AtividadesOrdemdeservicos(models.Model):
    atividade = models.ForeignKey(Atividades, on_delete=models.PROTECT, blank=True, null=True)
    ordemdeservico = models.ForeignKey('Ordemdeservicos', on_delete=models.PROTECT, blank=True, null=True)
    resolucao = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atividades_ordemdeservicos'

    def __str__(self):
        return f"{self.condominio} - {self.chamada}"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'

    def __str__(self):
        return self.name


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, on_delete=models.PROTECT, blank=True, null=True)
    permission = models.ForeignKey('AuthPermission', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

    def __str__(self):
        return f"{self.group} - {self.permission}"


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.PROTECT, blank=True, null=True)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

    def __str__(self):
        return self.name


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

    def __str__(self):
        return self.username


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT, blank=True, null=True)
    group = models.ForeignKey(AuthGroup, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

    def __str__(self):
        return f"{self.user} - {self.group}"


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT, blank=True, null=True)
    permission = models.ForeignKey(AuthPermission, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

    def __str__(self):
        return f"{self.user} - {self.permission}"


class CamFacials(models.Model):
    config_facial = models.ForeignKey('ConfigFacials', on_delete=models.PROTECT, blank=True, null=True)
    condominio = models.ForeignKey('Condominios', on_delete=models.PROTECT, blank=True, null=True)
    active = models.IntegerField()
    name = models.CharField(max_length=45)
    url = models.CharField(max_length=255)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    gamma = models.IntegerField(blank=True, null=True)
    tolerance = models.IntegerField(blank=True, null=True)
    threshold = models.IntegerField(blank=True, null=True)
    roi_left = models.IntegerField(blank=True, null=True)
    roi_top = models.IntegerField(blank=True, null=True)
    roi_right = models.IntegerField(blank=True, null=True)
    roi_bottom = models.IntegerField(blank=True, null=True)
    pgm = models.ForeignKey('Pgms', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cam_facials'

    def __str__(self):
        return f"{self.condominio} - {self.name}"


class CardsElevadors(models.Model):
    dispositivo = models.ForeignKey('Dispositivos', on_delete=models.PROTECT, blank=True, null=True)
    nome_cartao = models.CharField(max_length=45)
    codigo = models.CharField(max_length=45)
    ativado = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cards_elevadors'

    def __str__(self):
        return f"{self.dispositivo} - {self.nome_cartao}"


class CentraisJfls(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.PROTECT, blank=True, null=True)
    ip = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45, blank=True, null=True)
    versao = models.CharField(max_length=8, blank=True, null=True)
    mac = models.CharField(max_length=45, blank=True, null=True)
    ativada = models.IntegerField()
    data_ultima_conexao = models.DateTimeField(blank=True, null=True)
    part1 = models.IntegerField()
    part2 = models.IntegerField()
    part3 = models.IntegerField()
    part4 = models.IntegerField()
    sirene = models.IntegerField()
    problema = models.IntegerField()
    ordem = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'centrais_jfls'

    def __str__(self):
        return f"{self.condominio} - {self.ip}"


class Chamadas(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    tip = models.ForeignKey('Tips', on_delete=models.PROTECT, blank=True, null=True)
    audio = models.CharField(max_length=45, blank=True, null=True)
    digitado_para = models.CharField(max_length=45, blank=True, null=True)
    duracao = models.CharField(max_length=45, blank=True, null=True)
    tempo_espera = models.CharField(max_length=45, blank=True, null=True)
    data_start = models.DateTimeField()
    data_atendimento = models.DateTimeField(blank=True, null=True)
    data_desligamento = models.DateTimeField()
    ptah_js = models.IntegerField()
    atendeu = models.IntegerField()
    status = models.IntegerField(db_comment='1 - Atendendo, 2 - Ligando')
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chamadas'

    def __str__(self):
        return f"{self.condominio} - {self.tattica_funcionario}"


class ChavesVirtuais(models.Model):
    liberacoes_acesso = models.ForeignKey('LiberacoesAcessos', on_delete=models.PROTECT, blank=True, null=True)
    link_chave = models.CharField(unique=True, max_length=100)
    qtd_max = models.IntegerField(blank=True, null=True)
    qtd_usado = models.IntegerField(blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    hora_inicio = models.CharField(max_length=50, blank=True, null=True)
    hora_fim = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chaves_virtuais'

    def __str__(self):
        return f"{self.liberacoes_acesso} - {self.link_chave}"


class ChecklistObras(models.Model):
    nome = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checklist_obras'

    def __str__(self):
        return f"{self.nome}"


class Codigos(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    codigo = models.CharField(unique=True, max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'codigos'

    def __str__(self):
        return f"{self.condominio} - {self.apartamento} - {self.pessoa} - {self.codigo}"


class ComercialEtapas(models.Model):
    nome = models.CharField(max_length=50)
    tempo = models.IntegerField(blank=True, null=True)
    ordem = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comercial_etapas'

    def __str__(self):
        return f"{self.nome}"


class ComercialLeadEtapas(models.Model):
    comercial_lead = models.ForeignKey('ComercialLeads', on_delete=models.PROTECT, blank=True, null=True)
    comercial_etapa = models.ForeignKey(ComercialEtapas, on_delete=models.PROTECT, blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comercial_lead_etapas'

    def __str__(self):
        return f"{self.comercial_lead} - {self.comercial_etapa}"


class ComercialLeadProcessos(models.Model):
    comercial_lead = models.ForeignKey('ComercialLeads', on_delete=models.PROTECT, blank=True, null=True)
    comercial_processo = models.ForeignKey('ComercialProcessos', on_delete=models.PROTECT, blank=True, null=True)
    colaborador = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    data_execucao = models.DateField()
    situacao = models.IntegerField()
    obs = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comercial_lead_processos'

    def __str__(self):
        return f"{self.comercial_lead} - {self.comercial_processo}"

class ComercialLeads(models.Model):
    nome = models.CharField(max_length=225, blank=True, null=True)
    endereco = models.CharField(max_length=225, blank=True, null=True)
    responsavel = models.CharField(max_length=225, blank=True, null=True)
    cargo = models.CharField(max_length=45, blank=True, null=True)
    telefone = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    forma_contato = models.CharField(max_length=45, blank=True, null=True)
    tipo_portaria = models.IntegerField(blank=True, null=True)
    problema_relatado = models.CharField(max_length=255, blank=True, null=True)
    qtde_apartamentos = models.IntegerField(blank=True, null=True)
    forma_encontrou_tattica = models.CharField(max_length=225, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comercial_leads'

    def __str__(self):
        return f"{self.nome}"


class ComercialProcessos(models.Model):
    nome = models.CharField(max_length=225)
    descricao = models.CharField(max_length=255)
    tempo = models.IntegerField(blank=True, null=True)
    comercial_etapa = models.ForeignKey(ComercialEtapas, on_delete=models.PROTECT, blank=True, null=True)
    colaborador = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    obrigatorio = models.IntegerField(blank=True, null=True)
    arquivo_processo = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comercial_processos'

    def __str__(self):
        return f"{self.nome}"


class ComercialProspeccao(models.Model):
    cond_nome = models.CharField(max_length=100, blank=True, null=True, db_comment='Nome do condom�nio a qual o contato est� realizando o contato.')
    contato_nome = models.CharField(max_length=100, blank=True, null=True, db_comment='Nome do contato que fez a prospec��o')
    contato_telefone = models.CharField(max_length=45, blank=True, null=True, db_comment='Telefone do contato que fez a prospec��o.')
    contato_email = models.CharField(max_length=100, blank=True, null=True, db_comment='Email do contato a qual est� realizando a prospec��o.')
    contato_cargo = models.CharField(max_length=45, blank=True, null=True, db_comment='Cargo do contato no condom�nio a qual est� realizando a prospec��o. ')
    contato_origem = models.CharField(max_length=45, blank=True, null=True, db_comment='Como contato ficou sabendo a respeito da Tattica.')
    cond_qtd_apt = models.IntegerField(blank=True, null=True, db_comment='Quantidade de apartamento dentro do condom�nio a qual est� realizando a prospec��o.')
    cond_tipo_port = models.CharField(max_length=45, blank=True, null=True, db_comment='Tipo de portaria no condom�nio a qual est� realizando a prospec��o.')
    observacao = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comercial_prospeccao'

    def __str__(self):
        return f"{self.cond_nome}"


class Comodatos(models.Model):
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    patrimonio = models.ForeignKey('Patrimonios', on_delete=models.PROTECT, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comodatos'

    def __str__(self):
        return f"{self.tattica_funcionario}"


class CondominioEquipamentos(models.Model):
    condominio = models.ForeignKey('Condominios', on_delete=models.PROTECT, blank=True, null=True)
    tipos_equipamentos = models.ForeignKey('TiposEquipamentos', on_delete=models.PROTECT, blank=True, null=True)
    estado_equipamento = models.ForeignKey('EstadosEquipamentos', on_delete=models.PROTECT, blank=True, null=True)
    nome_condequipamento = models.CharField(max_length=220)
    modelo = models.CharField(max_length=220, blank=True, null=True)
    marca = models.CharField(max_length=220, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    data_instalacao = models.DateField(blank=True, null=True)
    valor_condequipamento = models.FloatField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condominio_equipamentos'

    def __str__(self):
        return f"{self.condominio}"


class Condominios(models.Model):
    internet = models.ForeignKey('Internets', on_delete=models.PROTECT, blank=True, null=True)
    unidade = models.ForeignKey('Unidades', on_delete=models.PROTECT, blank=True, null=True)
    suporteunidade = models.ForeignKey('Suporteunidades', on_delete=models.PROTECT, blank=True, null=True)
    entregadores_norma = models.ForeignKey('EntregadoresNormas', on_delete=models.PROTECT, blank=True, null=True)
    prestadores_norma = models.ForeignKey('PrestadoresNormas', on_delete=models.PROTECT, blank=True, null=True)
    reservas_norma = models.ForeignKey('ReservasNormas', on_delete=models.PROTECT, blank=True, null=True)
    mudancas_norma = models.ForeignKey('MudancasNormas', on_delete=models.PROTECT, blank=True, null=True)
    responsavel_tattica = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    norma_observacao = models.TextField(blank=True, null=True)
    nome_condominio = models.CharField(max_length=220)
    data_condominio = models.DateField(blank=True, null=True)
    dias_implantacao = models.IntegerField(blank=True, null=True)
    ramal_condominio = models.CharField(max_length=45, blank=True, null=True)
    ramal_interno = models.CharField(max_length=45, blank=True, null=True)
    cnpj = models.CharField(max_length=45, blank=True, null=True)
    logradouro = models.CharField(max_length=220, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=220, blank=True, null=True)
    bairro = models.CharField(max_length=220, blank=True, null=True)
    cidade = models.CharField(max_length=220, blank=True, null=True)
    uf = models.CharField(max_length=5, blank=True, null=True)
    cep = models.CharField(max_length=45, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    cameras_usuario = models.CharField(max_length=45, blank=True, null=True)
    cameras_senha = models.CharField(max_length=45, blank=True, null=True)
    cameras_usuario_sindico = models.CharField(max_length=45, blank=True, null=True)
    cameras_senha_sindico = models.CharField(max_length=45, blank=True, null=True)
    website = models.CharField(max_length=220, blank=True, null=True)
    website_agendamento = models.CharField(max_length=225, blank=True, null=True)
    telefone = models.CharField(max_length=45, blank=True, null=True)
    financeiro_responsavel = models.CharField(max_length=220, blank=True, null=True)
    financeiro_email = models.CharField(max_length=220, blank=True, null=True)
    arquivo_contrato = models.CharField(max_length=200, blank=True, null=True)
    acesso_aplicativo = models.IntegerField(blank=True, null=True)
    mod_acessos = models.IntegerField(blank=True, null=True)
    mod_qrcode = models.IntegerField(blank=True, null=True)
    mod_chave_virtual = models.IntegerField(blank=True, null=True)
    dias_chave_virtual = models.IntegerField(blank=True, null=True)
    distancia = models.IntegerField(blank=True, null=True)
    link_ri = models.CharField(max_length=220, blank=True, null=True)
    empresa = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condominios'

    def __str__(self):
        return f"{self.nome_condominio}"


class CondominiosFeriados(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    feriado = models.ForeignKey('Feriados', on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condominios_feriados'

    def __str__(self):
        return f"{self.feriado}"


class CondominiosFuncionarios(models.Model):
    tipos_condominios_funcionario = models.ForeignKey('TiposCondominiosFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    nome_condominios_funcionario = models.CharField(max_length=220)
    telefone1 = models.CharField(max_length=45, blank=True, null=True)
    telefone2 = models.CharField(max_length=45, blank=True, null=True)
    hora_inicio = models.CharField(max_length=20, blank=True, null=True)
    hora_inicio_sab = models.CharField(max_length=20, blank=True, null=True)
    hora_fim_sab = models.CharField(max_length=20, blank=True, null=True)
    hora_fim = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condominios_funcionarios'

    def __str__(self):
        return f"{self.nome_condominios_funcionario}"


class CondominiosFuncionariosDispositivosRoles(models.Model):
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_role = models.ForeignKey('DispositivosRoles', on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condominios_funcionarios_dispositivos_roles'

    def __str__(self):
        return f"{self.dispositivos_role}"


class ConfigFacials(models.Model):
    nome_sv = models.CharField(max_length=45)
    ip_sv = models.CharField(max_length=45)
    gui = models.IntegerField()
    extract = models.IntegerField()
    resize = models.IntegerField()
    win_size = models.IntegerField()
    show_match = models.IntegerField()
    step_frame = models.IntegerField()
    tolerance = models.IntegerField()
    threshold = models.IntegerField()
    resolution_x = models.IntegerField()
    resolution_y = models.IntegerField()
    webhook = models.CharField(max_length=255)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config_facials'

    def __str__(self):
        return f"{self.nome_sv}"


class ConfigOs(models.Model):
    hora_inicio = models.CharField(max_length=6)
    hora_fim = models.CharField(max_length=6)
    motivo = models.CharField(max_length=225, blank=True, null=True)
    ativo = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config_os'

    def __str__(self):
        return f"{self.motivo}"


class ContatoEmergencias(models.Model):
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    nome = models.CharField(max_length=220)
    celular = models.CharField(max_length=45)
    celular_2 = models.CharField(max_length=45, blank=True, null=True)
    parentesco = models.CharField(max_length=200, blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contato_emergencias'

    def __str__(self):
        return f"{self.nome}"


class ControlesAcessos(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tipos_controles_acesso = models.ForeignKey('TiposControlesAcessos', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    sindico = models.ForeignKey('Sindicos', on_delete=models.PROTECT, blank=True, null=True)
    entregador = models.ForeignKey('TatticaFuncionarios', models.DO_NOTHING, related_name='controlesacessos_entregador_set', blank=True, null=True)
    realizador = models.ForeignKey('TatticaFuncionarios', models.DO_NOTHING, related_name='controlesacessos_realizador_set', blank=True, null=True)
    solicitante = models.CharField(max_length=100, blank=True, null=True)
    execucao = models.IntegerField(blank=True, null=True, db_comment='1 - Presencial; 2 - Remoto')
    pedido = models.IntegerField(blank=True, null=True, db_comment='1 - Gratuito, 2 - Aguardando Pagamento, 6  - A receber em dinheiro, 7 - A receber por Pagseguro, 8 - A receber por transfer�ncia, 3 - Pago em dinheiro, 5 - Pago por Pagseguro, 4 - Pago por transfer�ncia, 9 - Em Analise')
    quantidade = models.IntegerField(blank=True, null=True)
    valor = models.CharField(max_length=45, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    identificador = models.TextField(blank=True, null=True)
    agendado = models.IntegerField(blank=True, null=True, db_comment='0 - Pedido normal; 1 - Pedido agendado; ')
    promo_status = models.IntegerField(blank=True, null=True)
    data_prazo = models.DateField(blank=True, null=True)
    data_entrega = models.DateTimeField(blank=True, null=True)
    data_final = models.DateField(blank=True, null=True)
    data_pagamento = models.DateTimeField(blank=True, null=True)
    comprador_nome = models.CharField(max_length=255, blank=True, null=True)
    comprador_email = models.CharField(max_length=255, blank=True, null=True)
    comprador_cpf = models.CharField(max_length=15, blank=True, null=True)
    comprador_telefone = models.CharField(max_length=15, blank=True, null=True)
    metodo_pagamento = models.IntegerField(blank=True, null=True, db_comment='1 - Cart�o de Cr�dito, 2 - Boleto, 3 - D�bito, 4 - Saldo PagSeguro, 5 - Oi Paggo, 7 - D�posito em conta, 11 - PIX')
    link_boleto = models.TextField(blank=True, null=True)
    codigo_pagseguro = models.CharField(max_length=255, blank=True, null=True)
    status_pagseguro = models.IntegerField(blank=True, null=True, db_comment='1 - Aguardando Pagamento, 2 - Em analise, 3 - Paga, 4 - Dispon�vel, 5 - Em disputa, 6 - Devolvida, 7 - Cancelada, 8 - Debitado, 9 - Reten��o tempor�ria')
    status = models.IntegerField(db_comment='0 - Deletado\n1 - Pendente\n2 - a Entregar\n3 - Resolvido')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'controles_acessos'

    def __str__(self):
        return f"{self.tipos_controles_acesso}"


class Convidados(models.Model):
    agendamento = models.ForeignKey(Agendamentos, on_delete=models.PROTECT, blank=True, null=True)
    nome_convidado = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'convidados'

    def __str__(self):
        return f"{self.nome_convidado}"


class Criticidades(models.Model):
    nome_criticidade = models.CharField(max_length=100)
    icone_criticidade = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'criticidades'

    def __str__(self):
        return f"{self.nome_criticidade}"


class Departamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome_departamento = models.CharField(max_length=45)
    sigla = models.CharField(max_length=45, blank=True, null=True)
    ramal_departamento = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departamento'

    def __str__(self):
        return f"{self.nome_departamento}"


class Departamentos(models.Model):
    nome_departamento = models.CharField(max_length=45)
    sigla = models.CharField(max_length=45, blank=True, null=True)
    ramal_departamento = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departamentos'

    def __str__(self):
        return f"{self.nome_departamento}"


class Dispositivos(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_modelo = models.ForeignKey('DispositivosModelos', on_delete=models.PROTECT, blank=True, null=True)
    nome_dispositivo = models.CharField(max_length=45)
    ip = models.CharField(max_length=45)
    versao = models.CharField(max_length=45, blank=True, null=True)
    mac = models.CharField(max_length=45, blank=True, null=True)
    device_id = models.BigIntegerField(blank=True, null=True)
    device_name = models.CharField(max_length=45, blank=True, null=True)
    data_ultima_conexao = models.DateTimeField(blank=True, null=True)
    user = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos'

    def __str__(self):
        return f"{self.nome_dispositivo}"


class DispositivosAcessos(models.Model):
    dispositivo = models.ForeignKey(Dispositivos, on_delete=models.PROTECT, blank=True, null=True)
    nome_acesso = models.CharField(max_length=45)
    codigo = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_acessos'

    def __str__(self):
        return f"{self.nome_acesso}"


class DispositivosCards(models.Model):
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    permissao_acessos = models.ForeignKey('PermissaoAcessos', on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_cards_tipo = models.ForeignKey('DispositivosCardsTipos', on_delete=models.PROTECT, blank=True, null=True)
    veiculo = models.ForeignKey('Veiculos', on_delete=models.PROTECT, blank=True, null=True)
    nome_card = models.CharField(max_length=45, blank=True, null=True)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    biometria = models.TextField(blank=True, null=True)
    face = models.TextField(blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)
    finger_position = models.IntegerField(blank=True, null=True)
    data_bloqueio = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_cards'

    def __str__(self):
        return f"{self.nome_card}"


class DispositivosCardsTipos(models.Model):
    nome_card_tipo = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_cards_tipos'

    def __str__(self):
        return f"{self.nome_card_tipo}"


class DispositivosEventos(models.Model):
    evento = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_eventos'

    def __str__(self):
        return f"{self.evento}"


class DispositivosMarcas(models.Model):
    nome_marca = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_marcas'

    def __str__(self):
        return f"{self.nome_marca}"


class DispositivosModelos(models.Model):
    dispositivos_tipo = models.ForeignKey('DispositivosTipos', on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_marca = models.ForeignKey(DispositivosMarcas, on_delete=models.PROTECT, blank=True, null=True)
    nome_modelo = models.CharField(max_length=45)
    identificador = models.CharField(max_length=45)
    biometria = models.IntegerField()
    tag = models.IntegerField()
    rf433 = models.IntegerField()
    senha = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_modelos'

    def __str__(self):
        return f"{self.nome_modelo}"


class DispositivosRegistros(models.Model):
    dispositivos_card = models.ForeignKey(DispositivosCards, on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_acesso = models.ForeignKey(DispositivosAcessos, on_delete=models.PROTECT, blank=True, null=True)
    dispositivo = models.ForeignKey(Dispositivos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    permissao_acessos = models.ForeignKey('PermissaoAcessos', on_delete=models.PROTECT, blank=True, null=True)
    card_elevador = models.ForeignKey(CardsElevadors, on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_evento = models.ForeignKey(DispositivosEventos, on_delete=models.PROTECT, blank=True, null=True)
    codigo_card = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_registros'

    def __str__(self):
        return f"{self.dispositivo}"


class DispositivosRoles(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    nome_role = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_roles'

    def __str__(self):
        return f"{self.nome_role}"


class DispositivosRolesDispositivosAcessos(models.Model):
    dispositivos_role = models.ForeignKey(DispositivosRoles, on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_acesso = models.ForeignKey(DispositivosAcessos, on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_roles_dispositivos_acessos'

    def __str__(self):
        return f"{self.dispositivos_role}"


class DispositivosTipos(models.Model):
    nome_tipo = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispositivos_tipos'

    def __str__(self):
        return f"{self.nome_tipo}"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.PROTECT, blank=True, null=True)
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_admin_log'

    def __str__(self):
        return f"{self.object_id}"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

    def __str__(self):
        return f"{self.model}"


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

    def __str__(self):
        return f"{self.name}"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

    def __str__(self):
        return f"{self.session_key}"


class Documentos(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    nome_documento = models.CharField(max_length=45)
    arquivo = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documentos'

    def __str__(self):
        return f"{self.arquivo}"


class ElevadorChamados(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    empresa = models.ForeignKey('Empresas', on_delete=models.PROTECT, blank=True, null=True)
    tipos_elevador_chamado = models.ForeignKey('TiposElevadorChamados', on_delete=models.PROTECT, blank=True, null=True)
    sindico = models.ForeignKey('Sindicos', on_delete=models.PROTECT, blank=True, null=True)
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    tattica_solicitante = models.ForeignKey('TatticaFuncionarios', models.DO_NOTHING, related_name='elevadorchamados_tattica_solicitante_set', blank=True, null=True)
    solicitante = models.CharField(max_length=200, blank=True, null=True)
    elevador = models.CharField(max_length=150)
    protocolo = models.CharField(max_length=45)
    atendente = models.CharField(max_length=150)
    andar = models.CharField(max_length=45, blank=True, null=True)
    hora_ligacao = models.CharField(max_length=45)
    descricao = models.TextField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'elevador_chamados'

    def __str__(self):
        return f"{self.elevador}"


class Empresas(models.Model):
    razao_social = models.CharField(max_length=220, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=220)
    cnpj = models.CharField(max_length=45, blank=True, null=True)
    imagem = models.CharField(max_length=45, blank=True, null=True)
    website = models.CharField(max_length=220, blank=True, null=True)
    telefone = models.CharField(max_length=45, blank=True, null=True)
    celular = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=220, blank=True, null=True)
    logradouro = models.CharField(max_length=220, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=220, blank=True, null=True)
    bairro = models.CharField(max_length=220, blank=True, null=True)
    cidade = models.CharField(max_length=220, blank=True, null=True)
    uf = models.CharField(max_length=5, blank=True, null=True)
    cep = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresas'

    def __str__(self):
        return f"{self.nome_fantasia}"


class EmpresasServicos(models.Model):
    nome_tipos_empresa = models.CharField(max_length=220)
    cor = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresas_servicos'

    def __str__(self):
        return f"{self.nome_tipos_empresa}"


class EmpresasServicosEmpresas(models.Model):
    empresas_servico = models.ForeignKey(EmpresasServicos, on_delete=models.PROTECT, blank=True, null=True)
    empresa = models.ForeignKey(Empresas, on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresas_servicos_empresas'

    def __str__(self):
        return f"{self.empresa}"


class Encomendas(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    tipos_encomenda = models.ForeignKey('TiposEncomendas', on_delete=models.PROTECT, blank=True, null=True)
    transportadora = models.CharField(max_length=100, blank=True, null=True)
    entregador = models.CharField(max_length=100, blank=True, null=True)
    remetente = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    data_recebimento = models.DateField()
    hora_recebimento = models.CharField(max_length=20)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'encomendas'

    def __str__(self):
        return f"{self.tipos_encomenda}"


class EntregadoresNormas(models.Model):
    nome_entregador_normas = models.CharField(max_length=220)
    cor = models.CharField(max_length=20, blank=True, null=True)
    icone = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entregadores_normas'

    def __str__(self):
        return f"{self.nome_entregador_normas}"


class EstadosEquipamentos(models.Model):
    nome_estados_equipamento = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estados_equipamentos'

    def __str__(self):
        return f"{self.nome_estados_equipamento}"


class Eventos(models.Model):
    centrais_jfl = models.ForeignKey(CentraisJfls, on_delete=models.PROTECT, blank=True, null=True)
    tipos_evento = models.ForeignKey('TiposEventos', on_delete=models.PROTECT, blank=True, null=True)
    zona = models.ForeignKey('Zonas', on_delete=models.PROTECT, blank=True, null=True)
    pgm = models.ForeignKey('Pgms', on_delete=models.PROTECT, blank=True, null=True)
    conta = models.CharField(max_length=4, blank=True, null=True)
    contador = models.CharField(max_length=4, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos'

    def __str__(self):
        return f"{self.tipos_evento}"


class EventosTratados(models.Model):
    tipos_eventos_tratado = models.ForeignKey('TiposEventosTratados', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    evento = models.ForeignKey(Eventos, on_delete=models.PROTECT, blank=True, null=True)
    descricao = models.TextField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos_tratados'

    def __str__(self):
        return f"{self.tipos_eventos_tratado}"


class Faturamentos(models.Model):
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tipos_pagamento = models.ForeignKey('TiposPagamentos', on_delete=models.PROTECT, blank=True, null=True)
    parcelas = models.ForeignKey('Parcelas', on_delete=models.PROTECT, blank=True, null=True)
    nome_faturamento = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    desconto = models.TextField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faturamentos'

    def __str__(self):
        return f"{self.nome_faturamento}"


class FaturamentosMateriais(models.Model):
    faturamento = models.ForeignKey(Faturamentos, on_delete=models.PROTECT, blank=True, null=True)
    materiais_produtos = models.ForeignKey('MateriaisProdutos', on_delete=models.PROTECT, blank=True, null=True)
    produtos_qtd = models.IntegerField(blank=True, null=True)
    valor = models.CharField(max_length=45, blank=True, null=True)
    desconto = models.CharField(max_length=45, blank=True, null=True)
    valor_custo = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faturamentos_materiais'

    def __str__(self):
        return f"{self.materiais_produtos}"


class FaturamentosOrcamentos(models.Model):
    faturamento = models.ForeignKey(Faturamentos, on_delete=models.PROTECT, blank=True, null=True)
    orcamento = models.ForeignKey('Orcamentos', on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faturamentos_orcamentos'

    def __str__(self):
        return f"{self.orcamento}"


class Feriados(models.Model):
    nome = models.CharField(max_length=45)
    data = models.CharField(max_length=5)
    sinc_acessos = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feriados'

    def __str__(self):
        return f"{self.nome}"


class Ferramentas(models.Model):
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    tattica_supervisor = models.ForeignKey('TatticaFuncionarios', models.DO_NOTHING, related_name='ferramentas_tattica_supervisor_set', blank=True, null=True)
    fornecedor = models.CharField(max_length=45, blank=True, null=True)
    nome_ferramenta = models.CharField(max_length=45, blank=True, null=True)
    qtde = models.IntegerField(blank=True, null=True)
    valor = models.CharField(max_length=45, blank=True, null=True)
    num_nota = models.CharField(max_length=45, blank=True, null=True)
    data_compra = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ferramentas'

    def __str__(self):
        return f"{self.nome_ferramenta}"


class Fotos(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tipos_foto = models.ForeignKey('TiposFotos', on_delete=models.PROTECT, blank=True, null=True)
    nome_foto = models.CharField(max_length=220, blank=True, null=True)
    imagem_foto = models.CharField(max_length=220)
    foto_dir = models.CharField(max_length=220)
    type = models.CharField(max_length=220)
    descricao = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fotos'

    def __str__(self):
        return f"{self.nome_foto}"


class Funcionarios(models.Model):
    empresa = models.ForeignKey(Empresas, on_delete=models.PROTECT, blank=True, null=True)
    tipos_funcionario = models.ForeignKey('TiposFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    nome_funcionario = models.CharField(max_length=220)
    cargo = models.CharField(max_length=220, blank=True, null=True)
    cpf = models.CharField(max_length=45, blank=True, null=True)
    rg = models.CharField(max_length=45, blank=True, null=True)
    telefone = models.CharField(max_length=45, blank=True, null=True)
    celular = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=220, blank=True, null=True)
    imagem_prestador = models.CharField(max_length=220, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funcionarios'

    def __str__(self):
        return f"{self.nome_funcionario}"


class GruposEventos(models.Model):
    nome_grupo_evento = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupos_eventos'

    def __str__(self):
        return f"{self.nome_grupo_evento}"


class GruposZonas(models.Model):
    nome_grupo_zona = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupos_zonas'

    def __str__(self):
        return f"{self.nome_grupo_zona}"


class HistoricoCondominios(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    sindico = models.ForeignKey('Sindicos', on_delete=models.PROTECT, blank=True, null=True)
    tipo_contato = models.IntegerField()
    data_execucao = models.DateField(blank=True, null=True)
    hora_execucao = models.CharField(max_length=45, blank=True, null=True)
    assunto = models.CharField(max_length=255, blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    alertar = models.IntegerField(blank=True, null=True)
    arquivo = models.CharField(max_length=225, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historico_condominios'

    def __str__(self):
        return f"{self.condominio}"


class HistoricoPessoas(models.Model):
    user = models.ForeignKey('Users', on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    apartamento_id = models.IntegerField(blank=True, null=True)
    tipos_pessoa_id = models.IntegerField(blank=True, null=True)
    criticidade_id = models.IntegerField(blank=True, null=True)
    responsavel = models.IntegerField(blank=True, null=True)
    nome_pessoa = models.CharField(max_length=220, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    cpf = models.CharField(max_length=45, blank=True, null=True)
    rg = models.CharField(max_length=45, blank=True, null=True)
    data_aniversario = models.DateField(blank=True, null=True)
    parentesco = models.CharField(max_length=220, blank=True, null=True)
    observacao = models.CharField(max_length=220, blank=True, null=True)
    celular = models.CharField(max_length=45, blank=True, null=True)
    celular_2 = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=220, blank=True, null=True)
    profissao = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historico_pessoas'

    def __str__(self):
        return f"{self.pessoa}"


class Imagemcameras(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario_id = models.IntegerField(blank=True, null=True)
    tattica_solicitante = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    apartamento_id = models.IntegerField(blank=True, null=True)
    pessoa_id = models.IntegerField(blank=True, null=True)
    sindico_id = models.IntegerField(blank=True, null=True)
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    solicitante = models.CharField(max_length=220, blank=True, null=True)
    cameras = models.CharField(max_length=220)
    periodo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    tipo_gravacao = models.IntegerField(db_comment='1 - Imagem, 2 - Audio')
    execucao = models.IntegerField(db_comment='1 - Presencial; 2 - Remoto')
    aprovacao = models.IntegerField()
    area_sindico = models.IntegerField(db_comment='0-n�o; 1-sim')
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imagemcameras'

    def __str__(self):
        return f"{self.condominio}"


class Informativos(models.Model):
    titulo = models.CharField(max_length=220)
    mensagem = models.TextField()
    imagem = models.CharField(max_length=255, blank=True, null=True)
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    log_quem_recebeu = models.TextField(blank=True, null=True)
    status_notification = models.IntegerField(blank=True, null=True)
    total_enviado = models.IntegerField(blank=True, null=True)
    total_recebido = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey('Users', on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'informativos'

    def __str__(self):
        return f"{self.condominio}"


class Internets(models.Model):
    nome_internet = models.CharField(max_length=220)
    empresa = models.CharField(max_length=220)
    telefone = models.CharField(max_length=45, blank=True, null=True)
    telefone2 = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=220, blank=True, null=True)
    website = models.CharField(max_length=220, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'internets'

    def __str__(self):
        return f"{self.empresa}"


class ItensCadastrados(models.Model):
    nome_item = models.CharField(max_length=220)
    valor_unitario = models.FloatField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itens_cadastrados'

    def __str__(self):
        return f"{self.nome_item}"


class ItensOrcamentos(models.Model):
    orcamento = models.ForeignKey('Orcamentos', on_delete=models.PROTECT, blank=True, null=True)
    itens_cadastrado = models.ForeignKey(ItensCadastrados, on_delete=models.PROTECT, blank=True, null=True)
    qtd_item = models.IntegerField()
    valor_unitario = models.FloatField()
    valor_total = models.FloatField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itens_orcamentos'

    def __str__(self):
        return f"{self.orcamento}"


class ItensVistorias(models.Model):
    nome_itens_vistoria = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itens_vistorias'

    def __str__(self):
        return f"{self.nome_itens_vistoria}"


class LiberacoesAcessos(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    nome_acesso = models.CharField(max_length=220, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    rg = models.CharField(max_length=45, blank=True, null=True)
    cpf = models.CharField(max_length=45, blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'liberacoes_acessos'

    def __str__(self):
        return f"{self.condominio}"


class LiberacoesChaves(models.Model):
    liberacoes_acesso = models.ForeignKey(LiberacoesAcessos, on_delete=models.PROTECT, blank=True, null=True)
    chave = models.CharField(max_length=45)
    qtd_max = models.IntegerField()
    qtd_usado = models.IntegerField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    hora_inicio = models.CharField(max_length=45)
    hora_fim = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'liberacoes_chaves'

    def __str__(self):
        return f"{self.liberacoes_acesso}"


class MateriaisAtividades(models.Model):
    atividade = models.ForeignKey(Atividades, on_delete=models.PROTECT, blank=True, null=True)
    nome_material = models.CharField(max_length=220)
    qtd = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materiais_atividades'

    def __str__(self):
        return f"{self.atividade}"


class MateriaisGrupos(models.Model):
    nome_grupo = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materiais_grupos'

    def __str__(self):
        return f"{self.nome_grupo}"


class MateriaisMarcas(models.Model):
    nome_marca = models.CharField(max_length=100)
    observacao_marca = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materiais_marcas'

    def __str__(self):
        return f"{self.nome_marca}"


class MateriaisObras(models.Model):
    obra = models.ForeignKey('Obras', on_delete=models.PROTECT, blank=True, null=True)
    nome_material = models.CharField(max_length=220)
    qtd = models.CharField(max_length=45)
    data_material = models.DateField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materiais_obras'

    def __str__(self):
        return f"{self.obra}"


class MateriaisProdutos(models.Model):
    materiais_grupo = models.ForeignKey(MateriaisGrupos, on_delete=models.PROTECT, blank=True, null=True)
    materiais_marca = models.ForeignKey(MateriaisMarcas, on_delete=models.PROTECT, blank=True, null=True)
    materiais_unidade = models.ForeignKey('MateriaisUnidades', on_delete=models.PROTECT, blank=True, null=True)
    materiais_tipo = models.IntegerField(blank=True, null=True)
    nome_produto = models.CharField(max_length=100)
    observacao_produto = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    custo = models.CharField(max_length=45)
    valor = models.CharField(max_length=45)
    listar_app = models.IntegerField(blank=True, null=True)
    implantacao = models.IntegerField(blank=True, null=True)
    max_desc = models.IntegerField(blank=True, null=True, db_comment='Maximo de desconto para este produto.')
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materiais_produtos'

    def __str__(self):
        return f"{self.nome_produto}"


class MateriaisUnidades(models.Model):
    nome_unidade = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materiais_unidades'

    def __str__(self):
        return f"{self.nome_unidade}"


class MudancasNormas(models.Model):
    nome_mudanca_normas = models.CharField(max_length=220)
    cor = models.CharField(max_length=20)
    icone = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mudancas_normas'

    def __str__(self):
        return f"{self.nome_mudanca_normas}"


class Notificacoes(models.Model):
    user = models.ForeignKey('Users', on_delete=models.PROTECT, blank=True, null=True)
    responsavel = models.ForeignKey('Users', models.DO_NOTHING, related_name='notificacoes_responsavel_set', blank=True, null=True)
    tipo = models.IntegerField()
    titulo = models.CharField(max_length=220)
    mensagem = models.TextField()
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notificacoes'

    def __str__(self):
        return f"{self.user}"


class Obras(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_final = models.DateField(blank=True, null=True)
    data_previsao = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obras'

    def __str__(self):
        return f"{self.condominio}"


class ObrasChecklistObras(models.Model):
    obra = models.ForeignKey(Obras, on_delete=models.PROTECT, blank=True, null=True)
    checklist_obra = models.ForeignKey(ChecklistObras, on_delete=models.PROTECT, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obras_checklist_obras'

    def __str__(self):
        return f"{self.obra}"


class Ocorrencias(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_solicitante = models.ForeignKey('TatticaFuncionarios', models.DO_NOTHING, related_name='ocorrencias_tattica_solicitante_set', blank=True, null=True)
    sindico = models.ForeignKey('Sindicos', on_delete=models.PROTECT, blank=True, null=True)
    departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT, blank=True, null=True)
    ocorrencia = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    solicitante = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField()
    observacao = models.TextField(blank=True, null=True)
    atividades_count = models.IntegerField()
    atividades_pendentes_count = models.IntegerField()
    criticidade = models.IntegerField(blank=True, null=True, db_comment='0 - Normal; 1 - Cr�tico;')
    relevancia = models.IntegerField(blank=True, null=True)
    area_sindico = models.IntegerField(db_comment='0-n�o; 1-sim')
    status = models.IntegerField(db_comment='0 - Deletado; 1 - Pendente; 2 - Resolvido; 3 - Duplicado')
    email_send = models.IntegerField(blank=True, null=True, db_comment='1 - N�o enviado; 2 - Enviado')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ocorrencias'

    def __str__(self):
        return f"{self.condominio}"


class Orcamentos(models.Model):
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    orcamento_nome = models.CharField(max_length=100, blank=True, null=True, db_comment='"ID" do or�amento')
    orcamento_tipo = models.IntegerField(blank=True, null=True)
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    comercial_lead = models.ForeignKey(ComercialLeads, on_delete=models.PROTECT, blank=True, null=True)
    ocorrencia = models.ForeignKey(Ocorrencias, on_delete=models.PROTECT, blank=True, null=True)
    empresa = models.CharField(max_length=45, blank=True, null=True)
    assunto = models.CharField(max_length=225, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    pdfurl = models.CharField(max_length=100, blank=True, null=True)
    desconto = models.IntegerField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    data_diagnostico = models.DateField(blank=True, null=True)
    status = models.IntegerField(db_comment='0 - Cria��o; 1 - Pendente; 2 - Aprovado; 3 - Cancelado; 4 - Concluido')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orcamentos'

    def __str__(self):
        return f"{self.condominio}"


class OrcamentosMateriais(models.Model):
    orcamento = models.ForeignKey(Orcamentos, on_delete=models.PROTECT, blank=True, null=True)
    materiais_produtos = models.ForeignKey(MateriaisProdutos, on_delete=models.PROTECT, blank=True, null=True)
    produtos_qtd = models.IntegerField(blank=True, null=True)
    valor = models.CharField(max_length=45, blank=True, null=True, db_comment='Valor em que foi vendido a unidade')
    desconto = models.CharField(max_length=45, blank=True, null=True)
    valor_custo = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orcamentos_materiais'

    def __str__(self):
        return f"{self.condominio}"


class OrcamentosPessoas(models.Model):
    orcamento = models.ForeignKey(Orcamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey('Pessoas', on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orcamentos_pessoas'

    def __str__(self):
        return f"{self.orcamento}"


class Ordemdeservicos(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    tattica_ajudante = models.ForeignKey('TatticaFuncionarios', models.DO_NOTHING, related_name='ordemdeservicos_tattica_ajudante_set', blank=True, null=True)
    hora_entrada = models.TimeField(blank=True, null=True)
    hora_saida = models.TimeField(blank=True, null=True)
    data_os = models.DateField(blank=True, null=True)
    possui_faturamento = models.IntegerField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ordemdeservicos'

    def __str__(self):
        return f"{self.condominio}"


class OrdemdeservicosMateriaisProdutos(models.Model):
    ordemdeservico = models.ForeignKey(Ordemdeservicos, on_delete=models.PROTECT, blank=True, null=True)
    materiais_produto = models.ForeignKey(MateriaisProdutos, on_delete=models.PROTECT, blank=True, null=True)
    qtde = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ordemdeservicos_materiais_produtos'

    def __str__(self):
        return f"{self.ordemdeservico}"


class Parcelas(models.Model):
    parcela = models.IntegerField()
    min_valor = models.TextField(db_comment='Valor minimo para aplicar parcela.')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parcelas'

    def __str__(self):
        return f"{self.parcela}"


class Patrimonios(models.Model):
    tipos_patrimonio = models.ForeignKey('TiposPatrimonios', on_delete=models.PROTECT, blank=True, null=True)
    departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT, blank=True, null=True)
    estados_equipamento = models.ForeignKey(EstadosEquipamentos, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    nome_patrimonio = models.CharField(max_length=220)
    modelo = models.CharField(max_length=220, blank=True, null=True)
    local = models.CharField(max_length=220, blank=True, null=True)
    data_compra = models.DateField(blank=True, null=True)
    valor_patrimonio = models.FloatField(blank=True, null=True)
    durabilidade = models.IntegerField(blank=True, null=True)
    depreciacao = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patrimonios'

    def __str__(self):
        return f"{self.nome_patrimonio}"


class Pedagios(models.Model):
    tipos_pedagio = models.ForeignKey('TiposPedagios', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    tipos_veiculo = models.ForeignKey('TiposVeiculos', on_delete=models.PROTECT, blank=True, null=True)
    data_pedagio = models.DateField()
    qtd = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedagios'

    def __str__(self):
        return f"{self.tipos_pedagio}"


class PermissaoAcessos(models.Model):
    tipos_acesso = models.ForeignKey('TiposAcessos', on_delete=models.PROTECT, blank=True, null=True)
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    empresas_servicos_empresa = models.ForeignKey(EmpresasServicosEmpresas, on_delete=models.PROTECT, blank=True, null=True)
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.PROTECT, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    domingo = models.IntegerField()
    segunda = models.IntegerField()
    terca = models.IntegerField()
    quarta = models.IntegerField()
    quinta = models.IntegerField()
    sexta = models.IntegerField()
    sabado = models.IntegerField()
    acesso_livre = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissao_acessos'

    def __str__(self):
        return f"{self.apartamento}"


class PermissaoAcessosDispositivosRoles(models.Model):
    permissao_acesso = models.ForeignKey(PermissaoAcessos, on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_role = models.ForeignKey(DispositivosRoles, on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissao_acessos_dispositivos_roles'

    def __str__(self):
        return f"{self.permissao_acesso}"


class Pessoas(models.Model):
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    tipos_pessoa = models.ForeignKey('TiposPessoas', on_delete=models.PROTECT, blank=True, null=True)
    criticidade = models.ForeignKey(Criticidades, on_delete=models.PROTECT, blank=True, null=True)
    tipos_classificacao = models.ForeignKey('TiposClassificacaos', on_delete=models.PROTECT, blank=True, null=True)
    responsavel = models.IntegerField(db_comment='1 - Sim, 2 - N�o')
    nome_pessoa = models.CharField(max_length=220, blank=True, null=True)
    imagem_pessoa = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=1)
    cpf = models.CharField(max_length=45, blank=True, null=True)
    rg = models.CharField(max_length=45, blank=True, null=True)
    data_aniversario = models.DateField(blank=True, null=True)
    parentesco = models.CharField(max_length=220, blank=True, null=True)
    observacao = models.CharField(max_length=220, blank=True, null=True)
    celular = models.CharField(max_length=45, blank=True, null=True)
    celular_2 = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=220, blank=True, null=True)
    profissao = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pessoas'

    def __str__(self):
        return f"{self.nome_pessoa}"


class PessoasDispositivosRoles(models.Model):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.PROTECT, blank=True, null=True)
    dispositivos_role = models.ForeignKey(DispositivosRoles, on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pessoas_dispositivos_roles'

    def __str__(self):
        return f"{self.pessoa}"


class Pets(models.Model):
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    raca = models.ForeignKey('Racas', on_delete=models.PROTECT, blank=True, null=True)
    nome_pet = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pets'

    def __str__(self):
        return f"{self.apartamento}"


class Pgms(models.Model):
    centrais_jfl = models.ForeignKey(CentraisJfls, on_delete=models.PROTECT, blank=True, null=True)
    nome_pgm = models.CharField(max_length=45)
    nome_exibicao = models.CharField(max_length=60, blank=True, null=True)
    codigo = models.IntegerField()
    visivel_morador = models.IntegerField()
    visivel_visitante = models.IntegerField()
    visivel_sindico = models.IntegerField(blank=True, null=True)
    retencao = models.IntegerField()
    bloqueio = models.IntegerField(blank=True, null=True)
    reserva = models.IntegerField(blank=True, null=True)
    codigo_camera = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pgms'

    def __str__(self):
        return f"{self.nome_pgm}"


class PlantaoOcorrencias(models.Model):
    plantao_operacional = models.ForeignKey('PlantaoOperacionals', on_delete=models.PROTECT, blank=True, null=True)
    ocorrencia = models.TextField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plantao_ocorrencias'

    def __str__(self):
        return f"{self.ocorrencia}"


class PlantaoOperacionals(models.Model):
    supervisor1 = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    supervisor2 = models.ForeignKey('TatticaFuncionarios', models.DO_NOTHING, related_name='plantaooperacionals_supervisor2_set', blank=True, null=True)
    unidade = models.ForeignKey('Unidades', on_delete=models.PROTECT, blank=True, null=True)
    data_abertura = models.DateField()
    data_fechamento = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plantao_operacionals'

    def __str__(self):
        return f"{self.unidade}"


class Portas(models.Model):
    porta_nome = models.CharField(max_length=55)
    cond = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    senha_dispositivo = models.ForeignKey(DispositivosModelos, on_delete=models.PROTECT, blank=True, null=True)
    tag_dispositivo = models.ForeignKey(DispositivosModelos, models.DO_NOTHING, related_name='portas_tag_dispositivo_set', blank=True, null=True)
    bio_dispositivo = models.ForeignKey(DispositivosModelos, models.DO_NOTHING, related_name='portas_bio_dispositivo_set', blank=True, null=True)
    ctrlgar_dispositivo = models.ForeignKey(DispositivosModelos, models.DO_NOTHING, related_name='portas_ctrlgar_dispositivo_set', blank=True, null=True)
    a1 = models.CharField(max_length=45, blank=True, null=True)
    a2 = models.CharField(max_length=45, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'portas'

    def __str__(self):
        return f"{self.porta_nome}"


class PrestadoresAcessos(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    empresas_servicos_empresa = models.ForeignKey(EmpresasServicosEmpresas, on_delete=models.PROTECT, blank=True, null=True)
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prestadores_acessos'

    def __str__(self):
        return f"{self.condominio}"


class PrestadoresNormas(models.Model):
    nome_prestador_normas = models.CharField(max_length=220)
    cor = models.CharField(max_length=20, blank=True, null=True)
    icone = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prestadores_normas'

    def __str__(self):
        return f"{self.nome_prestador_normas}"


class Projetos(models.Model):
    tipos_projeto = models.ForeignKey('TiposProjetos', on_delete=models.PROTECT, blank=True, null=True)
    departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    nome_projeto = models.CharField(max_length=45)
    descricao = models.TextField()
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    data_previsao = models.DateField(blank=True, null=True)
    tarefas_count = models.IntegerField()
    tarefas_pendentes_count = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projetos'

    def __str__(self):
        return f"{self.nome_projeto}"


class Qths(models.Model):
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    data_visita = models.DateTimeField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qths'

    def __str__(self):
        return f"{self.tattica_funcionario}"


class QthsTarefas(models.Model):
    nome_tarefa = models.CharField(max_length=100)
    ordem = models.IntegerField()
    icon = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qths_tarefas'

    def __str__(self):
        return f"{self.nome_tarefa}"


class QthsTarefasQths(models.Model):
    qth = models.ForeignKey(Qths, on_delete=models.PROTECT, blank=True, null=True)
    qths_tarefa = models.ForeignKey(QthsTarefas, on_delete=models.PROTECT, blank=True, null=True)
    resposta_tarefa = models.IntegerField(db_comment='0 - sem, 1 - ok e 2 - n�o')
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qths_tarefas_qths'

    def __str__(self):
        return f"{self.qths_tarefa}"


class Questionarios(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.PROTECT, blank=True, null=True)
    nome_pessoa = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    pergunta1 = models.IntegerField(blank=True, null=True)
    pergunta2 = models.IntegerField(blank=True, null=True)
    pergunta3 = models.IntegerField(blank=True, null=True)
    pergunta4 = models.IntegerField(blank=True, null=True)
    pergunta5 = models.IntegerField(blank=True, null=True)
    pergunta6 = models.IntegerField(blank=True, null=True)
    pergunta7 = models.IntegerField(blank=True, null=True)
    sugestao = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionarios'

    def __str__(self):
        return f"{self.nome_pessoa}"


class Racas(models.Model):
    tipos_raca = models.ForeignKey('TiposRacas', on_delete=models.PROTECT, blank=True, null=True)
    nome_raca = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'racas'

    def __str__(self):
        return f"{self.nome_raca}"


class Recados(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    nome_recado = models.CharField(max_length=220, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    class Meta:
        managed = False
        db_table = 'recados'

    def __str__(self):
        return f"{self.nome_recado}"


class ReconhecidoFacials(models.Model):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.PROTECT, blank=True, null=True)
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    cam_facial = models.ForeignKey(CamFacials, on_delete=models.PROTECT, blank=True, null=True)
    foto_face = models.CharField(max_length=255)
    data_reconhecimento = models.DateTimeField()
    dataset_pasta = models.CharField(max_length=255)
    abriu_porta = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reconhecido_facials'

    def __str__(self):
        return f"{self.pessoa}"


class ReservasNormas(models.Model):
    nome_reserva_normas = models.CharField(max_length=220)
    cor = models.CharField(max_length=20, blank=True, null=True)
    icone = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservas_normas'

    def __str__(self):
        return f"{self.nome_reserva_normas}"


class Roles(models.Model):
    nome_role = models.CharField(max_length=220)
    identificador = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'

    def __str__(self):
        return f"{self.identificador}"


class Sindicos(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.PROTECT, blank=True, null=True)
    tipos_sindico = models.ForeignKey('TiposSindicos', on_delete=models.PROTECT, blank=True, null=True)
    email_sindico = models.CharField(max_length=200, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    email_permissao = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sindicos'

    def __str__(self):
        return f"{self.pessoa}"


class Subramais(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    numero = models.CharField(max_length=45)
    local = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subramais'

    def __str__(self):
        return f"{self.numero}"


class SubtiposOcorrencias(models.Model):
    nome_subtipos_ocorrencia = models.CharField(max_length=220)
    tipos_ocorrencia = models.ForeignKey('TiposOcorrencias', on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subtipos_ocorrencias'

    def __str__(self):
        return f"{self.nome_subtipos_ocorrencia}"


class SubtiposOcorrenciasOcorrencias(models.Model):
    ocorrencia = models.ForeignKey(Ocorrencias, on_delete=models.PROTECT, blank=True, null=True)
    subtipos_ocorrencia = models.ForeignKey(SubtiposOcorrencias, on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subtipos_ocorrencias_ocorrencias'

    def __str__(self):
        return f"{self.subtipos_ocorrencia}"


class SubtiposTiposAbastecimentos(models.Model):
    nome_subtipo = models.CharField(max_length=100)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subtipos_tipos_abastecimentos'

    def __str__(self):
        return f"{self.nome_subtipo}"


class Suporteunidades(models.Model):
    nome_suporteunidade = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suporteunidades'

    def __str__(self):
        return f"{self.nome_suporteunidade}"


class Tarefas(models.Model):
    tipos_tarefa = models.ForeignKey('TiposTarefas', on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey('TatticaFuncionarios', on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.ForeignKey(Projetos, on_delete=models.PROTECT, blank=True, null=True)
    descricao = models.TextField()
    observacao = models.TextField(blank=True, null=True)
    resolucao = models.TextField(blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    data_previsao = models.DateField(blank=True, null=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarefas'

    def __str__(self):
        return f"{self.tipos_tarefa}"


class TatticaFuncionarios(models.Model):
    departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT, blank=True, null=True)
    imagem_funcionario = models.CharField(max_length=45, blank=True, null=True)
    nome_funcionario = models.CharField(max_length=220)
    apelido = models.CharField(max_length=200, blank=True, null=True)
    cargo = models.CharField(max_length=45, blank=True, null=True)
    rg = models.CharField(max_length=45, blank=True, null=True)
    cpf = models.CharField(max_length=45, blank=True, null=True)
    carteira_trabalho = models.CharField(max_length=45, blank=True, null=True)
    logradouro = models.CharField(max_length=220, blank=True, null=True)
    numero = models.CharField(max_length=45, blank=True, null=True)
    complemento = models.CharField(max_length=220, blank=True, null=True)
    bairro = models.CharField(max_length=220, blank=True, null=True)
    cidade = models.CharField(max_length=220, blank=True, null=True)
    uf = models.CharField(max_length=10, blank=True, null=True)
    cep = models.CharField(max_length=45, blank=True, null=True)
    telefone = models.CharField(max_length=45, blank=True, null=True)
    celular = models.CharField(max_length=45, blank=True, null=True)
    hora_inicio = models.CharField(max_length=20, blank=True, null=True)
    hora_fim = models.CharField(max_length=20, blank=True, null=True)
    data_adimissao = models.DateField(blank=True, null=True)
    data_demissao = models.DateField(blank=True, null=True)
    telefone_contato = models.CharField(max_length=45, blank=True, null=True)
    plano_saude = models.CharField(max_length=220, blank=True, null=True)
    tipo_sangue = models.CharField(max_length=45, blank=True, null=True)
    escala = models.CharField(max_length=220, blank=True, null=True)
    cnh = models.CharField(max_length=45, blank=True, null=True)
    cnh_data = models.DateField(blank=True, null=True)
    cnh_tipo = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tattica_funcionarios'

    def __str__(self):
        return f"{self.nome_funcionario}"


class TatticaTelefones(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT, blank=True, null=True)
    telefone = models.CharField(max_length=45)
    marca = models.CharField(max_length=45, blank=True, null=True)
    serie = models.CharField(max_length=45, blank=True, null=True)
    imei1 = models.CharField(max_length=45, blank=True, null=True)
    imei2 = models.CharField(max_length=45, blank=True, null=True)
    acessorios = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tattica_telefones'

    def __str__(self):
        return f"{self.telefone}"


class TatticaVeiculos(models.Model):
    tipos_veiculo = models.ForeignKey('TiposVeiculos', on_delete=models.PROTECT, blank=True, null=True)
    marca = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45)
    placa = models.CharField(max_length=45)
    chassi = models.CharField(max_length=45, blank=True, null=True)
    data_compra = models.DateField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    cor = models.CharField(max_length=45)
    ano = models.CharField(max_length=45)
    proprietario = models.IntegerField(db_comment='1 - veiculo da tattica\n2 - externo')
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tattica_veiculos'

    def __str__(self):
        return f"{self.tipos_veiculo}"


class TiposAbastecimentos(models.Model):
    nome_abastecimentos = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    subtipos_tipos_abastecimentos = models.ForeignKey(SubtiposTiposAbastecimentos, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_abastecimentos'

    def __str__(self):
        return f"{self.nome_abastecimentos}"


class TiposAcessos(models.Model):
    nome_tipos_acesso = models.CharField(max_length=220, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_acessos'

    def __str__(self):
        return f"{self.nome_tipos_acesso}"


class TiposClassificacaos(models.Model):
    nome_classificacao = models.CharField(max_length=45)
    texto_classificacao = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_classificacaos'

    def __str__(self):
        return f"{self.nome_classificacao}"


class TiposCondominiosFuncionarios(models.Model):
    nome_tipo_funcionario = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_condominios_funcionarios'

    def __str__(self):
        return f"{self.nome_tipo_funcionario}"


class TiposControlesAcessos(models.Model):
    nome_tipos_controles_acesso = models.CharField(max_length=220)
    visivel_morador = models.IntegerField(blank=True, null=True)
    valor = models.CharField(max_length=45, blank=True, null=True)
    link_pagamento = models.CharField(max_length=255, blank=True, null=True)
    valor_promo = models.CharField(max_length=45, blank=True, null=True)
    link_promo = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_controles_acessos'

    def __str__(self):
        return f"{self.nome_tipos_controles_acesso}"


class TiposElevadorChamados(models.Model):
    nome_tipo_chamado = models.CharField(max_length=150)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_elevador_chamados'

    def __str__(self):
        return f"{self.nome_tipo_chamado}"


class TiposEncomendas(models.Model):
    nome_tipos_encomenda = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_encomendas'

    def __str__(self):
        return f"{self.nome_tipos_encomenda}"


class TiposEquipamentos(models.Model):
    nome_tipos_condequipamento = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_equipamentos'

    def __str__(self):
        return f"{self.nome_tipos_condequipamento}"


class TiposEventos(models.Model):
    grupos_evento = models.ForeignKey(GruposEventos, on_delete=models.PROTECT, blank=True, null=True)
    nome_tipo_evento = models.CharField(max_length=75)
    codigo_tipo_evento = models.CharField(max_length=4)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_eventos'

    def __str__(self):
        return f"{self.nome_tipo_evento}"


class TiposEventosTratados(models.Model):
    nome_tipo_evento_tratado = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_eventos_tratados'

    def __str__(self):
        return f"{self.nome_tipo_evento_tratado}"


class TiposFotos(models.Model):
    nome_tipos_foto = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_fotos'

    def __str__(self):
        return f"{self.nome_tipos_foto}"


class TiposFuncionarios(models.Model):
    nome_tipos_funcionario = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_funcionarios'

    def __str__(self):
        return f"{self.nome_tipos_funcionario}"


class TiposOcorrencias(models.Model):
    nome_tipos_ocorrencia = models.CharField(max_length=220)
    departamento_id = models.IntegerField(blank=True, null=True)
    visivel_app = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_ocorrencias'

    def __str__(self):
        return f"{self.nome_tipos_ocorrencia}"


class TiposOcorrenciasOcorrencias(models.Model):
    ocorrencia = models.ForeignKey(Ocorrencias, on_delete=models.PROTECT, blank=True, null=True)
    tipos_ocorrencia = models.ForeignKey(TiposOcorrencias, on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_ocorrencias_ocorrencias'

    def __str__(self):
        return f"{self.ocorrencia}"


class TiposPagamentos(models.Model):
    nome_tipos_pagamento = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_pagamentos'

    def __str__(self):
        return f"{self.nome_tipos_pagamento}"


class TiposPatrimonios(models.Model):
    nome_tipos_patrimonio = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_patrimonios'

    def __str__(self):
        return f"{self.nome_tipos_patrimonio}"


class TiposPedagios(models.Model):
    nome_tipos_pedagio = models.CharField(max_length=45)
    valor = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_pedagios'

    def __str__(self):
        return f"{self.nome_tipos_pedagio}"


class TiposPessoas(models.Model):
    nome_tipos_pessoa = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_pessoas'

    def __str__(self):
        return f"{self.nome_tipos_pessoa}"


class TiposProjetos(models.Model):
    nome_tipo_projeto = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_projetos'

    def __str__(self):
        return f"{self.nome_tipo_projeto}"


class TiposRacas(models.Model):
    nome_tipos_raca = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_racas'

    def __str__(self):
        return f"{self.nome_tipos_raca}"


class TiposSindicos(models.Model):
    nome_tipos_sindico = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_sindicos'

    def __str__(self):
        return f"{self.nome_tipos_sindico}"


class TiposTarefas(models.Model):
    tipos_projeto = models.ForeignKey(TiposProjetos, on_delete=models.PROTECT, blank=True, null=True)
    tipo_tarefa_nome = models.CharField(max_length=45)
    etapa = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_tarefas'

    def __str__(self):
        return f"{self.tipo_tarefa_nome}"


class TiposVeiculos(models.Model):
    nome_tipos_veiculo = models.CharField(max_length=220)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_veiculos'

    def __str__(self):
        return f"{self.nome_tipos_veiculo}"


class TiposZonas(models.Model):
    codigo_tipo_zona = models.CharField(max_length=2)
    nome_tipo_zona = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_zonas'

    def __str__(self):
        return f"{self.nome_tipo_zona}"''


class Tips(models.Model):
    unidade = models.ForeignKey('Unidades', on_delete=models.PROTECT, blank=True, null=True)
    nome_tip = models.CharField(max_length=100)
    ptah_user = models.CharField(max_length=50)
    ip_tip = models.CharField(max_length=50)
    ramal_ptah = models.CharField(max_length=45)
    endpoint = models.CharField(max_length=45)
    mac = models.CharField(max_length=45)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tips'

    def __str__(self):
        return f"{self.nome_tip}"


class TipsTatticaFuncionarios(models.Model):
    tip = models.ForeignKey(Tips, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey(TatticaFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    data_logout = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tips_tattica_funcionarios'

    def __str__(self):
        return f"{self.tattica_funcionario}"


class Unidades(models.Model):
    nome_unidade = models.CharField(max_length=100)
    status = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unidades'

    def __str__(self):
        return f"{self.nome_unidade}"


class Users(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, blank=True, null=True)
    unidade = models.ForeignKey(Unidades, on_delete=models.PROTECT, blank=True, null=True)
    suporteunidade = models.ForeignKey(Suporteunidades, on_delete=models.PROTECT, blank=True, null=True)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario_id = models.IntegerField(blank=True, null=True)
    condominios_funcionario = models.ForeignKey(CondominiosFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=255)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    notificacao_ronda = models.IntegerField(blank=True, null=True)
    token_gos = models.CharField(max_length=255, blank=True, null=True)
    acessos = models.IntegerField(blank=True, null=True)
    data_acesso = models.DateTimeField(blank=True, null=True)
    check_lgpd = models.IntegerField(blank=True, null=True)
    permissao_os = models.IntegerField()
    permissao_pgm = models.IntegerField()
    permissao_qth = models.IntegerField()
    permissao_historico = models.IntegerField()
    permissao_ca = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return f"{self.username}"


class Vagas(models.Model):
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    numero = models.CharField(max_length=45)
    andar = models.CharField(max_length=45)
    descricao = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vagas'

    def __str__(self):
        return f"{self.apartamento}"


class Veiculos(models.Model):
    apartamento = models.ForeignKey(Apartamentos, on_delete=models.PROTECT, blank=True, null=True)
    tipos_veiculo = models.ForeignKey(TiposVeiculos, on_delete=models.PROTECT, blank=True, null=True)
    marca = models.CharField(max_length=220)
    modelo = models.CharField(max_length=220, blank=True, null=True)
    cor = models.CharField(max_length=45, blank=True, null=True)
    placa = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'veiculos'

    def __str__(self):
        return f"{self.tipos_veiculo}"


class Vistorias(models.Model):
    condominio = models.ForeignKey(Condominios, on_delete=models.PROTECT, blank=True, null=True)
    tattica_funcionario = models.ForeignKey(TatticaFuncionarios, on_delete=models.PROTECT, blank=True, null=True)
    relato = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vistorias'

    def __str__(self):
        return f"{self.condominio}"


class VistoriasItensVistorias(models.Model):
    vistoria = models.ForeignKey(Vistorias, on_delete=models.PROTECT, blank=True, null=True)
    itens_vistoria = models.ForeignKey(ItensVistorias, on_delete=models.PROTECT, blank=True, null=True)
    ordem = models.IntegerField()
    descricao = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vistorias_itens_vistorias'

    def __str__(self):
        return f"{self.vistoria}"


class Zonas(models.Model):
    centrais_jfl = models.ForeignKey(CentraisJfls, on_delete=models.PROTECT, blank=True, null=True)
    tipos_zona = models.ForeignKey(TiposZonas, on_delete=models.PROTECT, blank=True, null=True)
    grupos_zona = models.ForeignKey(GruposZonas, on_delete=models.PROTECT, blank=True, null=True)
    nome_zona = models.CharField(max_length=45)
    codigo_zona = models.CharField(max_length=2)
    particao_a = models.IntegerField()
    particao_b = models.IntegerField()
    particao_c = models.IntegerField()
    particao_d = models.IntegerField()
    stay = models.IntegerField()
    inteligente = models.IntegerField()
    silenciosa = models.IntegerField()
    autoanulavel = models.IntegerField()
    permitir_inibir = models.IntegerField()
    sirene_intermitente = models.IntegerField()
    chime = models.IntegerField()
    code = models.IntegerField()
    status = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zonas'

    def __str__(self):
        return f"{self.nome_zona}"
