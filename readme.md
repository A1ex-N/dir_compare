# dir_compare.py

Simple python script to compare files in two directories (by hashing them, using hashlib.blake2b) and report mismatches 
(files in both directories have to have matching filenames)

For example if you have two dirs
```
dir1/
  one.txt -> contains the text "true"
  two.txt -> contains the text "true"
dir2/
  one.txt -> contains the text "true"
  two.txt -> contains the text "false"
```

the output of the command `dir_compare.py dir1 dir2` will be 

```
Hashing: dir1/one.txt (1/2) [size of file]
Hashing: dir1/two.txt (2/2) [size of file]
Hashing: dir2/one.txt (1/2) [size of file]
Hashing: dir2/two.txt (2/2) [size of file]

one.txt Match: True
two.txt Match: False
```

Note:
The program will skip hashing files that don't exist in both directories, and will ignore sub-directories.
