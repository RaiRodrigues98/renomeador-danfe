# Renomeador DANFE v6

Versão otimizada para DANFEs de layout fixo e deploy no Railway.

## Como funciona

1. Renderiza somente a área do código de barras da primeira página.
2. Lê a chave NF-e (Code 128) com ZBar.
3. Extrai os 9 dígitos de `nNF` da chave de 44 dígitos.
4. Remove zeros à esquerda e renomeia o PDF.
5. Se o código de barras falhar, usa Tesseract apenas no pequeno campo superior direito.

O motor antigo RapidOCR/ONNX/OpenCV foi removido.

## Variáveis recomendadas no Railway

```env
WEB_CONCURRENCY=1
MAX_CONCURRENT_PROCESSING=3
BARCODE_DPI=180
OCR_DPI=180
DATA_DIR=/tmp/renomeador-danfe
```

## Deploy

O projeto contém Dockerfile e railway.toml. No Railway, deixe o Custom Start Command vazio para usar o CMD do Dockerfile.

## Teste local com Docker

```bash
docker build -t renomeador-danfe-v6 .
docker run --rm -p 8080:8080 -e PORT=8080 renomeador-danfe-v6
```

Acesse `http://localhost:8080/health`.
