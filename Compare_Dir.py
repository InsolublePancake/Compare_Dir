import os

def getFileTree(rootDir):
    Tree = {}
    for dirPath, subdirList, fileList in os.walk(rootDir):
        if dirPath.endswith('.ipynb_checkpoints'): continue
        else: pass
        #print(dirName)
        dirName = dirPath.split('\\')[-1].lower()
        Tree.setdefault(dirName, [])
        Tree[dirName].append({dirPath : [{'path': os.path.join(dirPath, file),
                                          'size': os.stat(os.path.join(dirPath, file))[6],
                                          'filetype': file.split('.')[-1]} for file in fileList]})
    return Tree


def dirSizes(Tree):
    #Get size of each duplicate directory
    print('\n\nBytes\tFolder')
    for directory in Tree.keys():
        for dupeDir in Tree[directory]:
            for fol in dupeDir.keys():
                total = 0
                for file in dupeDir[fol]:
                    #print(file['size'], '\t', file['path'])
                    total += file['size']
                print(total, '\t', fol)
        print()


#Get list of files for each duplicate directory
#Output a list of dictionaries with one dictionary per directory name
# and each dictionary in the form: {folderpath: [list of filenames]}

def createDirNameList(Tree):
    dirList = []
    for directory in Tree.keys():
        dic = {}
        for dupeDir in Tree[directory]:
            #dic[dupDir] = []
            #print(dupeDir)
            for fol in dupeDir.keys():
                print(fol)
                dic[fol] = []
                for file in dupeDir[fol]:
                    #Appends a tuple of file (name, size) to dirNameList
                    #At this point it could be useful to split the file extension off
                    fileNm = file['path'].split('\\')[-1]
                    fileSz = file['size']
                    dic[fol].append((fileNm, fileSz))
                    #print(file['size'], '\t', file['path'])
                    #total += file['size']
        dirList.append(dic)
    return dirList

#Tree                           -- dict   keys: directory names (e.g. 'images') 
#Tree[dirName]                  -- list
#Tree[dirName][x]               -- dict   keys: directory paths (e.g. 'N:\\user\\lumbric\\python\\Pixel\\images')
#Tree[dirName][x]["dirPath"]    -- list
#Tree[dirName][x]["dirPath"][x] -- dict   keys: 'size', 'path', 'filetype'
    
#             Tree                           -- dict   keys: directory names (e.g. 'images') 
#directory    Tree[dirName]                  -- list
#dupeDir      Tree[dirName][x]               -- dict   keys: directory paths (e.g. 'N:\\user\\lumbric\\python\\Pixel\\images')
#fol          Tree[dirName][x]["dirPath"]    -- list
#file         Tree[dirName][x]["dirPath"][x]  -- dict   keys: 'size', 'path', 'filetype'



def compareInternal(dirList):
    """ dirNameList is a list of dictionaries. Each dictionary corresponds to folder name
        and each key is the path for the folder. So, a uniquely named folder will be
        in a dictionary with a single key (the path to the folder). 
        Where multiple folders have the same name the corresponding dictionary will 
        have multiple keys."""

    for dname in dirList:
        excludeList = ['Thumbs.db'] #Files to ignore in comparisons

        # creates a set of the number of files in each duplicate directory. 
        s = {len(dname[dupe]) for dupe in dname.keys()} 
        # if s==1  all the folders have the same number of files (note the files may be different)
        if len(s) > 1:
            compList = [] # list
            nameList = []
            for dupe in dname.keys():
                compList.append({d for d in dname[dupe] if d[0] not in excludeList})
                nameList.append(dupe)

    # Compare directories with Set comparisons
    # For each directory (set) in compList:
    for n, i in enumerate(compList):
        subList = compList[:n] + compList[n+1:]
        subSet = set()
        for s in subList: 
            subSet = subSet | s
                
        print('~~ {} ~~'.format(nameList[n]), 
        '\nDoes either not include the following, or filesizes differ:\n', 
        [tup[0] for tup in subSet-i], '\n')

   





path = r"N:\user\lumbric\python\Pixel"
dirTree = getFileTree(path)
dirSizes(dirTree)
dirNameList = createDirNameList(dirTree)

compareInternal(dirNameList)









