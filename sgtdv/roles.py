from rolepermissions.roles import AbstractUserRole

class ACS(AbstractUserRole):
    available_permissions={'cadastrar_cidadao':True,'Editar_cidadao':True, 'buscar_cidadao':True,'detail_cidadao':True}

class Coordenador(AbstractUserRole):
    available_permissions={'cadastrar_profissional':True,'editar_profissional':True, 'buscar_profissional':True,'detail_profissional':True,\
                           'cadastrar_estabelecimento':True,'editar_estabelecimento':True,'detail_estabelecimento':True,'listar_estabelecimento':True,\
                            'emissao_relatorios':True,'cadastrar_usuario':True,'edital_usuario':True,'listar_usuario':True,'detail_usuario':True}
    
class Digitador(AbstractUserRole):
    available_permissions={'cadastrar_diaria':True,'editar_diaria':True, 'buscar_diaria':True,'detail_diaria':True,\
                           'cadastrar_profissional':True,'editar_profissional':True, 'buscar_profissional':True,'detail_profissional':True,\
                           'cadastrar_reembolso':True,'editar_reembolso':True,\
                           'detail_reembolso':True,'buscar_reembolso':True,
        }

class Recepcao(AbstractUserRole):
    available_permissions={'cadastrar_cidadao':True,'editar_cidadao':True, 'buscar_cidadao':True,'detail_cidadao':True,\
                           'cadastrar_paciente_especialiade':True,'editar_paciente_especialiade':True,'detail_paciente_especialiade':True,\
                            'buscar_paciente_especialiade':True,'cadastrar_registro_transporte':True,'editar_registro_transporte':True,\
                             'detail_registro_transporte':True, 'buscar_registro_transporte':True, 'cadastrar_viagem':True,'editar_viagem':True\
                                ,'detail_viagem':True,'buscar_viagem':True,'search-paciente-especialidade':True,}
    
class Regulacao(AbstractUserRole):
     available_permissions={'cadastrar_recibo_tfd':True,'editar_recibo_tfd':True, 'buscar_recibo_tfd':True,\
                           'buscar_cidadao':True,'cadastrar_recibo_passagem':True,'editar_recibo_passagem':True,'buscar_recibo_tfd':True,\
                            'cadastrar_especialidade':True,'editar_especialidade':True,'listar_especialidade':True,\
                            'detail_especialidade':True,'buscar_especialidade':True,'emissao_relatorios':True,'search-paciente-especialidade':True,}
     
class Secretario(AbstractUserRole):
     available_permissions={'emissão de relatórios':True}