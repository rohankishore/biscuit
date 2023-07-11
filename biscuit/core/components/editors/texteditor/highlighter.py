import os, tkinter as tk
from pygments import lex
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound


class Highlighter:
    def __init__(self, master, *args, **kwargs):
        self.text = master
        self.base = master.base

        try:
            self.lexer = get_lexer_for_filename(os.path.basename(master.path), inencoding=master.encoding, encoding=master.encoding)
        except ClassNotFound:
            self.lexer = None

        self.tag_colors = self.base.theme.syntax
        self.setup_highlight_tags()

    def setup_highlight_tags(self):
        for token, color in self.tag_colors.items():
            self.text.tag_configure(str(token), foreground=color)

    def highlight(self):
        if not self.lexer:
            return
        
        for token, _ in self.tag_colors.items():
            self.text.tag_remove(str(token), '1.0', tk.END)
            
        text = self.text.get_all_text()
        self.text.mark_set("range_start", "1.0")
        for token, content in lex(text, self.lexer):
            self.text.mark_set("range_end", f"range_start + {len(content)}c")
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")
            
            # DEBUG
            # print(f"{content} is recognized as a <{str(token)}>")
        # print("==================================")
