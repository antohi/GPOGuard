import csv


class BaselineParser:
    def __init__(self, bl_path, bl_type):
        self.bl_path = bl_path
        self.bl_type = bl_type
    # Parses baseline file and returns it as a dict
    def parse_bl(self) -> dict:
        parsed_bl = {}
        try:
            with open(self.bl_path, mode='r') as b:
                reader = csv.DictReader(b)
                for row in reader:
                    setting = row['SettingName'].strip()
                    info = [row['ExpectedValue'].strip(), row['Framework'].strip(), row['ControlID'].strip(), row['Description'].strip(), row['Severity'].strip(), row['Category'].strip()]
                    parsed_bl[setting] = info
                return parsed_bl
        except Exception as e:
            return {}

    def get_bl_type(self):
        return self.bl_type