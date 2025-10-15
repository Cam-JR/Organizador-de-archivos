import os
import shutil
from datetime import datetime

def _unique_dest(dest):
    base, ext = os.path.splitext(dest)
    counter = 1
    new = dest
    while os.path.exists(new):
        new = f"{base} ({counter}){ext}"
        counter += 1
    return new

def organize_by_type(folder, extensions_map=None):
    if extensions_map is None:
        extensions_map = {
            "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
            "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
            "Videos": [".mp4", ".mkv", ".mov", ".avi"],
            "Audio": [".mp3", ".wav", ".flac"],
            "Comprimidos": [".zip", ".rar", ".7z"],
            "Ejecutables": [".exe", ".msi", ".dmg"],
            "Código": [".js", ".py", ".html", ".css", ".json", ".ts"]
        }

    moved = []
    for fname in list(os.listdir(folder)):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1].lower()
            moved_flag = False
            for category, exts in extensions_map.items():
                if ext in exts:
                    dest_dir = os.path.join(folder, category)
                    os.makedirs(dest_dir, exist_ok=True)
                    dest = os.path.join(dest_dir, fname)
                    dest = _unique_dest(dest)
                    shutil.move(fpath, dest)
                    moved.append({"from": fpath, "to": dest, "category": category})
                    moved_flag = True
                    break
            if not moved_flag:
                # mueve a "Otros"
                dest_dir = os.path.join(folder, "Otros")
                os.makedirs(dest_dir, exist_ok=True)
                dest = os.path.join(dest_dir, fname)
                dest = _unique_dest(dest)
                shutil.move(fpath, dest)
                moved.append({"from": fpath, "to": dest, "category": "Otros"})
    return {"moved": moved, "count": len(moved)}

def organize_by_date(folder, by="modified"):
    """
    Crea subcarpetas por fecha YYYY-MM-DD basadas en la fecha de modificación
    y mueve los archivos a la carpeta correspondiente.
    """
    moved = []
    for fname in list(os.listdir(folder)):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            if by == "modified":
                ts = os.path.getmtime(fpath)
            elif by == "created":
                ts = os.path.getctime(fpath)
            else:
                ts = os.path.getmtime(fpath)

            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            dest_dir = os.path.join(folder, date_str)
            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, fname)
            dest = _unique_dest(dest)
            shutil.move(fpath, dest)
            moved.append({"from": fpath, "to": dest, "date": date_str})
    # Ordena la lista por fecha (reciente → antiguo) antes de devolver
    moved_sorted = sorted(moved, key=lambda x: x["date"], reverse=True)
    return {"moved": moved_sorted, "count": len(moved_sorted)}


#Parte de vista-previa

def simulate_by_type(folder, extensions_map=None):
    if extensions_map is None:
        extensions_map = {
            "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
            "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
            "Videos": [".mp4", ".mkv", ".mov", ".avi"],
            "Audio": [".mp3", ".wav", ".flac"],
            "Comprimidos": [".zip", ".rar", ".7z"],
            "Ejecutables": [".exe", ".msi", ".dmg"],
            "Código": [".js", ".py", ".html", ".css", ".json", ".ts"]
        }

    simulated = []
    for fname in list(os.listdir(folder)):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1].lower()
            category = next((cat for cat, exts in extensions_map.items() if ext in exts), "Otros")
            dest_dir = os.path.join(folder, category)
            dest = os.path.join(dest_dir, fname)
            simulated.append({"from": fpath, "to": dest, "category": category})
    return {"moved": simulated, "count": len(simulated)}


def simulate_by_date(folder, by="modified"):
    simulated = []
    for fname in list(os.listdir(folder)):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            if by == "modified":
                ts = os.path.getmtime(fpath)
            elif by == "created":
                ts = os.path.getctime(fpath)
            else:
                ts = os.path.getmtime(fpath)

            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            dest_dir = os.path.join(folder, date_str)
            dest = os.path.join(dest_dir, fname)
            simulated.append({"from": fpath, "to": dest, "date": date_str})
    simulated_sorted = sorted(simulated, key=lambda x: x.get("date", ""), reverse=True)
    return {"moved": simulated_sorted, "count": len(simulated_sorted)}
