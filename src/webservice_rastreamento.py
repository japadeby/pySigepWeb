# -*- coding: utf-8 -*-
from usuario import Usuario
import urllib


class WebserviceRastreamento(object):
    _URL = 'http://websro.correios.com.br/sro_bin/sroii_xml.eventos'

    TIPO_LISTA_ETIQUETAS = 1
    TIPO_INTERVALO_ETIQUETAS = 2

    RETORNAR_TODOS_EVENTOS = 3
    RETORNAR_ULTIMO_EVENTO = 4

    _constantes = {
        TIPO_LISTA_ETIQUETAS: 'L',
        TIPO_INTERVALO_ETIQUETAS: 'F',
        RETORNAR_TODOS_EVENTOS: 'T',
        RETORNAR_ULTIMO_EVENTO: 'U',
    }

    def __init__(self, obj_usuario):
        if not isinstance(obj_usuario, Usuario):
            raise TypeError

        self.obj_usuario = obj_usuario

    def rastrea_objetos(self, tipo, resultado, lista_etiquetas):

        etiquetas = ''
        for etq in lista_etiquetas:
            etiquetas += etq.etiqueta_com_dig_verif

        params = {"Usuario": self.obj_usuario.nome,
                  "Senha": self.obj_usuario.senha,
                  'Tipo': WebserviceRastreamento._constantes[tipo],
                  'Resultado': WebserviceRastreamento._constantes[resultado],
                  'Objetos': etiquetas,
                  }

        query = urllib.urlencode(params)
        f = urllib.urlopen(WebserviceRastreamento._URL, query)
        contents = f.read()
        f.close()


