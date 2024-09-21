import os

class write_file():
    @staticmethod
    def write(output_file,text):
        with open(output_file, 'a') as file:
            file.write(f"{text}")