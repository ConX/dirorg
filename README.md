Description
===========

This script organizes the files of a directory by grouping
them based on their extension. It can also group
directories by identifing which extension they mostly contain.


Help
====

Usage: dirorg.py [options] <Source Directory> [Destination Directory]

Options:

  -h, --help       show this help message and exit
  -b, --batch      Run without asking for directory creation.
  -v, --verbose    Print debug messages for every action.
  -d, --directory  Recursively determine the content of the directories and
                   group them properly.
  --dry-run        Simulate execution.
  --hidden         Work on hidden files too.


Configuring
===========

**Add new file extensions**

On the top of the script there is a tuple (EXTDIR) containing the correspondences
between extensions and destination directories.

```python
EXTDIR = (
          (("mp3", "wav"), "Audio"),
          (("avi", "mpeg", "mp4", "wmv"), "Videos"),
          (("tar", "tgz", "zip", "gz", "rar", "7z", "bz2"), "Archives"),
          (("jpg", "tiff", "jpeg", "gif", "png", "bmp", "ico"), "Images"),
          (("txt", "xml"), "Text"),
          (("pdf", "chm"), "PDFs"),
          (("doc", "docx", "ods", "odt", "ptt", "xls"), "Office"),
          (("sh", "py", "pl"), "Scripts"),
         )
```

If you want all files with "bin" and "exe" extension to be moved in "Binaries"
directory you just have to add the following tuple in EXTDIR:

```python
(("bin", "exe"), "Binaries")
```

Examples
========

**Group files in "foo" directory to "bar" directory. Ask for unknown extensions.**

```sh
$ dirorg.py foo/ bar/
```

**
