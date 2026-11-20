# Steam Reviews Toxicity List

> **Aviso de Conteúdo (Content Warning):** Este repositório contém termos ofensivos, discurso de ódio e linguagem sexual explícita listados **estritamente para fins defensivos de moderação de conteúdo, pesquisa de segurança e filtragem pré-LLM**. O projeto não endossa nenhum termo listado e não deve ser utilizado para assédio ou geração de conteúdo abusivo.
>
> *Projeto independente e open source, sem afiliação com Valve/Steam, Google, OpenAI, Anthropic ou qualquer provedor de IA.*

Lista colaborativa e multilíngue de termos críticos de toxicidade e **Violação de Termos de Serviço (TOS)** encontrados em **reviews da Steam**, criada para **blindar pipelines de texto antes da inferência em LLMs**.

---

## Objetivo

Atuar como uma **camada local e determinística de blindagem pré-inferência**, identificando e removendo textos nocivos (reviews, comentários, chats, tickets) **antes** que sejam enviados para APIs de LLMs com políticas de segurança estritas — como **Google Gemini** (incluindo modelos da família `gemini-decision`), **OpenAI**, entre outros.

### Problemas e riscos que este projeto resolve

Ao processar grandes volumes de texto gerado por usuários (UGC) diretamente em LLMs comerciais, você fica exposto a riscos operacionais e de conta:

- **Bloqueios HTTP 400 (`PROHIBITED_CONTENT` / `TOS Violation`):** textos com conteúdo extremo são rejeitados na entrada, quebrando pipelines em lote, interrompendo filas e gerando retries inúteis.
- **Risco de restrição, suspensão ou banimento do projeto/conta:** o envio recorrente de conteúdo que viola os Termos de Serviço pode acionar sistemas automáticos de prevenção a abuso do provedor, resultando em **limitação de cota, bloqueio da API key, suspensão do projeto ou banimento permanente da conta**.
- **Desperdício de custo e latência:** enviar textos inevitavelmente bloqueáveis consome tempo de processamento e aumenta o risco de falhas em cascata.
- **Falsos positivos de listas genéricas:** muitas listas públicas bloqueiam palavras comuns de jogos ou uso coloquial (como `die`, `morrer`, `aviso`, `caralho`). Aqui, a lista de TOS foca **apenas em termos de alto risco real**, deixando termos leves ou contextuais para camadas de censura separadas.

---

## Estrutura do Projeto

```text
├── lists/
│   ├── tos/
│   │   ├── pt.csv          # Termos em Português
│   │   ├── en.csv          # Termos em Inglês
│   │   └── es.csv          # Termos em Espanhol
│   └── lista_tos.csv       # Lista consolidada (gerada a partir de lists/tos/*.csv)
├── scripts/
│   └── build_and_validate.py
├── .github/workflows/
│   └── validate.yml        # Validação automática em Pull Requests
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

Cada idioma possui seu próprio CSV em `lists/tos/` para facilitar revisões e contribuições focadas por falantes nativos. O arquivo `lists/lista_tos.csv` reúne automaticamente todos os idiomas.

---

## Esquema das Colunas

Todos os arquivos CSV seguem exatamente o mesmo padrão UTF-8 com 5 colunas:

| Coluna | Obrigatória | Descrição | Valores esperados |
| :--- | :---: | :--- | :--- |
| `termo` | Sim | Palavra ou expressão exata (em minúsculas) a ser bloqueada antes da inferência. | Ex.: `nigger`, `gay sex`, `bater em mulher` |
| `classificacao` | Sim | Ação recomendada para o filtro local. Na lista de TOS, **todos os termos devem ser `remover`** (descartar/barrar o texto antes da API). | `remover` |
| `linguagem` | Sim | Código ISO 639-1 do idioma do termo. Deve corresponder ao nome do arquivo em `lists/tos/<linguagem>.csv`. | `pt`, `en`, `es`, `fr`, `de`, etc. |
| `motivo` | Sim | Motivo técnico pelo qual o termo está na lista. | `TOS Violation` |
| `categoria` | Sim | Categoria de violação de política associada ao termo. | `Discurso de ódio (Racismo)`, `Discurso de ódio (Homofobia)`, `Discurso de ódio (Capacitismo)`, `Violência / Discurso de ódio (Misoginia)`, `Conteúdo sexual explícito`, `Ameaça / Violência` |

---

## Validação e Build Local

Após editar qualquer arquivo em `lists/tos/`, execute o script para validar o formato e regerar `lists/lista_tos.csv`:

```bash
python scripts/build_and_validate.py
```

Para apenas validar sem modificar arquivos (mesmo comando usado no CI):

```bash
python scripts/build_and_validate.py --check
```

---

## Colabore com o Projeto

A linguagem na internet muda rápido e cada idioma tem suas próprias gírias, variações e formas de evasão. **Sua contribuição ajuda toda a comunidade a manter pipelines de IA mais seguros e estáveis.**

Você pode contribuir de três formas:
1. **Adicionando novos termos** em um idioma existente (`lists/tos/pt.csv`, `en.csv`, `es.csv`).
2. **Criando suporte a um novo idioma** adicionando um arquivo `lists/tos/<codigo_iso>.csv` (ex.: `fr.csv`, `de.csv`, `it.csv`).
3. **Reportando falsos positivos** via Issue caso algum termo esteja barrando textos legítimos.

Leia o guia rápido em [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir seu Pull Request.

---

## Licença

Distribuído sob a licença [MIT](LICENSE).
