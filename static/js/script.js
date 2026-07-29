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

btnSelecionar.addEventListener("click", () => input.click());

input.addEventListener("change", () => {
    arquivos = [...input.files];
    atualizarLista();
});

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("dragover");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("dragover");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("dragover");

    arquivos = [...e.dataTransfer.files];
    atualizarLista();
});

function atualizarLista() {

    lista.innerHTML = "";

    arquivos.forEach(file => {

        lista.innerHTML += `
            <div class="arquivo">
                📄 ${file.name}
            </div>
        `;

    });

}

btnProcessar.addEventListener("click", async () => {

    if (arquivos.length === 0) {
        alert("Selecione pelo menos um PDF.");
        return;
    }

    let sucesso = 0;
    let erro = 0;

    btnProcessar.disabled = true;
    btnSelecionar.disabled = true;
    btnDownload.style.display = "none";

    tabelaResultados.innerHTML = "";
    logs.innerHTML = "";

    totalArquivos.innerText = arquivos.length;
    totalSucesso.innerText = "0";
    totalErro.innerText = "0";

    progressoContainer.style.display = "block";

    barra.style.width = "0%";
    barra.innerText = "0%";

    texto.innerHTML = "Iniciando processamento...";

    const total = arquivos.length;

    for (let i = 0; i < total; i++) {

        texto.innerHTML = `Processando ${i + 1} de ${total}...`;

        const formData = new FormData();
        formData.append("arquivos", arquivos[i]);

        try {

            const resposta = await fetch("/processar", {
                method: "POST",
                body: formData
            });

            if (!resposta.ok) {
                throw new Error("Erro ao processar o arquivo.");
            }

            const dados = await resposta.json();

            dados.resultados.forEach(resultado => {

                tabelaResultados.innerHTML += `
                    <tr>
                        <td>${resultado.arquivo_original}</td>
                        <td>${resultado.numero_nf ?? "-"}</td>
                        <td>${resultado.arquivo_final ?? "-"}</td>
                        <td>${resultado.status}</td>
                    </tr>
                `;

                sucesso++;
                totalSucesso.innerText = sucesso;

                logs.innerHTML += `
                    <div class="text-success">
                        ✔ ${resultado.arquivo_original} → ${resultado.arquivo_final}
                    </div>
                `;

                logs.scrollTop = logs.scrollHeight;

            });

        } catch (e) {

            console.error(e);

            erro++;
            totalErro.innerText = erro;

            tabelaResultados.innerHTML += `
                <tr class="table-danger">
                    <td>${arquivos[i].name}</td>
                    <td>-</td>
                    <td>-</td>
                    <td>Erro ao processar</td>
                </tr>
            `;

            logs.innerHTML += `
                <div class="text-danger">
                    ✖ ${arquivos[i].name} → Erro ao processar
                </div>
            `;

            logs.scrollTop = logs.scrollHeight;

        }

        const porcentagem = Math.round(((i + 1) / total) * 100);

        barra.style.width = porcentagem + "%";
        barra.innerText = porcentagem + "%";

    }

    texto.innerHTML = `✅ Processamento concluído!<br>Sucesso: ${sucesso} | Erros: ${erro}`;

    btnDownload.style.display = "inline-block";

    btnProcessar.disabled = false;
    btnSelecionar.disabled = false;

});

btnDownload.addEventListener("click", () => {

    window.location.href = "/download";

});