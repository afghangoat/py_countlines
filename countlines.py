#Version: 2.1
#Features:
#- Custom extension check count (just overwrite the extensions mapping to fit your needs)
#- Also check in ZIP file
#- Catches common errors
#- Lots of extensions supported by default config
#- Adds filter,ignore, command line support, --help
#- Credits: Afghan Goat

import os
import zipfile
import argparse

extensions_mapping = {
    '.js': 'JavaScript',
    '.mjs': 'JavaScript (Modules)',
    '.jsx': 'JavaScript (React)',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript (React)',
    '.html': 'HTML/Web Files',
    '.htm': 'HTML/Web Files',
    '.htaccess': 'HTML/Web Files',
    '.htpasswd': 'HTML/Web Files',
    '.xml': 'HTML/Web Files',
    '.xhtml': 'HTML/Web Files',
    '.svg': 'HTML/Web Files (SVG)',
    '.info': 'Information Files',
    '.css': 'CSS',
    '.scss': 'SASS (SCSS)',
    '.sass': 'SASS (Indented Syntax)',
    '.less': 'LESS',
    '.py': 'Python',
    '.pyw': 'Python (Windows)',
    '.pyo': 'Python (Optimized Bytecode)',
    '.pyc': 'Python (Compiled Bytecode)',
    '.php': 'PHP',
    '.php3': 'PHP',
    '.php4': 'PHP',
    '.php5': 'PHP',
    '.phtml': 'PHP',
    '.java': 'Java',
    '.jsp': 'Java Server Pages',
    '.c': 'C',
    '.h': 'C Header',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.inl': 'C++ Inline file',
    '.tpp': 'C++ Template file',
    '.cxx': 'C++',
    '.hpp': 'C++ Header',
    '.cs': 'C#',
    '.dat': 'Data file',
    '.vb': 'Visual Basic',
    '.vbproj': 'Visual Basic Project Config',
    '.vbs': 'Visual Basic Script',
    '.lua': 'Lua',
    '.sh': 'Bash Script',
    '.zsh': 'Zsh Script',
    '.zs': 'Z Script',
    '.bat': 'Windows Batch Script',
    '.cmd': 'Windows Command Script',
    '.asm': 'Assembly',
    '.s': 'Assembly',
    '.v': 'Verilog',
    '.sv': 'SystemVerilog',
    '.hdl': 'Hardware Description Language',
    '.gd': 'Godot Script',
    '.glsl': 'Shader',
    '.vert': 'Shader',
    '.frag': 'Shader',
    '.gdshader': 'Shader',
    '.frag': 'Shader (Fragment)',
    '.vert': 'Shader (Vertex)',
    '.geo': 'Shader (Geometry)',
    '.r': 'R Script',
    '.rmd': 'R Markdown',
    '.rs': 'Rust',
    '.dart': 'Dart',
    '.go': 'Go',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.kts': 'Kotlin (Script)',
    '.rb': 'Ruby',
    '.erb': 'Ruby (Embedded)',
    '.pl': 'Perl',
    '.pm': 'Perl Module',
    '.tcl': 'Tcl',
    '.clj': 'Clojure',
    '.cljs': 'ClojureScript',
    '.groovy': 'Groovy',
    '.scala': 'Scala',
    '.ml': 'OCaml',
    '.mli': 'OCaml Interface',
    '.hs': 'Haskell',
    '.erl': 'Erlang',
    '.ex': 'Elixir',
    '.exs': 'Elixir (Script)',
    '.nim': 'Nim',
    '.coffee': 'CoffeeScript',
    '.elm': 'Elm',
    '.json': 'JSON',
    '.toml': 'TOML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.pas': 'Pascal',
    '.ini': 'INI Configuration',
    '.cfg': 'Configuration File',
    '.md': 'Markdown',
    '.rst': 'reStructuredText',
    '.tex': 'LaTeX',
    '.bib': 'LaTeX Bibliography',
    '.rkt': 'Racket',
    '.lsp': 'Lisp',
    '.lisp': 'Lisp',
    '.a68': 'Algol 68',
    '.alg': 'Algol',
    '.scm': 'Scheme',
    '.asp': 'Active Server Pages',
    '.aspx': 'ASP.NET',
    '.sql': 'SQL',
    '.ps1': 'PowerShell',
    '.psm1': 'PowerShell Module',
    '.psd1': 'PowerShell Data File',
    '.cob': 'COBOL File',
    '.f': 'Fortran',
    '.for': 'Fortran',
    '.f90': 'Fortran (Modern)',
    '.f95': 'Fortran (Modern)',
    '.pro': 'Prolog',
    '.awk': 'AWK Script',
    '.mat': 'MATLAB Data File',
    '.m': 'MATLAB/Objective-C',
    '.octave': 'GNU Octave',
    '.vhd': 'VHDL',
    '.vhdl': 'VHDL',
    '.hdl': 'Hardware Description Language',
    '.mk': 'Makefile'
}

specific_files = {
    'makefile': 'Makefile',
    'Makefile': 'Makefile',
    'doxyfile': 'Doxygen config file',
    'Doxyfile': 'Doxygen config file'
}

def count_lines_in_file(file_path, file_obj=None):
    try:
        if file_obj:
            lines = sum(1 for line in file_obj.splitlines())
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = sum(1 for line in file)
        return lines
    except PermissionError:
        print(f"Skipping file: {file_path} (Permission denied)")
        return 0
    except FileNotFoundError:
        print(f"Skipping file: {file_path} (File not found)")
        return 0

# Process files based on extensions
def process_file(file_name, file_obj=None):

    for specific_name, lang in specific_files.items():
        if file_name.endswith(specific_name):
            return lang, count_lines_in_file(None, file_obj) if file_obj else count_lines_in_file(file_name)
    
    for ext, lang in extensions_mapping.items():
        if file_name.endswith(ext):
            return lang, count_lines_in_file(None, file_obj) if file_obj else count_lines_in_file(file_name)
    
    return None, 0

def process_directory(root_dir):
    total_lines_by_language = {}

    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith('.zip'):
                try:
                    with zipfile.ZipFile(file_path, 'r') as archive:
                        for entry in archive.namelist():
                            lang, lines = process_file(entry, archive.read(entry).decode('utf-8', errors='ignore'))
                            if lang:
                                total_lines_by_language[lang] = total_lines_by_language.get(lang, 0) + lines
                except zipfile.BadZipFile:
                    print(f"Skipping corrupted zip file: {file_path}")
            else:
                lang, lines = process_file(file_path)
                if lang:
                    total_lines_by_language[lang] = total_lines_by_language.get(lang, 0) + lines

    return total_lines_by_language

# Print the results
def print_results(total_lines_by_language):
    total_lines = 0
    print("Total lines in source code:")
    for lang, lines in sorted(total_lines_by_language.items(), key=lambda x: x[0]):
        print(f" {lang}: {lines} lines")
        total_lines += lines
    print(f"----\nTotaling: {total_lines} lines")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Counts LoC in a specified directory recursively.")
    parser.add_argument("folder_path", help="The name of the folder which needs to be scanned.")
    parser.add_argument("--filter", default="nofilter|", help="Filter for specific extension? (nofilter,filter,ignore) (example: --filter filter,Makefile,-txt) This will find you makefiles and txts.")
    
    args = parser.parse_args()
    
    exts=args.filter.split(',')
    del exts[0]
    
    if args.filter.startswith("filter")==True:
        extensions_mapping.clear()
        specific_files.clear()
        for n in exts:
            n = n.replace("-", ".")
            if '.' in n:
                extensions_mapping[n]=n
            else:
                specific_files[n]=n
    elif args.filter.startswith("ignore")==True:
        for n in exts:
            n = n.replace("-", ".")
            if '.' in n:
                if n in extensions_mapping:
                    del extensions_mapping[n]
            else:
                if n in specific_files:
                    del specific_files[n]
    

    total_lines_by_language = process_directory(args.folder_path)
    print_results(total_lines_by_language)