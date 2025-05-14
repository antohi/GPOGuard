import csv


class BaselineParser:

    # Parses baseline file and returns it as a dict
    @staticmethod
    def parse_bl(bl_path) -> dict:
        parsed_bl = {}
        try:
            with open(bl_path, mode='r') as b:
                reader = csv.DictReader(b)
                for row in reader:
                    setting = row['SettingName'].strip()
                    info = [row['ExpectedValue'].strip(), row['Framework'].strip(), row['ControlID'].strip(), row['Description'].strip(), row['Severity'].strip(), row['Category'].strip()]
                    parsed_bl[setting] = info
                return parsed_bl
        except Exception as e:
            return {}
