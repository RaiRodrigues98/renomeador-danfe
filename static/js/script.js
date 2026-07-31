const input = document.getElementById("arquivos");
const dropArea = document.getElementById("drop-area");
const lista = document.getElementById("listaArquivos");
const btnSelecionar = document.getElementById("btnSelecionar");
const btnProcessar = document.getElementById("btnProcessar");
const btnDownload = document.getElementById("btnDownload");
const tabelaResultados = document.getElementById("tabelaResultados");
const progressoContainer = document.getElementById("progressoContainer");
const barra = document.getElementById("barraProgresso");
const texto = document.getElementById("textoProgresso");
const totalArquivos = document.getElementById("totalArquivos");
const totalSucesso = document.getElementById("totalSucesso");
const totalErro = document.getElementById("totalErro");
const logs = document.getElementById("logs");

let arquivos = [];
let sessaoAtual = null;

btnSelecionar.addEventListener("click", () => input.click());
input.addEventListener("change", () => definirArquivos([...input.files]));

dropArea.addEventListener("dragover", (evento) => {
    evento.preventDefault();
    dropArea.classList.add("dragover");
});
dropArea.addEventListener("dragleave", () => dropArea.classList.remove("dragover"));
dropArea.addEventListener("drop", (evento) => {
    evento.preventDefault();
    dropArea.classList.remove("dragover");
    definirArquivos([...evento.dataTransfer.files]);
});

function definirArquivos(novosArquivos) {
    arquivos = novosArquivos.filter((arquivo) =>
        arquivo.name.toLowerCase().endsWith(".pdf")
    );
    atualizarLista();
}

function atualizarLista() {
    lista.replaceChildren();
    arquivos.forEach((arquivo) => {
        const item = document.createElement("div");
        item.className = "arquivo";
        item.textContent = `📄 ${arquivo.name}`;
        lista.appendChild(item);
    });
}

function atualizarProgresso(concluidos, total, nomeArquivo = "") {
    const porcentagem = total ? Math.round((concluidos / total) * 100) : 0;
    barra.style.width = `${porcentagem}%`;
    barra.textContent = `${porcentagem}%`;
    barra.setAttribute("aria-valuenow", String(porcentagem));
    texto.textContent = concluidos < total
        ? `Processando ${concluidos + 1} de ${total}: ${nomeArquivo}`
        : `Processamento concluído: ${concluidos} de ${total}`;
}

function adicionarResultado(resultado) {
    const sucesso = resultado.status === "Sucesso";

    const log = document.createElement("div");
    log.className = sucesso ? "text-success" : "text-danger";
    log.textContent = sucesso
        ? `✔ ${resultado.arquivo_original} → ${resultado.arquivo_final}`
        : `✖ ${resultado.arquivo_original} → ${resultado.status}`;
    logs.appendChild(log);

    const linha = document.createElement("tr");
    [
        resultado.arquivo_original,
        resultado.numero_nf ?? "-",
        resultado.arquivo_final ?? "-",
        resultado.status,
    ].forEach((valor) => {
        const celula = document.createElement("td");
        celula.textContent = valor;
        linha.appendChild(celula);
    });
    tabelaResultados.appendChild(linha);
    logs.scrollTop = logs.scrollHeight;
}

async function lerErro(resposta) {
    try {
        const dados = await resposta.json();
        return dados.detail || dados.mensagem || `Erro HTTP ${resposta.status}`;
    } catch {
        return `Erro HTTP ${resposta.status}`;
    }
}

btnProcessar.addEventListener("click", async () => {
    if (arquivos.length === 0) {
        alert("Selecione pelo menos um PDF.");
        return;
    }

    btnProcessar.disabled = true;
    btnSelecionar.disabled = true;
    input.disabled = true;
    btnDownload.style.display = "none";
    tabelaResultados.replaceChildren();
    logs.replaceChildren();
    totalArquivos.textContent = String(arquivos.length);
    totalSucesso.textContent = "0";
    totalErro.textContent = "0";
    progressoContainer.style.display = "block";
    atualizarProgresso(0, arquivos.length, arquivos[0].name);

    let sucesso = 0;
    let erro = 0;

    try {
        const respostaSessao = await fetch("/sessao", { method: "POST" });
        if (!respostaSessao.ok) throw new Error(await lerErro(respostaSessao));
        sessaoAtual = (await respostaSessao.json()).sessao_id;

        let proximoIndice = 0;
        let concluidos = 0;
        const concorrencia = Math.min(3, arquivos.length);

        async function processarProximo() {
            while (true) {
                const indice = proximoIndice;
                proximoIndice += 1;
                if (indice >= arquivos.length) return;

                const arquivo = arquivos[indice];
                atualizarProgresso(concluidos, arquivos.length, arquivo.name);

                const formData = new FormData();
                formData.append("sessao_id", sessaoAtual);
                formData.append("arquivo", arquivo);

                try {
                    const resposta = await fetch("/processar-arquivo", {
                        method: "POST",
                        body: formData,
                    });
                    if (!resposta.ok) throw new Error(await lerErro(resposta));

                    const resultado = await resposta.json();
                    adicionarResultado(resultado);
                    if (resultado.status === "Sucesso") sucesso += 1;
                    else erro += 1;
                } catch (falhaArquivo) {
                    erro += 1;
                    adicionarResultado({
                        arquivo_original: arquivo.name,
                        arquivo_final: null,
                        numero_nf: null,
                        status: `Erro: ${falhaArquivo.message}`,
                    });
                }

                concluidos += 1;
                totalSucesso.textContent = String(sucesso);
                totalErro.textContent = String(erro);
                atualizarProgresso(concluidos, arquivos.length);
                await new Promise((resolve) => requestAnimationFrame(resolve));
            }
        }

        await Promise.all(
            Array.from({ length: concorrencia }, () => processarProximo())
        );

        texto.innerHTML = `✅ Processamento concluído!<br>Sucesso: ${sucesso} | Erros: ${erro}`;
        if (sucesso > 0) btnDownload.style.display = "inline-block";
    } catch (falha) {
        console.error(falha);
        texto.textContent = `Erro durante o processamento: ${falha.message}`;
        alert(`Erro ao iniciar o processamento: ${falha.message}`);
    } finally {
        btnProcessar.disabled = false;
        btnSelecionar.disabled = false;
        input.disabled = false;
    }
});

btnDownload.addEventListener("click", () => {
    if (sessaoAtual) window.location.href = `/download/${sessaoAtual}`;
});
