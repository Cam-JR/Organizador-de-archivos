const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let flaskProcess;
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 980,
    height: 720,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  // 👉 Conectar con Flask
  const pythonCmd = process.platform === "win32" ? "python" : "python3";
  const script = path.join(__dirname, "../backend/app.py");

  flaskProcess = spawn(pythonCmd, [script]);

  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask: ${data.toString()}`);
  });
  flaskProcess.stderr.on("data", (data) => {
    console.error(`Flask err: ${data.toString()}`);
  });

  setTimeout(() => {
    mainWindow.loadURL("http://127.0.0.1:5000");
  }, 1800);

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

// 🟢 ESTE BLOQUE AGREGA EL DIÁLOGO PARA EL BOTÓN “Seleccionar”
ipcMain.handle("dialog:openDirectory", async () => {
  const result = await dialog.showOpenDialog({
    properties: ["openDirectory"]
  });
  if (!result.canceled) return result.filePaths[0];
});

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (flaskProcess) flaskProcess.kill();
  if (process.platform !== "darwin") app.quit();
});
