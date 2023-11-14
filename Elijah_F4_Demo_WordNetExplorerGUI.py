import tkinter as tk
from tkinter import ttk
from nltk.corpus import wordnet as wn


class WordnetExplorer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("WordNet Explorer")
        self.geometry("800x800")

        self.word_entry = ttk.Entry(self)
        self.word_entry.pack(pady=20)

        self.search_button = ttk.Button(self, text="Search", command=self.search_word)
        self.search_button.pack(pady=20)

        self.tree = ttk.Treeview(self)
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=False)
        self.tree.heading("#0", text="Hypernyms", anchor=tk.W)
        self.tree["columns"] = ("POS", "Definition")
        self.tree.column("#0", width=200)
        self.tree.column("POS", width=50)
        self.tree.column("Definition", width=500)
        self.tree.heading("POS", text="POS")
        self.tree.heading("Definition", text="Definition")

        self.antonyms_tree = ttk.Treeview(self)
        self.antonyms_tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=False)
        self.antonyms_tree.heading("#0", text="Antonyms", anchor=tk.W)
        self.antonyms_tree["columns"] = ("POS", "Definition")
        self.antonyms_tree.column("#0", width=200)
        self.antonyms_tree.column("POS", width=50)
        self.antonyms_tree.column("Definition", width=500)
        self.antonyms_tree.heading("POS", text="POS")
        self.antonyms_tree.heading("Definition", text="Definition")

    def fetch_hypernyms(self, synset, parent="", level=0):
        name = synset.name().split(".")[0]
        pos = synset.pos()
        definition = synset.definition()
        node_id = self.tree.insert(
            parent, "end", text=" " * level + name, values=(pos, definition)
        )
        hypernyms = synset.hypernyms()

        for hyper in hypernyms:
            self.fetch_hypernyms(hyper, node_id, level + 1)

    def fetch_antonyms(self, synset, parent=""):
        name = synset.name().split(".")[0]
        pos = synset.pos()
        definition = synset.definition()
        node_id = self.antonyms_tree.insert(
            parent, "end", text=name, values=(pos, definition)
        )
        antonyms = synset.lemmas()[0].antonyms()

        for ant in antonyms:
            ant_name = ant.name()
            ant_pos = ant.synset().pos()
            ant_def = ant.synset().definition()
            ant_node_id = self.antonyms_tree.insert(
                node_id, "end", text=ant_name, values=(ant_pos, ant_def)
            )
            ant_hypernyms = ant.synset().hypernyms()
            for hyper in ant_hypernyms:
                self.fetch_hypernyms(hyper, ant_node_id)

    def search_word(self):
        word = self.word_entry.get()
        if not word:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.antonyms_tree.get_children():
            self.antonyms_tree.delete(row)

        synsets = wn.synsets(word)

        for syn in synsets:
            self.fetch_hypernyms(syn)
            self.fetch_antonyms(syn)


app = WordnetExplorer()
app.mainloop()
