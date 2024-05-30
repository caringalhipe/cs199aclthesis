import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
from random import shuffle

# Checks if two linear orders have an adjacent swap
def check_swap(str1, str2):
    for i in range(len(str1) - 1):
        if str1[i] == str2[i + 1] and str1[i + 1] == str2[i]:
            if str1[0:i] + str1[i + 2:] != str2[0:i] + str2[i + 2:]:
                return None
            return f"{str(min(int(str1[i]), int(str2[i])))}-{str(max(int(str1[i]), int(str2[i])))}"
    return None

# Process input to create a graph and generate a figure
def process_input(data):
    lines = data.strip().split("\n")
    num_orders = int(lines[0])
    inp = lines[1:num_orders + 1]

    G = nx.Graph()

    # Add nodes and edges based on adjacent swaps
    for a in range(num_orders):
        G.add_node(inp[a])
        for b in range(a + 1, num_orders):
            pairs = [inp[a][i:i + 2] for i in range(len(inp[a])) if "".join(reversed(inp[a][i:i + 2])) == "".join(inp[b][i:i + 2]) and inp[a][0:i] + inp[a][i + 2:] == inp[b][0:i] + inp[b][i + 2:]]
            if len(pairs) > 0:
                G.add_edge(inp[a], inp[b], label=str(sorted([pairs[0][0], pairs[0][1]])))

    pos = nx.kamada_kawai_layout(G)
    color_map = ['pink' for node in G]

    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color=color_map, node_shape='s', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'), ax=ax)

    return fig

# Load data from file
def load_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
            display_graph(data)

# Submit input from textbox
def submit_input():
    data = input_textbox.get("1.0", tk.END)
    display_graph(data)

# Display graph based on input data
def display_graph(data):
    global canvas

    # Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    fig = process_input(data)
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the GUI
def create_gui():
    global input_textbox, plot_frame

    root = tk.Tk()
    root.title("Poset Visualizer")

    # Create banner
    banner = tk.Frame(root, bg="blue")
    banner.pack(fill=tk.X)
    banner_label = tk.Label(banner, text="Poset Visualizer", bg="blue", fg="white", font=("Arial", 24))
    banner_label.pack(pady=10)

    # Create main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create left column frame
    left_frame = tk.Frame(main_frame)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Create plot frame for middle column
    plot_frame = tk.Frame(main_frame)
    plot_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Create right column frame for text display
    right_frame = tk.Frame(main_frame, bg="darkgray")
    right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    right_text = tk.Text(right_frame, height=30, width=20, bg="darkgray", fg="white")
    right_text.pack(pady=10)

    # Configure grid weights
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=3)
    main_frame.columnconfigure(2, weight=1)
    main_frame.rowconfigure(0, weight=1)

    # Add Load from File button to left frame
    file_button = tk.Button(left_frame, text="Load from File", command=load_from_file)
    file_button.pack(pady=10)

    # Add input textbox to left frame
    input_textbox = tk.Text(left_frame, height=10, width=50)
    input_textbox.pack(pady=10)

    # Add Submit button to left frame
    submit_button = tk.Button(left_frame, text="Submit", command=submit_input)
    submit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
