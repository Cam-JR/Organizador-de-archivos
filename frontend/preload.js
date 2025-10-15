const { contextBridge, ipcRenderer } = require('electron');

// Exponer API segura al frontend
contextBridge.exposeInMainWorld('electronAPI', {
  selectFolder: async () => {
    return await ipcRenderer.invoke('dialog:openDirectory');
  }
});
