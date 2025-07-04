# 🤖 Assistente Estratégico

O **Assistente Estratégico** é uma aplicação avançada baseada em Inteligência Artificial, desenvolvida com as tecnologias `Streamlit`, `LangChain` e integração com modelos da OpenAI. Esta solução é projetada para fornecer suporte estratégico, processando perguntas e oferecendo respostas contextuais fundamentadas em documentos estruturados e pré-processados.

---

## 🚀 Funcionalidades Principais

- **Análise Contextual Inteligente**: As respostas são geradas com base na similaridade semântica de documentos fornecidos, garantindo precisão e relevância.
- **Pipeline Modular e Personalizado**: Configurado para processar consultas e buscar contextos relevantes de forma eficaz.
- **Interface de Usuário Intuitiva**: Desenvolvida com `Streamlit`, oferecendo estilização avançada e experiência interativa.
- **Atualização Automática de Dados**: Detecta alterações em documentos e recria o vetor FAISS automaticamente, mantendo os dados atualizados.

---

## 🛠️ Estrutura do Projeto

A organização do projeto segue uma estrutura modular e escalável:

```plaintext
project/
├── .gitignore
├── README.md
├── ChatBot.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── config/ 
│   ├── __init__.py
│   ├── config.py
│   ├── user.json
│   └── utils.py
├── dashboards/
│   ├── __init__.py
│   ├── dashboards_utils.py
│   └── iniciativas_dashboard.py
├── database/
│   ├── __init__.py
│   ├── file_handler.py
│   ├── metadata/
│   │   ├── markdown_indicadores.py
│   │   ├── markdown_padroes.py
│   │   ├── markdown_processor_estrutura.py
│   │   ├── markdown_processor_iniciativas.py
│   │   ├── markdown_processor_oms.py
│   │   ├── markdown_processor_pta.py
│   │   ├── markdown_recursive.py
│   │   └── markdown_riscos.py
│   └── vectorstore_handler.py
├── data/
│   ├── indicadores.csv
│   └── iniciativas.csv
├── documentation/
│   ├── iesgo_structured.md
│   ├── imgg_structured.md
│   ├── Iniciativas.md
│   ├── estatuto_social_structured.md
│   ├── diagnostico_iesgo_structured.md
│   ├── diagnostico_imgg_structured.md
│   ├── indicadores_structured.md
│   ├── instrucoes_chatbot.md
│   ├── oms_unidade.md
│   ├── padroes.md
│   ├── pta_descricao_structured.md
│   ├── riscos_structured.md
│   ├── estrutura_processos_structured.md
│   ├── regimento_interno_structured.md
│   └── instrucoes.md
├── histories/
│   └── checks_confirmed.json
├── memory/
│   ├── __init__.py
│   ├── compaction.py
│   ├── filters.py
│   ├── summarization.py
│   ├── truncation.py
│   └── memory_handler.py
├── pages/
│   ├── 1_📖 Instruções.py
│   ├── 2_⚙️_Editar_Perfil.py
│   ├── 3_📊 Dashboards.py
│   └── 4_👑_Admin.py
├── pipeline/
│   ├── __init__.py
│   ├── handler.py
│   ├── stream.py
│   └── utils.py
├── prompt/
│   ├── __init__.py
│   └── prompt_template.py
├── retriever/
│   ├── __init__.py
│   ├── retrievers.py
│   └── section.py
```

---

## 🔧 Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- Python 3.8 ou superior
- `pip` ou `conda` para gerenciamento de pacotes

---

## 📦 Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/LoboProgrammingg/IA-MARKDOWN
   cd IA-MARKDOWN
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   - Crie um arquivo `.env` na pasta raiz do projeto:
     ```
     OPENAI_API_KEY=seu_api_key_aqui
     ```
   - Substitua `seu_api_key_aqui` pela sua chave de API da OpenAI.

---

## 📂 Configuração de Dados

1. **Arquivo Markdown**:
   - O arquivo `arquivo.md` deve conter dados estruturados para análise pela IA.
   - Estrutura esperada:
     ```markdown
     ## Unidade: Nome da Unidade
     Conteúdo relacionado ao meu projeto...

     ## Unidade: Outra Unidade
     Mais informações...
     ```

2. **VectorStore (FAISS)**:
   - O sistema detecta automaticamente mudanças no arquivo `arquivo.md` e recria o vetor FAISS conforme necessário, garantindo que os dados estejam sempre atualizados.

---

## ▶️ Como Executar

1. Inicie a aplicação:
   ```bash
   streamlit run app.py
   ```

2. Acesse o navegador no link fornecido pelo terminal (geralmente `http://localhost:8501`).

---

## 🔍 Pipeline de Processamento

O pipeline, configurado no arquivo `pipeline.py`, segue as etapas abaixo:

1. **Carregamento do VectorStore**:
   - A função `get_vectorstore` no arquivo `vectorstore_handler.py` verifica e atualiza automaticamente o vetor FAISS com base no arquivo Markdown.

2. **Configuração do Pipeline**:
   - Utiliza o retriever do FAISS para localizar os contextos mais relevantes.
   - Processa as consultas com o modelo da OpenAI (`gpt-4o-mini`), garantindo respostas precisas e contextualizadas.

3. **Resposta em Streaming**:
   - As respostas são geradas em tempo real e exibidas na interface do Streamlit.

---

## 🎨 Interface do Usuário

A interface da aplicação foi projetada com atenção ao design e facilidade de uso:

- **Chat Interativo**:
  - Mensagens do usuário e da IA são exibidas em balões estilizados.
  - O texto da IA é formatado para destacar palavras-chave como `Unidade`, `Objetivo Estratégico`, etc.

- **Estilo Visual Personalizado**:
  - Cores, fontes e layout foram ajustados para proporcionar uma experiência visual agradável e profissional.

---

## ✨ Exemplos de Uso

### Entrada do Usuário:
```plaintext
Qual é o objetivo estratégico da Unidade X?
```

### Resposta da IA:
```plaintext
Unidade: Unidade X

Objetivo Estratégico: Aumentar a eficiência operacional...

Perspectiva: Interna
```

---

## 🛠️ Manutenção e Atualização

### Atualização do VectorStore
- Sempre que o arquivo `arquivo.md` for alterado, o sistema detectará as mudanças e recriará automaticamente o vetor FAISS.

### Adicionando Novas Funcionalidades
- **Prompt**: Edite o arquivo `prompt_template.py` para ajustar o formato ou mensagem padrão.
- **Modelos**: Atualize o modelo no arquivo `pipeline.py` para utilizar novas versões ou modelos diferentes da OpenAI.

---

## 🧑‍💻 Contribuindo

Contribuições são sempre bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie uma nova branch:
   ```bash
   git checkout -b minha-nova-funcionalidade
   ```
3. Faça suas alterações e envie um pull request.

---

## 📞 Suporte

Se você tiver dúvidas ou precisar de suporte, sinta-se à vontade para abrir uma [issue](https://github.com/LoboProgrammingg/IA-MARKDOWN/issues).
