import os


class Updater:
    MARKDOWN_FORMAT = ".md"

    def __init__(self):
        self.text = ""
    
    def make_text(self, d, cur_dir):
        for path in sorted(os.listdir(cur_dir)):
            if path == ".git":
                continue
            if os.path.isdir(new_path:="{}/{}".format(cur_dir, path)):
                if new_path.count(".") > 1:
                    continue
                self.text += "{} {}\n".format("#"*d, path)
                self.make_text(d+1, new_path)
            else:
                if os.path.splitext(new_path)[-1] == self.MARKDOWN_FORMAT:
                    self.text += "{} {}\n".format("#"*(d),os.path.splitext(new_path)[0].split("/")[-1])
                    with open(new_path, "r", encoding="utf8") as f:
                        for line in f.readlines():
                            if line.startswith("# "):
                                self.text += "- {}\n".format(line.replace("# ", ""))
            self.text += "<br/>\n<br/>\n"
            self.text += "\n"
                
    def update(self):
        with open("./README.md", "w", encoding="utf8") as f:
            self.make_text(1, ".")
            f.write(self.text)

    

if __name__ == "__main__":
    updater = Updater()
    updater.update()
