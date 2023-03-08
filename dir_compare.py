import argparse
import hashlib
import os
import pathlib
from dataclasses import dataclass

from colorama import Fore


@dataclass
class File:
    path: pathlib.Path
    hash: str | None


def get_hash_for_file(path: pathlib.Path):
    with open(path, "rb") as f:
        file_hash = hashlib.blake2b()
        while chunk := f.read(8192):
            file_hash.update(chunk)
        return file_hash.hexdigest()


def hash_dir(path: pathlib.Path, missing_files: list[str]):
    if not path.is_dir():
        return

    files_in_dir = list(path.iterdir())
    total_file_in_dir = len(files_in_dir)

    for i, file in enumerate(files_in_dir, start=1):
        file_name_str = file.name
        abs_path = file.absolute()

        if file_name_str in missing_files or file.is_dir():
            print(
                Fore.YELLOW
                + f"Skipping: {abs_path} ({i}/{total_file_in_dir})"
                + Fore.RESET
            )
            continue

        size_of_file = os.path.getsize(abs_path)
        print(
            Fore.BLUE
            + f"Hashing : {abs_path} ({i}/{total_file_in_dir}) [{size_of_file} bytes]"
        )
        yield File(file, get_hash_for_file(file))


def find_missing_files(dir1: pathlib.Path, dir2: pathlib.Path):
    dir1_files = [file.name for file in dir1.iterdir()]
    dir2_files = [file.name for file in dir2.iterdir()]

    if len(dir1_files) == len(dir2_files):
        return

    mismatch = list(set(dir1_files).symmetric_difference(dir2_files))
    if len(mismatch) == len(dir1_files) + len(dir2_files):
        print(Fore.RED + "No matching files to hash")
        exit(1)
    for file in mismatch:
        yield file


def compare_hashes(hash1: File, hash2: File) -> bool:
    return hash1.hash == hash2.hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="The original folder")
    parser.add_argument("dst", type=str, help="The folder to check")

    args = parser.parse_args()

    src = pathlib.Path(args.src)
    dst = pathlib.Path(args.dst)

    if src.absolute() == dst.absolute():
        print(Fore.RED + "Can't compare a path to itself")
        exit(1)

    missing_files = list(find_missing_files(src, dst))

    dir1 = list(hash_dir(src, missing_files))
    dir2 = list(hash_dir(dst, missing_files))

    for file1, file2 in zip(dir1, dir2):
        is_same = compare_hashes(file1, file2)
        fore_colour = Fore.RED
        if is_same is True:
            fore_colour = Fore.GREEN
        print(
            fore_colour
            + f"{pathlib.Path(file1.path.name)} Match: {is_same}"
            + Fore.RESET
        )


if __name__ == "__main__":
    main()
