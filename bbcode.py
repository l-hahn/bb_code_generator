from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext

class BbCodeGenerator:
    default_keys = ("title", "image", "link", "code", "description")
    check_keys = ('b','i','u','s')
    type_values = ("text", "image", "url", "code")
    default_font_type = "Comic Sans MS"

    def entry_to_bbcode(entry):
        args = [] if entry['key'] not in ('description') else ['1.0', END]
        content = entry['content'].get(*args).rstrip("\r\n")
        if not content:
            return None
        type = entry['type'].get()
        if type == "image":
            content = f"[img]{content}[/img]"
            label = entry['label'].get()
            if label:
                content = f"{label}: {content}"
            return content
        if type == "url":
            label = entry['label'].get()
            if not label:
                content = f"[url]{content}[/url]"
            else:
                content = f"[url=\"{content}\"]{label}[/url]"
        if type == "code":
            content = f"[code]{content}[/code]"

        size = entry['size'].get()
        content = f"[size=\"{size}\"]{content}[/size]"

        for key in BbCodeGenerator.check_keys:
            check = entry['checks'][key][1].get()
            if check:
                content = f"[{key}]{content}[/{key}]"

        if entry['key'] == "title":
            content = f"[center]{content}[/center]"
        elif entry['key'] == "link":
            label = entry['label'].get()
            if not label:
                content = f"Link: {content}"
        else:
            label = entry['label'].get()
            if label:
                content = f"{label}: {content}"
        return content

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

        self._text_box_desc = scrolledtext.ScrolledText(self._window, width=73, height=10)
        self._text_box_bbcode = scrolledtext.ScrolledText(self._window, width=73, height=10)
        self._text_box_bbcode.config(state="disabled")

    def _make_default_entry(self, key):
        bools = [
            BooleanVar()
            for key in BbCodeGenerator.check_keys
        ]
        entry = {
            'key' : key,
            'key_label': Label(self._window, text=key, font=(BbCodeGenerator.default_font_type, 10)),
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

        if key == "description":
            del entry['content']
            entry['content'] = self._text_box_desc
            entry['label'].insert(0, key.title())
        if key in BbCodeGenerator.default_keys:
            if key == "image":
                entry['type'].set("image")
            else:
                entry['checks']['b'][1].set(True)
                entry['size'].set(6)
            if key == "link":
                entry['label'].insert(0, key.title())
                entry['type'].set("url")
            if key == "code":
                entry['label'].insert(0, key.title())
                entry['type'].set("code")

        if key == "title":
            del entry['label']
            entry['label'] = Label(self._window, text=key.title(), font=(BbCodeGenerator.default_font_type, 10))

        return entry

    def _make_empty_entry(self, key):
        bools = [
            BooleanVar()
            for key in BbCodeGenerator.check_keys
        ]
        entry = {
            'key': key,
            'key_label': Label(self._window, text=key, font=(BbCodeGenerator.default_font_type, 10)),
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
        entry['key_label'].grid(row=self._last_row, column=0)
        entry['label'].grid(row=self._last_row, column=1)
        entry['type'].grid(row=self._last_row, column=2)
        entry['size'].grid(row=self._last_row, column=3)
        for idx,box in enumerate(entry['checks'].values()):
            box[0].grid(row=self._last_row, column=idx+4)
        entry['content'].grid(row=self._last_row, column=len(entry['checks'])+4)

    def _default_window(self):
        self._header_labels = [
            Label(self._window, text = label_text, font=(BbCodeGenerator.default_font_type, 12))
            for label_text in ("key", "label", "type", "size", "B", "I", "U", "S", "content")
        ]
        for idx,label in enumerate(self._header_labels):
            label.grid(row=self._last_row, column=idx)
        self._last_row += 1

        for idx,entry in enumerate(BbCodeGenerator.default_keys):
            self._default_entries[entry] = self._make_default_entry(entry)
            if entry == "description":
                continue
            self._place_entry(self._default_entries[entry])
            self._last_row +=1

        self._update_textbox_positions()
        self._last_row +=1
        self._update_button_position()

    def _update_textbox_positions(self):
        self._place_entry(self._default_entries['description'])
        self._last_row +=1
        self._text_box_bbcode.grid(row=self._last_row, column=len(self._default_entries['description']['checks'])+4)

    def _update_button_position(self):
        self._button_add_entries.grid(column=0, row=self._last_row)
        self._button_render.grid(column=len(self._header_labels), row=self._last_row)


    def _update_additional_entries(self):
        new_key = f'key_{len(self._additional_entries)}'

        self._additional_entries[new_key] = self._make_empty_entry(new_key)
        self._place_entry(self._additional_entries[new_key])
        self._last_row += 1

        self._update_textbox_positions()
        self._last_row +=1

        self._update_button_position()

    def _generate_bbc(self):
        bbcode = [
            BbCodeGenerator.entry_to_bbcode(self._default_entries[entry])
            for entry in self._default_entries
            if entry != "description"
        ]
        
        bbcode.extend([
            BbCodeGenerator.entry_to_bbcode(self._additional_entries[entry])
            for entry in self._additional_entries
        ])
        
        bbcode.append(BbCodeGenerator.entry_to_bbcode(self._default_entries['description']))
        

        filtered_bbcode = [
            code
            for code in bbcode
            if code is not None
        ]
        bbcodetext = "\n".join(filtered_bbcode)
        self._text_box_bbcode.config(state="normal")
        self._text_box_bbcode.delete('1.0', END)
        self._text_box_bbcode.insert("1.0", bbcodetext)
        self._text_box_bbcode.config(state="disabled")

    def start(self):
        self._default_window()
        self._window.mainloop()

if __name__ == "__main__":
    app = BbCodeGenerator()
    app.start()
