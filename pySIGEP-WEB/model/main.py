# -*- coding: utf-8 -*-
from servico_atende_cliente import ServicoAtendeCliente
from usuario import Usuario
from tag_plp import TagPLP
from tag_remetente import TagRemetente
from tag_dimensao_objeto import *
from tag_objeto_postal import *
from tag_correios_log import TagCorreiosLog
from diretoria import Diretoria
from endereco import Endereco


def main():
    print 'Iniciando'
    usr = Usuario('sigep', 'n5f9t8', '34028316000103', '08082650',
                  '9912208555', '0057018901')

    print usr.nome
    print usr.num_cartao_postagem

    l = [ServicoPostagem.SERVICO_CARTA_COMERCIAL_A_FATURAR,
         ServicoPostagem.SERVICO_PAC_41068]

    sv = ServicoAtendeCliente(ServicoAtendeCliente.AMBIENTE_HOMOLOGACAO, usr)

    print sv.verifica_disponibilidade_servicos(l, '70002900', '74000100')
    print sv.consulta_cep('70002900').bairro
    print sv.consulta_status_cartao_postagem()

    sv_postagem = ServicoPostagem(ServicoPostagem.SERVICO_PAC_41068)
    etiquetas = sv.solicita_etiquetas(sv_postagem.servico_postagem_id,
                                      qtd_etiquetas=3)

    # etiquetas[0].etiqueta_sem_dig_verif = 'EC21325855 BR'
    # etiquetas[1].etiqueta_sem_dig_verif = 'EC21325856 BR'
    # etiquetas[2].etiqueta_sem_dig_verif = 'EC21325857 BR'

    digitos = sv.gera_digito_verificador_etiquetas(
        etiquetas, gerador=ServicoAtendeCliente.GERADOR_OFFLINE)

    for i in range(len(etiquetas)):
        print etiquetas[i].etiqueta_sem_dig_verif
        print digitos[i]

    remetente_endereco = Endereco(logradouro='Avenida Central', numero=2370,
                                  bairro='Centro', cep='70002900',
                                  cidade='Brasilia', uf=Endereco.UF_PARANA,
                                  complemento=u'sala 1205,12° andar')

    destinatario_endereco = Endereco(logradouro='Avenida Central',
                                     numero=1065, bairro='Setor Industrial',
                                     cidade='Goiânia', uf=Endereco.UF_GOIAS,
                                     cep=74000100, complemento='Qd:102 A Lt:04')

    # Montando xml do plp
    obj_tag_plp = TagPLP(usr.num_cartao_postagem)
    obj_remetente = TagRemetente(usr.nome, usr.num_contrato, usr.codigo_admin,
                                 remetente_endereco,
                                 Diretoria(Diretoria.DIRETORIA_DR_PARANA),
                                 telefone=6112345008, email='cli@mail.com.br')

    obj_destinatario = TagDestinatario('Destino Ltda', destinatario_endereco,
                                       telefone=6212349644)

    obj_nacional = TagNacional(endereco=destinatario_endereco,
                               numero_nfe=102030, valor_a_cobrar=0.0)

    obj_servico_adtagemicional = TagServicoAdicional(99.00)
    obj_servico_adicional.add_tipo_servico_adicional(
        TagServicoAdicional.TIPO_AVISO_RECEBIMENTO)
    obj_servico_adicional.add_tipo_servico_adicional(
        TagServicoAdicional.TIPO_VALOR_DECLARADO)

    obj_dimensao_objeto = TagDimensaoObjeto(Caixa(20, 30, 38))

    obj_postal = TagObjetoPostal(obj_destinatario=obj_destinatario,
                                 obj_nacional=obj_nacional,
                                 obj_dimensao_objeto=obj_dimensao_objeto,
                                 obj_servico_adicional=obj_servico_adicional,
                                 obj_servico_postagem=sv_postagem,
                                 ob_etiqueta=etiquetas[0],
                                 peso=200, status_processamento=0)

    obj_correios_log = TagCorreiosLog('2.3', obj_tag_plp, obj_remetente,
                                      [obj_postal])

    print ServicoAtendeCliente.fecha_plp_varios_servicos(
        obj_correios_log.get_xml(), 123, etiquetas)

if __name__ == '__main__':
    main()

