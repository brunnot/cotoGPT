# Projeto
Uso o Ollama como gerênciados / executor dos modelos.
Fiz teste com os modelos
* **llama2**:   `ollama pull llama2`
* **mistral**:  `ollama pull mistral` 

Para o desenvolvimento do assistente, estou usando o langchain

### Dependências
* python 3.10
* pipenv
* langchain
* streamlit
* streamlit-chat
* pypdf
* chromadb
* fastembed

`pipenv install langchain streamlit streamlit_chat chromadb pypdf fastembed`

### Executando o projeto

 1. Clonar o projeto: `git clone https://github.com/brunnot/cotoGPT.git`
 2. Na pasta do projeto entrar no ambiente virtual: `pipenv shell`
 3. Iniciar a aplicação web: `streamlit run main.py`

### Referências
https://python.langchain.com/docs/get_started/introduction
https://ollama.com/library
