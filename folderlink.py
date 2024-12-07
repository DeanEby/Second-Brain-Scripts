# The idea is to check for/create a note for every folder in my notes directory. Then I can link every other note to this root note.

import os
import re
import markdown

path = "C:/Users/ebyd2/Documents/Obsidian Vault"


# I found this function somewhere on stack overflow but I didn't write the url down
# I've modified it to only scan the directories I want, and add the filenames and path
def run_fast_scandir(dir, ext):    # dir: str, ext: list
    subdir, dirpath, files, filepath = [], [], [], []

    for f in os.scandir(dir):
        # Here we filter out all of the folders that we don't want to have notes linking to
        if f.is_dir() and '.' != f.name[0] and f.name != "templates" and f.name != "attachments" and f.name != "General":
            subdir.append(f.name)
            dirpath.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                filepath.append(f.path)
                files.append(f.name)

    
    for dir in list(dirpath):
        sd, dp, f, fp = run_fast_scandir(dir, ext)
        subdir.extend(sd)
        dirpath.extend(dp)
        files.extend(f)
        filepath.extend(fp)
    return subdir, dirpath, files, filepath


# get list of directories and files as well as their paths
subdir, dirpath, files, filepath = run_fast_scandir(path, [".md"])

# look at each subdirectory and add rootfilepath notes
for i in dirpath:
    # get the index so we can use subdir to get just the name
    index = dirpath.index(i)
    # create a rootfilepath name for every path
    rootfilepath = i + '/' + subdir[index] + '.md'
    rootfilename = subdir[index]
    linkname = "[[" + rootfilename + "]]"
    if not os.path.exists(rootfilepath):
        with open(rootfilepath, 'w') as file:
            file.write(subdir[index])
    else:
        print(rootfilepath + ' already exists')
    #print(i + '.md')
    # Go through all the files in the directory
    for f in os.scandir(i):
        if f.is_file():
            try:
                with open(f.path, 'r') as file:
                    contents = file.read()
                    print("opening")
                    if linkname in contents:
                        print("linkname in contents")
                        pass
                    else:
                        with open(f.path, 'a') as file:
                            file.write('\n')
                            file.write("- folderlink -")
                            file.write(linkname)
                            print("writing")

            except:
                pass



