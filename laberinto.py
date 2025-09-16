import tkinter as tk
import time
from collections import deque

LAB_SIZE = 15
CELL_SIZE = 30
VELOCIDAD = 0.3  # segundos por movimiento

inicio = (0, 0)
fin = (14, 14)

# -----------------------------
# CREAR LABERINTO CON HUECOS INTERCALADOS
# -----------------------------
laberinto = [[0 for _ in range(LAB_SIZE)] for _ in range(LAB_SIZE)]
for idx, col in enumerate(range(2, LAB_SIZE, 3)):
    for fila in range(LAB_SIZE):
        laberinto[fila][col] = 1  # muro completo
    # hueco intercalado: primero abajo, segundo arriba, etc.
    if idx % 2 == 0:
        laberinto[LAB_SIZE-1][col] = 0  # hueco abajo
    else:
        laberinto[0][col] = 0  # hueco arriba

# -----------------------------
# TKINTER
# -----------------------------
root = tk.Tk()
root.title("Laberinto BFS/DFS Casilla por Casilla")

canvas_laberinto = tk.Canvas(root, width=LAB_SIZE*CELL_SIZE, height=LAB_SIZE*CELL_SIZE, bg="white")
canvas_laberinto.grid(row=0, column=0)

canvas_visitados = tk.Canvas(root, width=LAB_SIZE*CELL_SIZE, height=LAB_SIZE*CELL_SIZE, bg="white")
canvas_visitados.grid(row=0, column=1)

algoritmo_var = tk.StringVar(value="BFS")
frame_controles = tk.Frame(root)
frame_controles.grid(row=1, column=0, columnspan=2, pady=10)
tk.Label(frame_controles, text="Selecciona algoritmo:").pack(side="left")
tk.Radiobutton(frame_controles, text="BFS", variable=algoritmo_var, value="BFS").pack(side="left")
tk.Radiobutton(frame_controles, text="DFS", variable=algoritmo_var, value="DFS").pack(side="left")
tk.Button(frame_controles, text="Iniciar", command=lambda: ejecutar()).pack(side="left", padx=10)

# -----------------------------
# FUNCIONES
# -----------------------------
def dibujar_tablero(canvas, data):
    canvas.delete("all")
    for i in range(LAB_SIZE):
        for j in range(LAB_SIZE):
            x1, y1 = j*CELL_SIZE, i*CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            color = "black" if data[i][j]==1 else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
    # inicio y fin
    canvas.create_rectangle(inicio[1]*CELL_SIZE, inicio[0]*CELL_SIZE,
                            inicio[1]*CELL_SIZE+CELL_SIZE, inicio[0]*CELL_SIZE+CELL_SIZE, fill="green")
    canvas.create_rectangle(fin[1]*CELL_SIZE, fin[0]*CELL_SIZE,
                            fin[1]*CELL_SIZE+CELL_SIZE, fin[0]*CELL_SIZE+CELL_SIZE, fill="red")

def crear_punto(canvas, pos, color="blue"):
    x1, y1 = pos[1]*CELL_SIZE, pos[0]*CELL_SIZE
    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
    return canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color)

def mover_punto(canvas, punto, pos):
    x1, y1 = pos[1]*CELL_SIZE, pos[0]*CELL_SIZE
    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
    canvas.coords(punto, x1+5, y1+5, x2-5, y2-5)

# BFS paso a paso
def bfs_casilla_por_casilla():
    queue = deque([inicio])
    visitados = set([inicio])
    padres = {inicio: None}

    while queue:
        actual = queue.popleft()
        yield actual, padres
        if actual == fin:
            return  # termina al encontrar el fin
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nx, ny = actual[0]+dx, actual[1]+dy
            vecino = (nx, ny)
            if 0<=nx<LAB_SIZE and 0<=ny<LAB_SIZE and laberinto[nx][ny]==0 and vecino not in visitados:
                queue.append(vecino)
                visitados.add(vecino)
                padres[vecino] = actual

# DFS paso a paso
def dfs_casilla_por_casilla():
    stack = [inicio]
    visitados = set([inicio])
    padres = {inicio: None}

    while stack:
        actual = stack.pop()
        yield actual, padres
        if actual == fin:
            return  # termina al encontrar el fin
        vecinos = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nx, ny = actual[0]+dx, actual[1]+dy
            vecino = (nx, ny)
            if 0<=nx<LAB_SIZE and 0<=ny<LAB_SIZE and laberinto[nx][ny]==0 and vecino not in visitados:
                vecinos.append(vecino)
        vecinos.reverse()  # para DFS
        for vecino in vecinos:
            stack.append(vecino)
            visitados.add(vecino)
            padres[vecino] = actual

# Ejecutar animación
def ejecutar():
    dibujar_tablero(canvas_laberinto, laberinto)
    dibujar_tablero(canvas_visitados, [[0]*LAB_SIZE for _ in range(LAB_SIZE)])
    player = crear_punto(canvas_laberinto, inicio, "blue")

    gen = bfs_casilla_por_casilla() if algoritmo_var.get()=="BFS" else dfs_casilla_por_casilla()

    try:
        for pos, padres in gen:
            mover_punto(canvas_laberinto, player, pos)
            crear_punto(canvas_visitados, pos, "orange")
            root.update()
            time.sleep(VELOCIDAD)
    except StopIteration:
        pass

    # Terminar el programa al finalizar
    root.destroy()

# -----------------------------
# INICIALIZAR
# -----------------------------
dibujar_tablero(canvas_laberinto, laberinto)
dibujar_tablero(canvas_visitados, [[0]*LAB_SIZE for _ in range(LAB_SIZE)])
root.mainloop()
