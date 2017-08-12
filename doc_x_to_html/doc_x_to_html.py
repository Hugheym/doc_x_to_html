#!/usr/bin/env python3
import sys
import mammoth
import os
import tempfile
import subprocess


__version__ = "0.0.2"

# Tested in Python 3.5.3

def is_doc_path(path: str) -> bool:
    """
     Returns True if path contains a .doc file, else False.
    """
    return path.endswith('.doc') and not os.path.isdir(path)


def is_docx_path(path: str) -> bool:
    """
     Returns True if path contains a .docx file, else False.
    """
    return path.endswith('.docx') and not os.path.isdir(path)


def doc_to_docx(file_path, out_dir_path):
    """
    Spawns subprocess that uses LibreOffice to save the source file having .doc
    format as a .docx file of the same base_name in the directory specified by
    out_dir_path
    :param file_path: full path of .doc file.
    :param out_dir_path: full path of output directory.
    """
    subprocess.call(['soffice', '--headless', '--convert-to', 'docx', file_path, '--outdir', out_dir_path])


def copy_to(file_path, target_dir_path):
    """
    Creates a symbolic link in target dir, having the same base name as and
    referring to the file specified by the file_path.
    :param file_path: full path to file we want to copy.
    :param target_dir: directory where symbolic link will go.
    """
    os.symlink(file_path, os.path.join(target_dir_path, os.path.basename(file_path)))


def get_file_list(root_dir: str, recursive: bool = True) -> [str]:
    """
    Get list of str that are full paths to all files in the root directory.
    :param root_dir:
    :return: list of paths of files in root directory.
    """
    res = []
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path):
            res.extend(get_file_list(root_dir=full_path, recursive=recursive))
        else:
            res.append(full_path)
    return res

def flatten_as_docx(source_dir_path, target_dir_path, recursive=True):
    """
    Given a source directory with a mixture of doc and docx files specified by source_dir_path,
    for each doc file create a file converted to docx, and for each docx file create a
    symbolic link to it inside the target directory specified by target_dir_path.
    If recursive is set to true, files in the source directory will be searched recursively, but
    the directory structure will not be preserved in the target directory.
    :param source_dir_path:
    :param target_dir_path:
    """
    for name in os.listdir(source_dir_path):
        full_path = os.path.join(source_dir_path, name)
        if os.path.isdir(full_path) and recursive:
            flatten_as_docx(full_path, target_dir_path)
        elif is_doc_path(full_path):
            doc_to_docx(full_path, target_dir_path)
        elif is_docx_path(full_path):
            copy_to(full_path, target_dir_path)


def get_html(source_dir_path, target_dir_path):
    """
    Given a source directory specified by source_dir_path and exclusively populated by docx
    :param source_dir_path: path to source directory populated by docx files.
    :param target_dir_path: path to target directory in which converted html files will be saved.
    """
    for name in os.listdir(source_dir_path):
        with open(os.path.join(source_dir_path, name), 'rb') as docFile:
            results = mammoth.convert_to_html(docFile)
            out_file_name = os.path.splitext(os.path.join(target_dir_path, name))[0] + '.html'
            with open(out_file_name, 'wb') as out_file:
                out_file.write(results.value.encode('utf-8'))


def check_success(source_path, target_path, recursive=True):
    """ Return true if all files in source path with an .doc or .docx extension have a corresponding file
    with an .html extension in target_path"""
    file_list = get_file_list(source_path, recursive=recursive)
    out_file_list = os.listdir(target_path) #since we want to only check top level of target directory
    file_list = [os.path.splitext(os.path.split(f)[-1])[0] for f in file_list]
    out_file_list = [os.path.splitext(p)[0] for p in out_file_list]
    return all((f in out_file_list for f in file_list))



def main():
    argv = sys.argv[1:]
    if(len(argv)<2):
        print("Expected 2 arguments, but got one. Please specify source path and target path")
        return 1
    source_path = argv[0]
    target_dirname = argv[1]
    tdir = tempfile.TemporaryDirectory()
    flatten_as_docx(source_path, tdir.name)
    get_html(tdir.name, target_dirname)
    success = check_success(source_path, target_dirname)
    if success:
        print("Success")
    else:
        print("Sorry, some files may not have been copied successfully")

