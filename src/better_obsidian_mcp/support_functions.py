import os

def get_note_list(directory):
    return [f[:-3] for f in os.listdir(directory) if f.endswith('.md')]
