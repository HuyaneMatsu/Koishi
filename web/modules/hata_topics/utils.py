from markdown import markdown
from os import listdir as list_directory
from os.path import join as join_paths, isfile as is_file

def generate_markdown(markdown_folder):
    markdowns = {}
    
    for name in list_directory(markdown_folder):
        if not name.endswith(('.md', '.MD')):
            continue
        
        case_fold_name = name.casefold()
        if ('wip' in case_fold_name) or ('deprecated' in case_fold_name):
            continue
        
        file_path = join_paths(markdown_folder, name)
        if not is_file(file_path):
            continue
        
        with open(file_path, 'r'):
            
        