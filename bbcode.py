from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext

class BbCodeGenerator:
    default_keys = ("Title", "Image", "Link", "Code", "Description")
    check_keys = ('b','i','u','s')
    type_values = ("text", "image", "url", "code")
    default_font_type = "Comic Sans MS"

    def __init__(self, heading="BB-Code Generator"):
        self._window = Tk()
        self._window.title(heading)
        self._last_row = 0

        self._default_entries = {}
        self._additional_entries = {}

        self._button_add_entries = Button(
            self._window, text="Add empty entry", command=self._update_additional_entries
        )
        self._button_render = Button(
            self._window, text="Generate BBC...", command=self._generate_bbc
        )

    def _make_default_entry(self, name):
        bools = [
            BooleanVar()
            for key in BbCodeGenerator.check_keys
        ]
        entry = {
            'label': Label(self._window, text=name, font=(BbCodeGenerator.default_font_type, 10)),
            'type': Combobox(self._window, values=BbCodeGenerator.type_values, width=6),
            'size': Combobox(self._window, values=list(range(1,101)), width=2),
            'checks' : {
                tag: (Checkbutton(self._window, var=bools[idx]), bools[idx])
                for idx,tag in enumerate(BbCodeGenerator.check_keys)
            },
            'content': Entry(self._window, width=100)
        }

        entry['type'].set("text")
        if name == "Description":
            del entry['content']
            entry['content'] = scrolledtext.ScrolledText(self._window, width=70, height=5)

        if name in BbCodeGenerator.default_keys:
            if name == "Image":
                entry['type'].set("image")
            else:
                entry['checks']['b'][1].set(True)
                entry['size'].set(6)
            if name == "Link":
                entry['type'].set("url")
            if name == "Code":
                entry['type'].set("code")

        return entry

    def _make_empty_entry(self):
        bools = [
            BooleanVar()
            for key in BbCodeGenerator.check_keys
        ]
        entry = {
            'label': Entry(self._window, width=15),
            'type': Combobox(self._window, values=BbCodeGenerator.type_values, width=6),
            'size': Combobox(self._window, values=list(range(1,101)), width=2),
            'checks' : {
                tag: (Checkbutton(self._window, var=bools[idx]), bools[idx])
                for idx,tag in enumerate(BbCodeGenerator.check_keys)
            },
            'content': Entry(self._window, width=100)
        }
        entry['type'].set("text")
        entry['size'].set(6)

        return entry

    def _place_entry(self, entry):
        entry['label'].grid(row=self._last_row, column=0)
        entry['type'].grid(row=self._last_row, column=1)
        entry['size'].grid(row=self._last_row, column=2)
        for idx,box in enumerate(entry['checks'].values()):
            box[0].grid(row=self._last_row, column=idx+3)
        entry['content'].grid(row=self._last_row, column=len(entry['checks'])+3)

    def _default_window(self):
        self._header_labels = [
            Label(self._window, text = label_text, font=(BbCodeGenerator.default_font_type, 12))
            for label_text in ("key", "type", "size", "B", "I", "U", "S", "content")
        ]
        for idx,label in enumerate(self._header_labels):
            label.grid(row=self._last_row, column=idx)
        self._last_row += 1

        for idx,entry in enumerate(BbCodeGenerator.default_keys):
            self._default_entries[entry] = self._make_default_entry(entry)
            self._place_entry(self._default_entries[entry])
            self._last_row +=1
        
        #some space ;)
        spacer = Label(self._window)
        spacer.grid(row=self._last_row, column=0)
        self._last_row +=1
        
        self._update_additional_entries()
        self._update_button_position()


    def _update_button_position(self):
        self._button_add_entries.grid(column=0, row=self._last_row)
        self._button_render.grid(column=len(self._header_labels), row=self._last_row)


    def _update_additional_entries(self):
        new_key = f'key_{len(self._additional_entries)}'

        self._additional_entries[new_key] = self._make_empty_entry()
        self._place_entry(self._additional_entries[new_key])
        self._last_row += 1

        self._update_button_position()

    def _generate_bbc(self):
        print(self._default_entries)
        print(self._additional_entries)

    def start(self):
        self._default_window()
        self._window.mainloop()

if __name__ == "__main__":
    app = BbCodeGenerator()
    app.start()
