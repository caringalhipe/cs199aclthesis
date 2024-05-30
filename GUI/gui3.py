import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt

def check_swap(str1, str2):
    for i in range(len(str1) - 1):
        if str1[i] == str2[i+1] and str1[i+1] == str2[i]:
            if str1[i+2:] != str2[i+2:]:
                return None
            return f"{str(min(int(str1[i]), int(str2[i])))}-{str(max(int(str1[i]), int(str2[i])))}"
    return None

def process_input(data):
    lines = data.strip().split("\n")
    num_orders = int(lines[0])
    inp = lines[1:num_orders + 1]
    
    G = nx.Graph()
    G.add_nodes_from(inp)

    for i in range(len(inp)-1):
        for j in range(i+1, len(inp)):
            adjacent = check_swap(inp[i], inp[j])
            if adjacent:
                G.add_edge(inp[i], inp[j], label=adjacent)

    pos = nx.kamada_kawai_layout(G)
    color_map = ['pink' for node in G]

    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color=color_map, node_shape='s', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'), ax=ax)
    
    return fig

def load_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
            display_graph(data)

def submit_input():
    data = input_textbox.get("1.0", tk.END)
    display_graph(data)

def display_graph(data):
    global canvas

    # Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    fig = process_input(data)
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def create_gui():
    global input_textbox, plot_frame
    
    root = tk.Tk()
    root.title("Linear Orders Graph")
    
    # Create a main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create left column frame
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    
    # Create right column frame for plot
    plot_frame = tk.Frame(main_frame)
    plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
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
