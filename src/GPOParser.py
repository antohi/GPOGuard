class GPOParser:

    # Parses GPO export and returns dict with settings and values for file
    @staticmethod
    def parse_gpo(gpo_path) -> dict:
        parsed_gpo = {}
        try:
            with open(gpo_path, 'r') as f:
                for eachLine in f.readlines():
                    if "=" in eachLine:
                        key, value = map(str.strip, eachLine.strip().split("=", 1))
                        parsed_gpo[key] = value
                return parsed_gpo
        except Exception:
            return {}



