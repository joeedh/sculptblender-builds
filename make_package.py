import zipfile as zf
import os, sys
import datetime

def np(path):
  return os.path.abspath(os.path.normpath(path))

ERROR_RET = -1

def print_help():
  print("usage: python make_package.py path-to-build-bin-dir optional-out-dir")
  
if len(sys.argv) < 2:
  print_help()
  sys.exit(ERROR_RET)

binpath = np(sys.argv[1])
if not os.path.exists(binpath):
  print("error: invali path " + binpath)
  sys.exit(ERROR_RET)
  
def make_default_name():
  time = datetime.datetime.now()
  osname = sys.platform.lower()
  
  if osname == "win32":
    osname = "win64"
  
  return "sculptblender_%s_%s_%s_%s.zip" % (str(time.year), str(time.month), str(time.day), osname)
    

OUTPATH = make_default_name()
if len(sys.argv) > 2:
  outdir = sys.argv[2]
  if not outdir.startswith("./") and not outdir.startswith("/") \
     and not outdir.startswith(".\\") and not outdir.startswith("\\"):
     outdir = "./" + outdir
  
  if not os.path.exists(outdir):
    os.makedirs(outdir)
    
  OUTPATH = os.path.join(outdir, OUTPATH)
  OUTPATH = np(OUTPATH)
  
print("Pulling files from %s\n" % (binpath))  
print("Generating %s" % (OUTPATH))

badexts = {"pdb", "cmake", "o", "obj", 
           "i", "rc.res", "rc", "log",
           "glsl.c", "h.done",
           "png.c", "h.c", "hh.c", "cc", "hh", "h"
          }
          
badfiles = {
#  "intermediate.manifest",
#  "embed.manifest", 
  "makesdna",
  "makesrna", 
  "datatoc",
  "CMakeCache.txt",
  "install_manifest.txt",
  "out",
  "tests.exe",
  "tests.exe.manifest",
  "datatoc_icon",
}

baddirs = {".cmake", "CMakeFiles", "tests", "Testing"}

def strip_binpath(f):
  f = np(f)
  f = f[len(binpath):]
  if f.startswith(os.path.sep):
    f = f[1:]
  return f
def nixpath(f):
  if sys.platform == "win32":
    f = f.replace("\\", "/")
  return f
  
def baddir(d):
  d = nixpath(strip_binpath(d)).split("/")

  for baddir in baddirs:
    if baddir in d:
      return True
        
  return False
  
def badfile(f):
  f = f.lower()
  if f.find("ninja") >= 0:
    return True
  if f.find("__pycache__") >= 0:
    return True
    
  for ext in badexts:
    binf = os.path.split(f)[1]
    if binf.endswith(".exe"):
      binf = f[:-4]
    
    if f.endswith("." + ext) or binf in badfiles:
      return True
    if f.startswith("unity_") and f.find("cxx") >= 0:
      return True
    if f.startswith("cmake_"):
      return True
      
  return False

def is_datadir(d):
  d = strip_binpath(np(d))
  return d.startswith("3") or d.startswith("4") or d.startswith("5")
  
#Find latest datadir 
def find_datadir():
  maxversion = None
  ret = None
  
  for f in os.scandir(binpath):
    if not f.is_dir():
      continue
    
    if is_datadir(f.path):
      f = f.name
      version = f.split(".")
      if len(version) > 1 and len(version[1]) == 1:
        version[1] = "0" + version[1]
      version = int("".join(version))
      
      if maxversion is None or version > maxversion:
        maxversion = version
        ret = f 
        
  return ret
      

if os.path.exists(OUTPATH):
  os.remove(OUTPATH)
  
ZIP_MODE = zf.ZIP_DEFLATED
#ZIP_MODE = zf.ZIP_STORED
zip = zf.ZipFile(OUTPATH, mode="w", compression=ZIP_MODE, compresslevel=4)

datadir = find_datadir()
zipfiles = []

for root, dirs, files in os.walk(binpath):
  if is_datadir(root) and not strip_binpath(root).startswith(datadir):
    continue
  
  if baddir(root):
    continue
  
  for f in files:
    fullpath = os.path.join(root, f)

    if badfile(fullpath):
      continue
      
    #if is_datadir(root):
    #  print(fullpath)
      
      
    zipfiles.append(fullpath)

for i, fullpath in enumerate(zipfiles):
  #break
  perc = 100.0 * (i + 1) / float(len(zipfiles))
  
  zippath = "sculptblender/" + nixpath(strip_binpath(fullpath))
  
  #print(zippath)
  sys.stdout.write("%.1f%%: %s\r" % (perc, zippath))
  zip.write(fullpath, zippath)
  
zip.close()