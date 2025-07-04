import os
import logging


def validate_env_variable(env_var_name):
    value = os.environ.get(env_var_name)
    if value is None:
        raise ValueError(f'{env_var_name} não encontrada no arquivo .env')
    return value


def safe_invoke(retriever, question):
    try:
        return retriever.invoke(question)
    except Exception as e:
        logging.error(
            f"[ERROR] Falha ao invocar {type(retriever).__name__ if retriever else 'None'}: {str(e)}"
        )
        return []


def combine_contexts(inputs):
    context_keys = [
        'iniciativas_contexto',
        'iesgo_contexto',
        'imgg_contexto',
        'indicadores_contexto',
        'diagnostico_imgg_contexto',
        'diagnostico_iesgo_contexto',
        'oms_contexto',
        'padroes_contexto',
        'pta_contexto',
        'riscos_contexto',
        'estatuto_social_contexto',
        'estrutura_processos_contexto',
        'regimento_interno_contexto',
        'gerentes_contexto',
    ]

    combined_contexts_list = []
    for context_key in context_keys:
        if context_key in inputs and inputs[context_key]:
            docs = inputs[context_key]
            if isinstance(docs, list) and all(
                hasattr(doc, 'page_content') for doc in docs
            ):
                combined_contexts_list.append(
                    '\n'.join(doc.page_content for doc in docs)
                )
    final_combined_context = '\n\n'.join(filter(None, combined_contexts_list))

    return {
        'pergunta': inputs['pergunta'],
        'contexto': final_combined_context,
        'memoria': inputs['memoria'],
    }


if __name__ == '__main__':

    class Document:
        def __init__(self, page_content):
            self.page_content = page_content

    sample_inputs = {
        'pergunta': 'Qual é o principal objetivo?',
        'memoria': 'Histórico da conversa anterior...',
        'iniciativas_contexto': [
            Document('Conteúdo sobre iniciativas A.'),
            Document('Mais sobre iniciativa B.'),
        ],
        'iesgo_contexto': [
            Document(
                'Detalhes do IESGO (Índice de Eficiência e Sustentabilidade da Governança)'
            )
        ],
        'imgg_contexto': [
            Document(
                'Detalhes sobre o IMGG (Instrumento de Maturidade de Governança e Gestão)'
            )
        ],
        'indicadores_contexto': [
            Document('Indicador X é: .'),
            Document('Indicador Y é: .'),
        ],
        'diagnostico_imgg_contexto': [Document('Diagnóstico IMGG: tudo ok.')],
        'diagnostico_iesgo_contexto': [
            Document('Diagnóstico IESGO: atenção necessária.')
        ],
        'oms_contexto': [Document('Informação da OMS relevante.')],
        'padroes_contexto': [Document('Padrão Alfa definido.')],
        'pta_contexto': [Document('PTA para o ano corrente.')],
        'riscos_contexto': [Document('Risco identificado: R1.')],
        'estatuto_social_contexto': [
            Document('Artigo 1 do estatuto social.'),
            Document('Capital social definido.'),
        ],
        'estrutura_processos_contexto': [
            Document('Processo P1 descrito.'),
            Document('Fluxo do processo P2.'),
        ],
        'regimento_interno_contexto': [
            Document('Artigo 1 do regimento interno.'),
            Document('Norma X definida no regimento.'),
        ],
        'gerentes_contexto': [
            Document('Gerente: Fulano de Tal'),
            Document('Equipe: Beltrano, Ciclano'),
        ],
    }

    combined_output = combine_contexts(sample_inputs)
    print('--- Pergunta ---')
    print(combined_output['pergunta'])
    print('\n--- Memória ---')
    print(combined_output['memoria'])
    print('\n--- Contexto Combinado ---')
    print(combined_output['contexto'])

    sample_inputs_missing = {
        'pergunta': 'Qual o risco?',
        'memoria': 'Outra conversa.',
        'riscos_contexto': [Document('Risco Z é alto.')],
        'estatuto_social_contexto': None,
        'regimento_interno_contexto': None,
        'gerentes_contexto': [Document('Gerente: Fulano de Tal')],
    }
    combined_output_missing = combine_contexts(sample_inputs_missing)
    print('\n\n--- Teste com Contextos Faltando ---')
    print('--- Pergunta ---')
    print(combined_output_missing['pergunta'])
    print('\n--- Contexto Combinado ---')
    print(combined_output_missing['contexto'])

    class MockRetriever:
        def __init__(self, should_fail=False):
            self.should_fail = should_fail

        def invoke(self, question):
            if self.should_fail:
                raise ValueError('Falha simulada no retriever')
            if question == 'teste_sucesso':
                return [Document('Documento de teste do retriever.')]
            return []

    print('\n\n--- Teste safe_invoke ---')
    retriever_sucesso = MockRetriever()
    retriever_falha = MockRetriever(should_fail=True)

    print('Invocando retriever com sucesso:')
    print(safe_invoke(retriever_sucesso, 'teste_sucesso'))
    print('Invocando retriever que falha:')
    print(safe_invoke(retriever_falha, 'qualquer_coisa'))
    print('Invocando retriever None:')
    print(safe_invoke(None, 'qualquer_coisa'))
