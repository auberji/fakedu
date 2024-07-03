import argparse
from pathlib import Path
from typing import List
import math

from enum import Enum
from os.path import exists
from sys import exit


class FileSize(Enum):
    KB = 1024
    MB = math.pow(1024, 2)
    GB = math.pow(1024, 3)

class FakeDu:

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
                    prog='fakedu',
                    description='fakedu',
                    epilog='Pretending to be du for interviews')
        parser.add_argument('--path', action='store', dest='root_path',
                            help='Path to search', required=True)
        parser.add_argument('--max-depth', action='store', type=int, dest='max_depth', default=0,
                            help='Maximum depth to iterate', required=False)
        parser.add_argument('--format', action='store', dest='format', default='B',
                            help='KB, MB, GB', required=False)
        parser.add_argument('--pattern', action='store', dest='pattern', default='*',
                            help='Pattern name of files and directories to search', required=False)
        return parser.parse_args()
    
    @staticmethod
    def search(path: Path, pattern: str, max_depth):
        files = []
        max_depth = max_depth - 1
        globbed = list(path.glob(pattern))
        for pathItem in globbed:
            if pathItem.is_file() and not pathItem.is_symlink():
                files.append((pathItem))
            elif pathItem.is_dir and max_depth > 0:
                files.extend(FakeDu.search(pathItem, pattern, max_depth))
        return files

    @staticmethod
    def file_size(path: Path):
        return path.stat().st_size
    
    def format_size(size, format: str):
        return f"{size}{format}" if format == "B" else f"{(size / FileSize[format].value):.20f}{format}"


    @staticmethod
    def sum_files(paths: List[Path]):
        sum = 0
        for path in paths:
            sum += FakeDu.file_size(path)
        return sum

        
    @staticmethod
    def main():
        args = FakeDu.parse_args()
     
        if not exists(args.root_path):
            raise OSError(f"{args.root_path} does not exist or is not a valid path\n")
    
        files = FakeDu.search(Path(args.root_path), args.pattern, args.max_depth)
        for file in files:
            print(f"File: {file.resolve()} Size: {FakeDu.format_size(FakeDu.file_size(file), args.format)}\n")
        print(f"Total Sum of path {args.root_path}: {FakeDu.format_size(FakeDu.sum_files(files), args.format)}\n")
        
if __name__ == "__main__":
    try:
        FakeDu.main()
    except OSError as err:
        print(err)
        exit(1)
