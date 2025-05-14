class GPOParser:
    def __init__(self, gpo_path):
        self.gpo_path = gpo_path

    # Parses GPO export and returns dict with settings and values for file
    def parse_gpo(self) -> dict:
        parsed_gpo = {}
        try:
            with open(self.gpo_path, 'r') as f:
                for eachLine in f.readlines():
                    if " = " in eachLine:
                        formatted = eachLine.strip().split(" = ")
                        parsed_gpo[formatted[0]] = formatted[1]
                return parsed_gpo
        except Exception:
            return {}



