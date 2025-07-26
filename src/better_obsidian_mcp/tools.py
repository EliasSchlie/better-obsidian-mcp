import os
from support_functions import get_note_list
from pydantic import Field

def read_note_outer(*args, **kwargs):
    directory = kwargs["directory"]
    
    def read_note(note_title: str = Field(description="The title of the note to read.")) -> str:
        """
        Get the content of a note with the provided title.
        """
        try:
            with open(os.path.join(directory, note_title + ".md"), "r") as f:
                return f.read()       
        except FileNotFoundError:
            return f"Note {note_title} not found."
    return read_note