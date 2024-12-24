import matplotlib.pyplot as plt

# Fungsi Uniform Cost Search tanpa heapq dan networkx
def uniform_cost_search(graph, start, goal):
    frontier = [(0, start, [])]  # (biaya, node, jalur)
    explored = set()  # Set untuk menyimpan node yang sudah dikunjungi

    while frontier:
        frontier.sort(key=lambda x: x[0])  # Mengurutkan frontier berdasarkan biaya
        cost, current_node, path = frontier.pop(0)  # Mengambil node dengan biaya terendah
        
        if current_node == goal:
            return path + [current_node], cost

        if current_node not in explored:
            explored.add(current_node)
            path = path + [current_node]
            
            for neighbor, edge_cost in graph[current_node].items():
                if neighbor not in explored:
                    total_cost = cost + edge_cost['cost']
                    frontier.append((total_cost, neighbor, path))

    return None, float('inf')  # Jika tidak ada jalur yang ditemukan

# Fungsi untuk mencari goal terdekat dari node start
def find_closest_goal(graph, start, parkiran):
    closest_goal = None
    min_cost = float('inf')
    closest_path = None

    for red_node in parkiran:
        path, cost = uniform_cost_search(graph, start, red_node)
        if path and cost < min_cost:
            closest_goal = red_node
            min_cost = cost
            closest_path = path

    return closest_goal, closest_path, min_cost

# Membuat graf menggunakan dictionary
graph = {
    '1': {'A': {'cost': 8}, 'E': {'cost': 6}},
    '2': {'A': {'cost': 10}, 'K': {'cost': 5}},
    '3': {'I': {'cost': 8}, 'C': {'cost': 15}},
    '4': {'E': {'cost': 10}, 'H': {'cost': 5}},
    '5': {'J': {'cost': 6}, 'K': {'cost': 7}},
    'A': {'1': {'cost': 8}, '2': {'cost': 10}, 'C': {'cost': 3}},
    'B': {'C': {'cost': 2}, 'G': {'cost': 1}},
    'C': {'A': {'cost': 3}, 'B': {'cost': 2}, 'D': {'cost': 1}, '3': {'cost': 15}},
    'D': {'C': {'cost': 1}, 'F': {'cost': 2}},
    'E': {'1': {'cost': 6}, '4': {'cost': 10}, 'F': {'cost': 2}},
    'F': {'D': {'cost': 2}, 'E': {'cost': 2}},
    'G': {'B': {'cost': 1}, 'K': {'cost': 2}},
    'H': {'4': {'cost': 5}, 'I': {'cost': 2}},
    'I': {'H': {'cost': 2}, '3': {'cost': 8}, 'J': {'cost': 2}},
    'J': {'I': {'cost': 2}, '5': {'cost': 6}},
    'K': {'2': {'cost': 5}, 'G': {'cost': 2}, '5': {'cost': 7}}
}

# Node yang diwarnai merah
parkiran = {'1', '2', '3', '4', '5'}

# Meminta input dari pengguna untuk menentukan start
start = input("Masukkan lokasi gedung anda (A-K): ").upper()

# Mencari goal terdekat dari node start
goal, path, total_cost = find_closest_goal(graph, start, parkiran)

# Output hasil UCS
if path:
    print(f"Parkiran terdekat adalah parkiran {goal}")
    print(f"Jalur yang ditemukan: {' -> '.join(path)}")
    print(f"Total cost: {total_cost}")
else:
    print("Tidak ada jalur yang ditemukan.")

# --- Kode untuk menampilkan graf secara manual ---

# Posisi node yang ditentukan secara manual
node_positions = {
    '1': (0, 1),
    '2': (2, 1),
    '3': (1, -1),
    '4': (-1, -2),
    '5': (3, -2),
    'A': (1, 1),
    'B': (2, 0),
    'C': (1, 0),
    'D': (0, 0),
    'E': (-1, -1),
    'F': (0, -1),
    'G': (2, -1),
    'H': (0, -2),
    'I': (1, -2),
    'J': (2, -2),
    'K': (3, -1)
}

# Menggambar graf menggunakan matplotlib
plt.figure(figsize=(6, 6))

# Menggambar node
for node, (x, y) in node_positions.items():
    # Tentukan warna node
    if node == start:
        color = 'yellow'  # Warna khusus untuk node start
    elif node == goal:
        color = 'red'  # Warna khusus untuk node goal
    else:
        color = 'lightgreen' if node in parkiran else 'lightblue'
    plt.scatter(x, y, s=1000, c=color)  # Menggambar node
    plt.text(x, y, node, fontsize=12, ha='center', va='center', fontweight='bold')  # Menambahkan label node

# Menggambar edge dan menambahkan label biaya
for node1, neighbors in graph.items():
    for node2, edge_data in neighbors.items():
        x1, y1 = node_positions[node1]
        x2, y2 = node_positions[node2]
        
        # Menggambar garis untuk setiap edge
        plt.plot([x1, x2], [y1, y2], 'gray', zorder=1)
        
        # Menambahkan label biaya di tengah-tengah edge
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        cost = edge_data['cost']
        plt.text(mid_x, mid_y, str(cost), fontsize=12, ha='center', va='center', color='red')

# Menampilkan graf
plt.title(f"Lokasi Parkir Terdekat dari gedung {start} adalah parkiran{goal}")
plt.axis('off')  # Menghapus sumbu
plt.show()
