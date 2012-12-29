#!/usr/bin/env python
# ==================================================
# Created by Constantinos Xanthopoulos (ConX)
# Email: conx AT xanthopoulos DOT info.
# ==================================================

import os,re,sys
from optparse import OptionParser


##### CONFIGURATIONS #####

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

##### SCRIPT #####

def trailSlash(path):
     if path[-1] != '/':
          path += '/'
     return path

def getExt(filename):
     if "." in filename:
          return filename.split(".")[-1]
     else:
          return None

def getDst(extension):
     for exts in EXTDIR:
          if extension in exts[0]:
               return exts[1]
     return None

def debug(text):
     global verbose
     if verbose:
          print text

def getYNAns(msg):
     while True:
          ans = raw_input(msg+" [y/n]: ")
          if ans == "y":
               return True
          elif ans == "n":
               return False

def fileMove(sf, dd):
     global dryrun
     if not os.path.exists(dd):
          debug("Creating directory '%s'." % (dd))
          if not dryrun:
               os.makedirs(dd)
     debug("Moving file %s in '%s'." % (sf, dd))
     if not dryrun:
          os.system ("mv '"+sf+"' '"+dd+"'")

def filesMove(sd, dd):
     global batch
     global hidden
     for f in [f for f in os.listdir(sd) if os.path.isfile(sd+f)]:
          if not f.startswith(".") or (hidden and f[1:].find(".") > -1):
               ext = getExt(f)
               if ext:
                    dst = getDst(ext)
                    if dst:
                         fileMove(sd+f, dd+dst)
                    elif batch:
                         fileMove(sd+f, dd+ext)
                    else:
                         ans = getYNAns("Create directory '%s' and move '%s' to it?" % (dd+ext, sd+f))
                         if ans:
                              fileMove(sd+f, dd+ext)


def dirMove(sd, dd):
     global hidden
     dircont = {}
     for d in [f for f in os.listdir(sd) if os.path.isdir(sd+f)]:
          if not d.startswith(".") or (hidden and d[1:].find(".") > -1):
               dircont[sd+d] = {}
               for root, sf, files in os.walk(sd+d):
                    for f in files:
                         f = os.path.join(sd, d, root, f)
                         dircont[sd+d][getExt(f)] = os.path.getsize(f) if not dircont[sd+d].has_key(getExt(f)) else os.path.getsize(f)+dircont[sd+d][getExt(f)]
               dircont[sd+d] = max(dircont[sd+d], key=lambda a: dircont[sd+d].get(a))
     for d in dircont.keys():
          dst = getDst(dircont[d])
          if dst:
               fileMove(d, dd+dst)
          elif batch:
               fileMove(d, dd+dircont[d])
          else:
               ans = getYNAns("Create directory '%s' and move '%s' to it?" % (dd+dircont[d], d))
               if ans:
                    fileMove(sd+f, dd+ext)


if __name__ == "__main__":
     usage = "Usage: %prog [options] <Source Directory> [Destination Directory]"
     parser = OptionParser(usage)
     parser.add_option("-b", "--batch", action="store_true", default=False, dest="batch", help="Run without asking for directory creation.")
     parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="Print messages for every action taken.")
     parser.add_option("-d", "--directory", action="store_true", default=False, dest="directory", help="Recursively determine the content of the directories and group them properly.")
     parser.add_option("--dry-run", action="store_true", default=False, dest="dryrun", help="Simulate execution.")
     parser.add_option("--hidden", action="store_true", default=False, dest="hidden", help="Work on hidden files too.")


     (options, args) = parser.parse_args()
     if not (len(args) > 0 and len(args) < 3):
          parser.print_help()
          sys.exit()
     
     batch = options.batch
     verbose = options.verbose
     dryrun = options.dryrun
     hidden = options.hidden
     directory = options.directory
     dd = "./";
     sd = trailSlash(args[0])
     
     if len(args) == 2:
          dd = trailSlash(args[1])
     
     if not directory:
          filesMove(sd, dd)
     else:
          dirMove(sd, dd)
