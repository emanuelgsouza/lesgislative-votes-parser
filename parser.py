import pandas as pd
import logging
from constants import INPUT_PATH, PARTIDO_MUNZONA, FORMAT_FILE, STATES, CANDIDATO_MUNZONA
from helpers import flat_lists


def factory_partido(
    ano_eleicao,
    descricao_ue,
    sigla_uf,
    nome_partido,
    numero_partido,
    sigla_partido,
    nome_legenda,
    composicao_legenda,
    tipo_agremiacao,    
    total_votos,
    total_legenda
):
    return {
        'ano_eleicao': ano_eleicao,
        'descricao_ue': descricao_ue,
        'sigla_uf': sigla_uf,
        'nome_partido': nome_partido,
        'numero_partido': numero_partido,
        'sigla_partido': sigla_partido,
        'nome_legenda': nome_legenda,
        'composicao_legenda': composicao_legenda,
        'tipo_agremiacao': tipo_agremiacao,    
        'total_votos': total_votos,
        'total_legenda': total_legenda
    }


def factory_deputado(
    ano_eleicao,
    nome,
    nome_urna,
    numero_urna,
    descricao_ue,
    sigla_uf,
    tipo_agremiacao,
    nome_partido,
    numero_partido,
    sigla_partido,
    nome_legenda,
    composicao_legenda,
    descricao_totalizacao_turno,
    total_votos,
    descricao_detalhe_situacao_candidatura,
    descricao_situacao_candidatura
):
    return {
        'ano_eleicao': ano_eleicao,
        'nome': nome,
        'nome_urna': nome_urna,
        'numero_urna': numero_urna,
        'descricao_ue': descricao_ue,
        'sigla_uf': sigla_uf,
        'tipo_agremiacao': tipo_agremiacao,
        'nome_partido': nome_partido,
        'numero_partido': numero_partido,
        'sigla_partido': sigla_partido,
        'nome_legenda': nome_legenda,
        'composicao_legenda': composicao_legenda,
        'descricao_totalizacao_turno': descricao_totalizacao_turno,
        'total_votos': total_votos,
        'descricao_detalhe_situacao_candidatura': descricao_detalhe_situacao_candidatura,
        'descricao_situacao_candidatura': descricao_situacao_candidatura 
    }


def generate_party_data():
    df = pd.read_csv(f'{INPUT_PATH}/{PARTIDO_MUNZONA}{FORMAT_FILE}')

    processed = []

    for state in STATES:
        dfl = df[(df['sigla_uf'] == state) & (df['codigo_cargo'] == 6)]
        logging.info(f'Processando dados para o {state}')

        partidos_grouped_by_vote = dfl[['nome_partido', 'total_votos']].groupby(by='nome_partido').sum()
        legenda_grouped_by_vote = dfl[['nome_partido', 'voto_em_legenda']].groupby(by='nome_partido').sum()

        items = dict()

        for row in dfl.itertuples():
            if row.nome_partido in items:
                continue

            if row.codigo_cargo != 6:
                # se trata de um cargo que não é o deputado federal
                continue

            items[row.nome_partido] = factory_partido(
                ano_eleicao=row.ano_eleicao,
                nome_partido=row.nome_partido,
                numero_partido=row.numero_partido,
                sigla_partido=row.sigla_partido,
                nome_legenda=row.nome_legenda,
                composicao_legenda=row.composicao_legenda,
                descricao_ue=row.descricao_ue,
                sigla_uf=row.sigla_uf,
                tipo_agremiacao=row.tipo_agremiacao,
                total_votos=partidos_grouped_by_vote.loc[row.nome_partido].values.item(),
                total_legenda=legenda_grouped_by_vote.loc[row.nome_partido].values.item(),
            )

        processed.append(list(items.values()))
    
    return flat_lists(lists=processed)

def generate_candidate_data():
    df = pd.read_csv(f'{INPUT_PATH}/{CANDIDATO_MUNZONA}{FORMAT_FILE}')

    candidates_grouped_by_vote = df[['numero_sequencial', 'total_votos']].groupby(by='numero_sequencial').sum()

    processed = []

    for state in STATES:
        dfl = df[df['sigla_uf'] == state]
        logging.info(f'Processando dados para o {state}')

        items = dict()

        for row in dfl.itertuples():
            if row.nome_urna in items:
                continue

            if row.codigo_cargo != 6:
                # se trata de um cargo que não é o deputado federal
                continue

            items[row.nome_urna] = factory_deputado(
                ano_eleicao=row.ano_eleicao,
                nome=row.nome,
                nome_urna=row.nome_urna,
                numero_urna=row.numero_urna,
                descricao_ue=row.descricao_ue,
                sigla_uf=row.sigla_uf,
                tipo_agremiacao=row.tipo_agremiacao,
                nome_partido=row.nome_partido,
                numero_partido=row.numero_partido,
                sigla_partido=row.sigla_partido,
                nome_legenda=row.nome_legenda,
                composicao_legenda=row.composicao_legenda,
                descricao_totalizacao_turno=row.descricao_totalizacao_turno,
                descricao_detalhe_situacao_candidatura=row.descricao_detalhe_situacao_candidatura,
                descricao_situacao_candidatura=row.descricao_situacao_candidatura,
                total_votos=candidates_grouped_by_vote.loc[row.numero_sequencial].values.item()
            )

        processed.append(list(items.values()))
    
    return flat_lists(lists=processed)
