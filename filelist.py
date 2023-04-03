import os
import datetime
import stat
def getSrcs(sync):
    """
    Return the list of sources to sync
    """
    args = sync.args
    srcs = []
    if args.recursive:
        #get the absolute path of the base folder and add all files into srcs recursively
        if type(args.src) is list: # if we have more than one source
            for base_folder in args.src:
                if os.path.isdir(os.path.abspath(base_folder)):
                    for root, dirs, files in os.walk(base_folder):
                        for file in files:
                            srcs.append(os.path.join(root, file))
                            #print("Adding file %s to the list of files to sync" % os.path.join(root, file))
                elif os.path.isfile(base_folder): # if it's a file, just add it to the list
                    srcs.append(os.path.basename(base_folder))
                    #print("Adding file %s to the list of files to sync" % os.path.basename(base_folder))
                else:
                    print("Error: %s is not a directory or a file" % base_folder)
        else:
            base_folder = args.src
            if os.path.isdir(os.path.abspath(base_folder)):
                for root, dirs, files in os.walk(base_folder):
                    for file in files:
                        srcs.append(os.path.join(root, file))
                        #print("Adding file %s to the list of files to sync" % os.path.join(root, file))
            elif os.path.isfile(base_folder):  # if it's a file, just add it to the list
                srcs.append(os.path.basename(base_folder))
                #print("Adding file %s to the list of files to sync" % os.path.basename(base_folder))
            else:
                print("Error: %s is not a directory or a file" % base_folder)

    else:
        #get the absolute path of the base folder and add all files into srcs
        if type(args.src) is list and len(args.src) > 1: # if we have more than one source
            for base_folder in args.src:
                if os.path.isdir(os.path.abspath(base_folder)):
                    if not base_folder.endswith(os.sep) and base_folder != '.': # if the directory doesn't end with a slash don't add it
                        print("Error we are not able to copy a directory without the -r option")
                    else:
                        for file in os.listdir(base_folder):
                            if os.path.isfile(base_folder + '/' + os.path.basename(file)):
                                srcs.append(base_folder + '/' + os.path.basename(file)) # add the file to the list but not his directory root
                            #print("Adding file %s to the list of files to sync" % (base_folder + '/' + os.path.basename(file)))
                elif os.path.isfile(base_folder): # if it's a file, just add it to the list
                    srcs.append(os.path.basename(base_folder))
                    #print("Adding file %s to the list of files to sync" % os.path.basename(base_folder))
                else:
                    print("Error: %s is not a directory or a file" % base_folder)
        else:
            if type(args.src) == list:
                base_folder = args.src[0]
            else:
                base_folder = args.src
            if os.path.isdir(os.path.abspath(base_folder)):
                if not base_folder.endswith(os.sep) and base_folder != '.': # if the directory doesn't end with a slash don't add it
                    print("Error we are not able to copy a directory without the -r option")
                else:
                    for file in os.listdir(base_folder):
                        if os.path.isfile(file):
                            srcs.append(base_folder + '/' + os.path.basename(file)) # add the file to the list but not his directory root
                            #print("Adding file %s to the list of files to sync" % (base_folder + '/' + os.path.basename(file)))
            elif os.path.isfile(base_folder): # if it's a file, just add it to the list
                srcs.append(os.path.basename(base_folder))
                #print("Adding file %s to the list of files to sync" % os.path.basename(base_folder))
            else:
                print("Error: %s is not a directory or a file" % base_folder)
    return srcs

def formatFilePrint(file_path):
        stat_info = os.stat(file_path) # Obtient les informations sur le fichier
        mode = stat_info.st_mode        # Obtient les droits du fichier
        perms = '-'
        for who in 'USR', 'GRP', 'OTH':
            for what in 'R', 'W', 'X':
                if mode & getattr(stat, f'S_I{what}{who}'):
                    perms += what.lower()
                else:
                    perms += '-'
        size = stat_info.st_size
        mod_time = datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y/%m/%d %H:%M:%S') # Obtient la taille et la date de modification
        if file_path.startswith('./'): #on enleve le ./ si les srcs sont dans le dossier courant
            file_path = file_path[2:]
        print(f"{perms} {size:>10} {mod_time} {file_path}") # Formatte la ligne de sortie

def printSrcs(srcs):
    """
    Print the list of sources to sync
    """
    for src in srcs:
        formatFilePrint(src)