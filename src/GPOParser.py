class GPOParser:
    def __init__(self, gpo_path):
        self.gpo_path = gpo_path

    def parse(self):
        gpo_set_and_val = {}
        try:
            with open(self.gpo_path, 'r') as f:
                for eachLine in f.readlines():
                    if " = " in eachLine:
                        formatted = eachLine.strip().split(" = ")
                        gpo_set_and_val[formatted[0]] = formatted[1]
                        return gpo_set_and_val
        except Exception as e:
            return f"[!] ERROR: Unable to read GPO file. Exception: {e}"


