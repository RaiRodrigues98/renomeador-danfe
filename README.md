# Renomeador DANFE v4

Aplicação FastAPI para localizar o número da NF em DANFEs e renomear os PDFs. A interface visual original foi preservada.

## Melhorias da v4

- extração direta do texto antes do OCR;
- OCR preguiçoso e limitado para evitar estouro de memória;
- múltiplos recortes e tratamentos de imagem para DANFEs digitalizados;
- validação real do conteúdo PDF;
- isolamento por sessão, nomes seguros e ZIP criado de forma atômica;
- logs no stdout, adequados ao Railway;
- Dockerfile sem execução como root e healthcheck configurado;
- armazenamento temporário em `/tmp`, sem exigir volume persistente.

## Execução local com Python

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Acesse `http://localhost:8000`.

## Execução com Docker

```bash
docker build -t renomeador-danfe-v4 .
docker run --rm -p 8080:8080 renomeador-danfe-v4
```

## Deploy no Railway

1. Envie esta pasta para um repositório GitHub.
2. No Railway, escolha **New Project > Deploy from GitHub repo**.
3. Selecione o repositório. O Railway usará o `Dockerfile` e o `railway.toml` automaticamente.
4. Em **Networking**, gere um domínio público.
5. Não configure volume para o uso normal: os arquivos são temporários e expiram.

Variáveis opcionais estão documentadas em `.env.example`. Para o plano com pouca memória, mantenha `WEB_CONCURRENCY=1` e `MAX_CONCURRENT_OCR=1`.

## Observação operacional

Arquivos enviados ficam no armazenamento temporário da instância e são removidos após o TTL. Um redeploy pode apagá-los antes do download; por isso, processe e baixe o ZIP na mesma sessão.
