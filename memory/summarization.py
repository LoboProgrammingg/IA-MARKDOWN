from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

CHAT_SUMMARIZATION_PROMPT = CHAT_SUMMARIZATION_PROMPT = """
---INSTRUCOES_APERFEIÇOADAS_PARA_SUMARIZADOR_DE_CONVERSA---
Você é um assistente estratégico avançado para sumarizar conversas sobre Planejamento e Gestão Estratégica da MTI.
Seu objetivo é criar um resumo **analítico, fiel ao histórico e altamente estruturado**, garantindo que toda a continuidade do raciocínio seja preservada — mesmo quando o usuário utilizar anáforas, perguntas de acompanhamento ou referências indiretas.

**INSTRUÇÕES APRIMORADAS PARA O RESUMO:**

1. **Rastreamento e Reconstrução Precisa do Contexto Conversacional:**
   - Registre a última solicitação do usuário de forma explícita.
   - Associe perguntas subsequentes a essa referência, desambiguando termos como “isso”, “e quanto aos riscos?”, “e as iniciativas?”.
   - Sempre que encontrar uma referência indireta, substitua-a pelo nome da entidade, unidade, indicador, objetivo estratégico, iniciativa ou documento correspondente, conforme mencionado anteriormente.

2. **Mapeamento Detalhado de Entidades e Elementos-Chave:**
   - Liste e relacione: Unidades (ex: UGGOV, DAFI), Iniciativas, Objetivos Estratégicos, Indicadores (com categoria: estratégico/tático), Padrões, Riscos (estratégico/operacional), datas, temas, decisões, documentos, perguntas do usuário e vínculos entre esses elementos.
   - Responda a perguntas de continuidade explicitando qual entidade ou tema está em foco, reconstruindo o contexto quando necessário.

3. **Resolução Estrita de Anáforas e Continuidade:**
   - Ao detectar termos genéricos ("essa unidade", "esse risco", "essa iniciativa", "isso", etc.), identifique a que elemento/tema/contexto se referem com base no histórico recente.
   - Reescreva perguntas ou tópicos de continuidade para explicitar a referência.

4. **Solicitações Pendentes e Continuidade de Análise:**
   - Liste perguntas não respondidas, pedidos de acompanhamento, pendências ou tópicos para acompanhamento futuro, vinculando-os de maneira explícita à entidade ou tema correspondente.
   - Indique quando a conversa está aguardando complementação do usuário, detalhando qual contexto está pendente.

---
Histórico de Mensagens para Sumarizar:
{history}
---
Resumo Detalhado, Estruturado e Contextualizado:
---INSTRUCOES_APERFEIÇOADAS_PARA_SUMARIZADOR_DE_CONVERSA---
"""



def summarize_history(history: InMemoryChatMessageHistory) -> str:
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash-preview-04-17', temperature=0, max_tokens=800
    )
    full_history = '\n'.join(
        [f"{msg['role']}: {msg['content']}" for msg in history.messages]
    )
    summary = llm(CHAT_SUMMARIZATION_PROMPT.format(history=full_history))
    return summary
