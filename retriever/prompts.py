from langchain.prompts import PromptTemplate
from .section import Section

PROMPT_TEMPLATES = {
    Section.INICIATIVAS: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Responda de forma objetiva sobre as iniciativas desta seção, relacionando-as às unidades, objetivos estratégicos e demais elementos relevantes. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.IESGO: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Explique e detalhe informações relacionadas ao Índice de Eficiência e Sustentabilidade da Governança (iESGo), focando nos diagnósticos, critérios avaliados e relação com as unidades. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.IMGG: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Forneça informações claras sobre o Instrumento de Maturidade de Governança e Gestão (IMGG), focando em diagnósticos, critérios e vínculos com as unidades. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.INDICADORES: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Explique os indicadores desta seção, seus tipos (estratégico, tático, operacional) e como se relacionam às unidades e iniciativas. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.DIAGNOSTICO_IMGG: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Apresente e relacione os dados do diagnóstico IMGG, detalhando pontos de melhoria, resultados e conexões com as unidades e objetivos. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.DIAGNOSTICO_IESGO: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Apresente e relacione os dados do diagnóstico iESGo, detalhando critérios, oportunidades de melhoria e relação com as unidades. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.OMS: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Forneça informações sobre Oportunidades de Melhoria (OMs), explicando seus critérios, recomendações e impactos para as unidades. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.PADROES: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Responda sobre padrões desta seção, orientando sobre aplicação, benefícios e sua relação com as unidades. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.PTA: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Foque no Plano de Trabalho Anual (PTA). Detalhe códigos de ação, responsáveis, descrições e relacione-os às unidades. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
    Section.RISCOS: PromptTemplate(
        input_variables=['section', 'question', 'connections', 'contexto'],
        template=(
            'Seção: {section}\n'
            'Pergunta: {question}\n'
            'Contexto:\n{contexto}\n'
            'Conexões: {connections}\n'
            'Analise riscos estratégicos desta seção, proponha recomendações e relacione-os com as unidades. '
            'Sempre utilize as informações do contexto acima. '
            'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
        ),
    ),
}

DEFAULT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=['section', 'question', 'connections', 'contexto'],
    template=(
        'Seção: {section}\n'
        'Pergunta: {question}\n'
        'Contexto:\n{contexto}\n'
        'Conexões: {connections}\n'
        'Responda de forma objetiva com base apenas no contexto fornecido. '
        'Se não houver resposta, diga explicitamente que a informação não está disponível no contexto.'
    ),
)


def get_prompt_template(section):
    return PROMPT_TEMPLATES.get(section, DEFAULT_PROMPT_TEMPLATE)
