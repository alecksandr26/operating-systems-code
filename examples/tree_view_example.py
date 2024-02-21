import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Treeview Example")

# Create a Treeview widget
tree = ttk.Treeview(root)

# Insert some sample data
tree.insert("", "end", text="Parent 1")
tree.insert("", "end", text="Parent 2")

# Function to iterate over all parent elements
def iterate_parents():
    print(tree.get_children(""))
    for parent_id in tree.get_children(""):  # Get top-level items (parents)
        print("Parent:", parent_id)

# Button to trigger the iteration
button = tk.Button(root, text="Iterate Parents", command=iterate_parents)
button.pack()

# Pack the Treeview widget
tree.pack(expand=True, fill="both")

# Run the Tkinter event loop
root.mainloop()

# Output:
# ('I001', 'I002')
# Parent: I001
# Parent: I002
