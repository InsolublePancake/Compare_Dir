import os

def getFileTree(rootDir):
    Tree = {}

    for dirPath, subdirList, fileList in os.walk(rootDir):
        if dirPath.endswith('ipynb_checkpoints'): continue
        else: pass
        #print(dirName)
        dirName = dirPath.split(os.sep)[-1].lower()
        Tree.setdefault(dirName, [])
        Tree[dirName].append({dirPath : [{'path': os.path.join(dirPath, file),
                                          'size': os.stat(os.path.join(dirPath, file))[6],
                                          'filetype': file.split(os.extsep)[-1]} for file in fileList]})
    return Tree


def dirSizes(Tree):
    #Get size of each duplicate directory
    #print('\n\nBytes\tFolder')
    for directory in Tree.keys():
        for dupeDir in Tree[directory]:
            for fol in dupeDir.keys():
                total = 0
                for file in dupeDir[fol]:
                    #print(file['size'], '\t', file['path'])
                    total += file['size']
                #print(total, '\t', fol)
        #print()


#Get list of files for each duplicate directory
#Output a list of dictionaries with one dictionary per directory name
# and each dictionary in the form: {folderpath: [list of filenames]}

def createDirNameList(Tree):
    excludeFiles = ['Thumbs.db']
    excludeExt = ['ipynb']
    dirList = []
    for directory in Tree.keys():
        dic = {}
        for dupeDir in Tree[directory]:
            #dic[dupDir] = []
            #print(dupeDir)
            for fol in dupeDir.keys():
                #print(fol)
                dic[fol] = {}
                for file in dupeDir[fol]:
                    #if file not in excludeFiles and file.split('.')[-1] not in excludeExt:
                    #Appends a tuple of file (name, size) to dirNameList
                    #At this point it could be useful to split the file extension off
                    fileNm = file['path'].split('\\')[-1]
                    fileSz = file['size']
                    #dic[fol].append((fileNm, fileSz))
                    if fileNm not in excludeFiles and fileNm.split('.')[-1] not in excludeExt:
                        dic[fol][fileNm] = fileSz
                    else: pass

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




path = r"N:\user\lumbric\python\Pixel"
dirTree = getFileTree(path)

dirSizes(dirTree)
dirNameList = createDirNameList(dirTree)






def compareDirs(dirList):
    #for every dirName
    #    for every duplicate dir name
    #        check the other duplicate dirs for the same filename, 
    #        and test whether it is the same size
    
    #for each unique directory name in the main list
    for drN, dirName in enumerate(dirList):
        allList =[]
        for dr in dirName:
            allList += [k for k in dirList[drN][dr].keys()]
        allSet = set(allList) #Set of all files from all duplicate directories
        
        missDict = {}
        missDict2 = {}
        sizeDict = {}
        
        if len(dirName.keys()) > 1:
            name = list(dirName.keys())[0].split(os.path.sep)[-1].upper()
            print('\nDuplicate directories found for: ', name, '\nComparing contents...\n') 
        
        #for each version of this directory
        for dpN, dupDir in enumerate(dirName):
            #Check that there are duplicate directories
            if len(dirName) == 1: continue
            else:
                #for every duplicate directory
                # list of filenames --> dirList[drN][dupDir].keys()
                # Directory path --> dupDir
                for f in allSet:
                    if f not in dirList[drN][dupDir].keys():
                        missDict.setdefault(f, [])
                        if dupDir not in missDict[f]:
                            missDict[f].append(dupDir)
                        else:pass
                    else:pass
                
                for fi in allSet:
                    if fi not in dirList[drN][dupDir].keys():
                        missDict2.setdefault(dupDir, [])
                        missDict2[dupDir].append(fi)
                        
                #for each file in directory
                for fl in dirList[drN][dupDir].items():
                    fn = fl[0]
                    fs = fl[1]
                    fpath = dupDir
                    sizeDict.setdefault(fn, ([],[]))
                    
                    if dupDir not in sizeDict[fn][1]:
                        sizeDict[fn][0].append(fl[1])
                        sizeDict[fn][1].append(fpath)                     
                
                dname = dupDir.split(os.path.sep)[-1]

        sizeDict = {k: v for k, v in sizeDict.items() if len(set(v[0])) > 1 }

        if sizeDict or missDict: 
            print('Duplicate directories are not identical:\n'.format(dname.upper()))
        else:
            print('Duplicate directories contain the same files at the same size')
            
        if sizeDict:
            print('There are differently sized versions of one or more files:')
            for k, v in sizeDict.items():
                print(k)
                for n in range(len(v[0])):
                    print('\t\t', v[0][n], '\t', v[1][n])
            print()

        #if missDict:
        #    print('The following files are missing from some directories:')
        #    for k, v in missDict.items():
        #        if v:
        #            print(k)
        #            for path in v:
        #                print('\t\t', path)
        #    print()
        
        if missDict2:
            for d in dirList[drN].keys():
                if d not in missDict2.keys():
                    print('{} has no missing files'.format(d))
            print('The following directories are missing files:')
            for k, v in missDict2.items():
                print('\t', k)
                for vs in v: print('\t\t', vs)
            print()
        
        print(40*'-')
                
compareDirs(dirNameList)   





