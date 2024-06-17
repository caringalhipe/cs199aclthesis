import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
from random import shuffle
from algo3_1 import k_poset_cover
from algo3_3 import exact_k_poset_cover

#import algo3 and kposet functions

# Checks if two linear orders have an adjacent swap
def check_swap(str1, str2):
      for i in range(len(str1)-1):
            if str1[i] == str2[i+1] and str1[i+1] == str2[i]:
                  if str1[0:i] + str1[i+2:] != str2[0:i] + str2[i+2:]:
                        return None
                  return f"{str(min(int(str1[i]), int(str2[i])))}, {str(max(int(str1[i]), int(str2[i])))}"
      return None

# Process input to create a graph and generate a figure
def process_input(data, poset = [], node_color = 'pink', edge_color = 'k'):
    global G
    
    num_orders = len(data)

    G = nx.Graph()

    #Add an edge between each node that has an adjacent swap
    for i in range(num_orders):
        G.add_node(data[i])
        for j in range(i+1, num_orders):
                adjacent = check_swap(data[i], data[j])
                if adjacent:
                    if data[i] in poset and data[j] in poset:
                            G.add_edge(data[i], data[j], label=adjacent, color = edge_color)
                    else:
                            G.add_edge(data[i], data[j], label=adjacent, color = 'k')

    #Determines the layout of the graph
    pos = nx.kamada_kawai_layout(G)

    #Color nodes
    color_map = []
    for node in G:
            if node in poset:
                  color_map.append(node_color)
            else:
                  color_map.append('pink')

    #Draw and show graph with labels on nodes and edges
    fig, ax = plt.subplots()      
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color=color_map, edge_color = nx.get_edge_attributes(G,'color').values())
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

    return fig

# Load data from file
def load_from_file():
    global data
    
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read().strip().split("\n")
            for i in range(len(data)):
                input_textbox.insert(tk.INSERT, data[i] + '\n')
            display_graph(data)

# Submit input from textbox
def submit_input(optimal):
    global data, k, right_frame, right_text
    right_text.delete('1.0', tk.END)
    data = input_textbox.get("1.0", tk.END).strip().split("\n")
    k = k_textbox.get("1.0", tk.END).strip()
    display_graph(data)
    if has_submitted:
        for widget in right_frame.winfo_children():
            widget.destroy()
        right_frame = tk.Frame(main_frame, bg="darkgray")
        right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        right_text = tk.Text(right_frame, height=20, width=25, bg="darkgray", fg="black")
        right_text.pack(pady=10)
    ### ALGO WILL RUN WHEN SUBMIT BUTTON IS PRESSED ###
    if len(data) > 0 and k.isnumeric() and int(k) > 0:
        
        if optimal:
            output = exact_k_poset_cover(data, k, G)
        else:
            output = k_poset_cover(data, k, G)
        print(output)
        
        if output:
            posets, linear_orders = output
            
            right_text.insert(tk.END, f"{len(linear_orders)} posets found for the input:\n")
            for k in range(len(posets)):
                right_text.insert(tk.END, f"P{k+1}: {posets[k]}\n")
            
            colors = ['r', 'g', 'b', 'c','m','y']

            for k in range(len(linear_orders)):
                highlight_button = tk.Button(right_frame, text=f"Show P{k+1}", command=lambda k=k: highlight_graph(data, linear_orders[k], colors[k % len(colors)]))
                highlight_button.pack(pady=3)
        else:
            right_text.insert(tk.END, f"No k={k} posets found for the input")
    else:
        messagebox.showerror('Invalid input', 'Please enter a valid value of k')

# Display graph based on input data
def display_graph(data):
    global canvas, has_submitted

    # Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()
        
    has_submitted = 1

    fig = process_input(data)
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
def redraw_graph():
    global canvas, data

    # Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()
        
    copy = data
    shuffle(copy)
    data = copy

    fig = process_input(data)
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
def highlight_graph(data, poset, poset_color):
    global canvas

    # Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    fig = process_input(data, poset, poset_color, poset_color)
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the GUI
def create_gui():
    global input_textbox, plot_frame, k_textbox, right_frame, right_text, main_frame

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
    plot_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    # Create right column frame for text display
    right_frame = tk.Frame(main_frame, bg="darkgray")
    right_frame.grid(row=0, column=2, sticky="nsew", padx=3, pady=3)
    right_text = tk.Text(right_frame, height=20, width=25, bg="darkgray", fg="black")
    right_text.pack(pady=3)

    # Configure grid weights
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=3)
    main_frame.columnconfigure(2, weight=1)
    main_frame.rowconfigure(0, weight=1)

    # Add Load from File button to left frame
    file_button = tk.Button(left_frame, text="Load from File", command=load_from_file)
    file_button.pack(pady=10)

    # Add input textbox to left frame
    input_label = tk.Label(left_frame, text = "Input Linear Orders:")
    input_label.pack(pady=10)
    input_textbox = tk.Text(left_frame, height=10, width=50)
    input_textbox.pack(pady=10)
    
    # Add k textbox to left frame
    k_label = tk.Label(left_frame, text = "Input k:")
    k_label.pack(pady=10)
    k_textbox = tk.Text(left_frame, height=1, width=2)
    k_textbox.pack(pady=10)

    # Add Submit button to left frame
    submit_button = tk.Button(left_frame, text="Submit", command=lambda optimal=0: submit_input(optimal))
    submit_button.pack(pady=10)
    
    # Add Submit button for optimal to left frame
    submit_button = tk.Button(left_frame, text="Find Optimal", command=lambda optimal=1:submit_input(optimal))
    submit_button.pack(pady=10)
    
    redraw_button = tk.Button(master=left_frame, text="Redraw Graph", command=redraw_graph)
    redraw_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()