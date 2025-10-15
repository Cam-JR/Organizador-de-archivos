const folderInput = document.getElementById("folderInput");
const selectBtn = document.getElementById("selectBtn");
const organizeBtn = document.getElementById("organizeBtn");
const previewBtn = document.getElementById("previewBtn");
const resultEl = document.getElementById("result");
const dateBySelect = document.getElementById("dateBy");

let isElectron = !!(window && window.process && window.process.type); // fallback

// Si estamos en Electron, podemos usar la API expuesta por preload
selectBtn.addEventListener("click", async () => {
  if (window.electronAPI && window.electronAPI.selectFolder) {
    const folder = await window.electronAPI.selectFolder();
    if (folder) folderInput.value = folder;
  } else {
    // fallback: usa input file (pero no dará ruta absoluta en navegador)
    const input = document.createElement("input");
    input.type = "file";
    input.webkitdirectory = true;
    input.directory = true;
    input.addEventListener("change", () => {
      if (input.files.length > 0) {
        // extracción distinta en navegador: no fiable para ruta absoluta
        const rel = input.files[0].webkitRelativePath;
        const top = rel.split("/")[0];
        folderInput.value = top;
        resultEl.textContent = "Nota: selección en navegador puede no dar ruta completa.";
      }
    });
    input.click();
  }
});

async function sendOrganize(preview = false) {
  let folder = folderInput.value.trim();
  if (!folder) {
    resultEl.textContent = "Por favor indica o selecciona una carpeta";
    return;
  }
  folder = folder.replace(/\\/g, "/");
  const mode = document.querySelector('input[name="mode"]:checked').value;
  const dateBy = dateBySelect.value;

  resultEl.textContent = preview ? "⏳ Generando vista previa..." : "⏳ Organizando...";

  const endpoint = preview ? "/preview" : "/organize";

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folder, mode, dateBy })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      const r = data.result;
      resultEl.innerHTML = preview
        ? `<strong>Vista previa:</strong> ${r.count} archivos se moverían.`
        : `<strong>Hecho:</strong> ${r.count} archivos organizados.`;
      if (r.count > 0) {
        const list = r.moved
          .slice(0, 10)
          .map(it => `<li>${it.to ? it.to : JSON.stringify(it)}</li>`)
          .join("");
        resultEl.innerHTML += `<ul>${list}${r.count > 10 ? "<li>...más</li>" : ""}</ul>`;
      }
    } else {
      resultEl.textContent = `❌ ${data.error || "Error desconocido"}`;
    }
  } catch (e) {
    resultEl.textContent = `⚠️ Error de conexión: ${e.message}`;
  }
}


organizeBtn.addEventListener("click", () => sendOrganize(false));
previewBtn.addEventListener("click", () => {
  // nota: en esta versión preview hace lo mismo que organizar; podrías agreg ar endpoint /preview
  sendOrganize(true);
});
