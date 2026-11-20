# Guia de Contribuição

Obrigado pelo interesse em colaborar com o **Steam Reviews Toxicity List**! Este guia define regras rápidas para manter a lista precisa, segura e com baixo índice de falsos positivos.

## Regras para Adicionar Termos

1. **Edite o arquivo do seu idioma** em `lists/tos/<linguagem>.csv` (ex.: `pt.csv`, `en.csv`, `es.csv`).
   - Para um novo idioma, crie `lists/tos/<codigo_iso>.csv` usando o código ISO 639-1 em minúsculas (ex.: `fr.csv`, `de.csv`).
2. **Use apenas termos de alto risco de TOS:**
   - Todos os termos na pasta `lists/tos/` devem ter `classificacao = remover` e `motivo = TOS Violation`.
   - **Evite palavras ambíguas ou comuns em jogos/conversas** que geram falsos positivos (ex.: `die`, `morrer`, `aviso`, `negro`, `pau`, `rola`, `caralho`). Termos leves ou dependentes de contexto não pertencem à lista de remoção por TOS.
3. **Respeite o formato CSV (UTF-8):**
   - Colunas obrigatórias: `termo,classificacao,linguagem,motivo,categoria`
   - Escreva `termo` e `linguagem` em minúsculas, sem espaços extras nas pontas.
   - Não adicione duplicatas `(termo, linguagem)`.
4. **Privacidade e segurança:**
   - **Nunca** inclua textos completos de reviews reais, nomes de usuários, links ou dados pessoais em commits, Issues ou PRs.
   - **Nunca** inclua conteúdo ilegal extremo (CSAM, instruções de violência real/terrorismo ou doxxing).

## Como Enviar seu Pull Request

1. Faça um fork e crie uma branch (`git checkout -b feat/termos-pt`).
2. Edite o arquivo do idioma em `lists/tos/`.
3. Execute o script de build e validação para atualizar `lists/lista_tos.csv`:
   ```bash
   python scripts/build_and_validate.py
   ```
4. Abra o Pull Request descrevendo:
   - O idioma alterado;
   - A categoria e o motivo técnico dos termos adicionados ou removidos (ex.: erro HTTP 400 observado em inferência ou relato de falso positivo).
