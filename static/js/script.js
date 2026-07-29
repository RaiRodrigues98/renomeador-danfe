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

    arquivos = [...e.dataTransfer.files].filter(
        arquivo => arquivo.name.toLowerCase().endsWith(".pdf")
    );

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

    let sucesso = 0;
    let erro = 0;

    const formData = new FormData();

    arquivos.forEach(file => {
        formData.append("arquivos", file);
    });

    try {

        texto.innerHTML = "Processando arquivos...";

        const resposta = await fetch("/processar", {
            method: "POST",
            body: formData
        });

        if (!resposta.ok) {
            throw new Error("Erro ao processar.");
        }

        const dados = await resposta.json();

        dados.resultados.forEach((resultado, index) => {

            if (resultado.status === "Sucesso") {
                sucesso++;

                logs.innerHTML += `
                    <div class="text-success">
                        ✔ ${resultado.arquivo_original} → ${resultado.arquivo_final}
                    </div>
                `;
            } else {
                erro++;

                logs.innerHTML += `
                    <div class="text-danger">
                        ✖ ${resultado.arquivo_original} → ${resultado.status}
                    </div>
                `;
            }

            tabelaResultados.innerHTML += `
                <tr>
                    <td>${resultado.arquivo_original}</td>
                    <td>${resultado.numero_nf ?? "-"}</td>
                    <td>${resultado.arquivo_final ?? "-"}</td>
                    <td>${resultado.status}</td>
                </tr>
            `;

            totalSucesso.innerText = sucesso;
            totalErro.innerText = erro;

            const porcentagem = Math.round(((index + 1) / dados.resultados.length) * 100);

            barra.style.width = porcentagem + "%";
            barra.innerText = porcentagem + "%";

            logs.scrollTop = logs.scrollHeight;

        });

        texto.innerHTML = `✅ Processamento concluído!<br>Sucesso: ${sucesso} | Erros: ${erro}`;

        if (sucesso > 0) {
            btnDownload.style.display = "inline-block";
        }

    } catch (e) {

        console.error(e);

        alert("Erro ao processar os arquivos.");

        texto.innerHTML = "Erro durante o processamento.";

    }

    btnProcessar.disabled = false;
    btnSelecionar.disabled = false;

});

btnDownload.addEventListener("click", () => {

    window.location.href = "/download";

});