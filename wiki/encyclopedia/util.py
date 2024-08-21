import os

def list_entries():
    """Returns a list of all names of encyclopedia entries."""
    return [filename.replace(".md", "") for filename in os.listdir("entries") if filename.endswith(".md")]

def save_entry(title, content):
    """Saves an encyclopedia entry, given its title and Markdown content."""
    with open(f"entries/{title}.md", "w") as f:
        f.write(content)

def get_entry(title):
    """Retrieves an encyclopedia entry by its title. Returns None if no such entry exists."""
    try:
        with open(f"entries/{title}.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None
