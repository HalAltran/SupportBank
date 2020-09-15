class CSVRow:
    def __init__(self, header_map, entries):
        self.header_map = header_map
        self.entries = entries

    def get_entry(self, header):
        return self.entries[self.header_map[header]]
