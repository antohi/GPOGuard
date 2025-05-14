class GPOParser:


    # Parses GPO export and returns dict with settings and values for file
    @staticmethod
    def parse_gpo(gpo_path) -> dict:
        parsed_gpo = {}
        try:
            with open(gpo_path, 'r') as f:
                for eachLine in f.readlines():
                    if " = " in eachLine:
                        formatted = eachLine.strip().split(" = ")
                        parsed_gpo[formatted[0]] = formatted[1]
                return parsed_gpo
        except Exception:
            return {}



