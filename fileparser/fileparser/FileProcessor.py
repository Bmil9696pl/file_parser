class FileProcessor:
    def __init__(self, file):
        self.file_content = file.readlines()
        self.file_name = self._get_file_name()
        self.file_extension = self._get_file_extension()
        self.actual_content = self._get_actual_content()

    def _get_file_name(self):
        return self.file_content[1].decode('utf-8').split('=')[2].strip().strip('"')

    def _get_file_extension(self):
        return self.file_name.split('.')[-1].lower()

    def _get_actual_content(self):
        content_lines = []
        in_file_content = False
        for line in self.file_content:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('Content-Disposition'):
                in_file_content = True
                continue
            if in_file_content and not decoded_line.startswith('--'):
                content_lines.append(decoded_line)
            if decoded_line.startswith('--') and in_file_content:
                break

        return ''.join(content_lines)