from rocksdict import Rdict
from tkinter import *
from tkinter import ttk 
import constants
import sys
import json

disease_id_start = "Disease::DOID:"

def query1(disease_id):
    with Rdict(constants.ROCKS_DB_PATH) as rocks_db:
        if disease_id not in rocks_db:
            return None
        return rocks_db[disease_id]

def query2():
    with Rdict(constants.ROCKS_DB_PATH) as rocks_db:
        if constants.QUERY2_KEY not in rocks_db:
            return None
        return rocks_db[constants.QUERY2_KEY]

class Client:
    def __init__(self, root):
        self.root = root
        self.root.title("HetioNet")
        self.main_menu()
        self.query1_result = None
    
    # Destroys all widgets currently in the window
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=0)
            self.root.grid_columnconfigure(i, weight=0)
    
    def main_menu(self):
        self.clear_screen()
        ttk.Label(self.root, text="Select a Query").grid(row=0, column=0)
        ttk.Button(self.root, text="Query 1", command=self.query1_screen).grid(row=1, column=0)
        ttk.Button(self.root, text="Query 2", command=self.query2_screen).grid(row=2, column=0)
        self.root.grid_columnconfigure(0, weight=1)
    
    def query1_screen(self):
        self.clear_screen()
        ttk.Button(self.root, text="Back", command=self.main_menu).grid(row=0, column=0, sticky='w')
        ttk.Label(self.root, text=f"Enter Disease ID: {disease_id_start}").grid(row=1, column=0)
        self.query1_input = ttk.Entry(self.root)
        self.query1_input.grid(row=1, column=1)
        ttk.Button(self.root, text="Get", command=self.get_query1_output).grid(row=1, column=2)
    
    def get_query1_output(self):
        if self.query1_result is not None:
            self.query1_result.destroy()
        if self.query1_input is None or self.query1_input.get() is None:
            return
        disease_id = f"{disease_id_start}{self.query1_input.get()}"
        
        query_result = query1(disease_id)
        if query_result is None:
            self.query1_result = ttk.Label(self.root, text=f"Id not found")
            self.query1_result.grid(row=2, column=0, sticky='w')
            return
        self.query1_result = ttk.Frame(self.root)
        self.query1_result.grid(row=2, column=0, sticky='w')
        ttk.Label(self.query1_result, text=disease_id).grid(row=0, column=0, sticky='w')
        ttk.Label(self.query1_result, text=query_result["name"]).grid(row=1, column=0, sticky='w')

        ttk.Label(self.query1_result, text="drugs").grid(row=2, column=0, sticky='w')
        drug_l = Listbox(self.query1_result, height=4)
        drug_l.grid(row=3, column=0, sticky='nwes')
        drug_ls = ttk.Scrollbar(self.query1_result, orient='vertical', command=drug_l.yview)
        drug_ls.grid(row=3, column=1, sticky='ns')
        drug_l['yscrollcommand'] = drug_ls.set
        for compound_name in query_result["drugs"]:
            drug_l.insert('end', compound_name)

        ttk.Label(self.query1_result, text="genes").grid(row=4, column=0, sticky='w')
        gene_l = Listbox(self.query1_result, height=4)
        gene_l.grid(row=5, column=0, sticky='nwes')
        gene_ls = ttk.Scrollbar(self.query1_result, orient='vertical', command=gene_l.yview)
        gene_ls.grid(row=5, column=1, sticky='ns')
        gene_l['yscrollcommand'] = gene_ls.set
        for gene in query_result["genes"]:
            gene_l.insert('end', gene)

        ttk.Label(self.query1_result, text="locations").grid(row=6, column=0, sticky='w')
        location_l = Listbox(self.query1_result, height=4)
        location_l.grid(row=7, column=0, sticky='nwes')
        location_ls = ttk.Scrollbar(self.query1_result, orient='vertical', command=location_l.yview)
        location_ls.grid(row=7, column=1, sticky='ns')
        location_l['yscrollcommand'] = location_ls.set
        for location in query_result["locations"]:
            location_l.insert('end', location)
    
    def query2_screen(self):
        self.clear_screen()
        ttk.Button(self.root, text="Back", command=self.main_menu).grid(row=0, column=0, sticky='w')
        ttk.Label(self.root, text="Query 2 Result").grid(row=1, column=0, sticky='w')
        query2_result = query2()
        if query2_result is None:
            ttk.Label(self.root, text="Couldn't find compounds").grid(row=2, column=0, sticky='w')
            return
        
        ttk.Label(self.root, text="Compound\tDisease").grid(row=2, column=0, sticky='w')
        l = Listbox(self.root)
        s = ttk.Scrollbar(self.root, orient='vertical', command=l.yview)
        l['yscrollcommand'] = s.set 
        for compound_name, _, disease_name, _  in query2_result:
            l.insert('end', f"{compound_name}\t{disease_name}")
        l.grid(row=3, column=0, sticky='nsew')
        s.grid(row=3, column=1, sticky='ns')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

def open_gui():
    root = Tk()
    root.geometry("600x400")
    Client(root)
    root.mainloop()
    
def open_cli():
    while True:
        print("\nHetioNet Project")
        print("1. Run Query 1")
        print("2. Run Query 2")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            disease_id = input(f"Enter disease id: {disease_id_start}").strip()
            try:
                result = query1(f"{disease_id_start}{disease_id}")
                if result is None:
                    print("Disease id not found.")
                else:
                    print(json.dumps(result, indent=4))
            except Exception as e:
                print("Error:", e)
        elif choice == "2":
            try:
                result = query2()
                if result is None:
                    print("Query result not found.")
                else:
                    print(result)
            except Exception as e:
                print("Error:", e)
        elif choice == "3":
            print("Exit")
            break
        else:
            print("Try again")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        open_cli()
    else:
        open_gui()