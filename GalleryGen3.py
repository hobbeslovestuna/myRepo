import re
import os

path ='E:/siteAthos/photos/'

class GalleryGen(object):

    def __init__(self):
        '''
            All paths must end with a /
            TODO : check if the creation log time is older than start time if so, don't log it
        '''
        # print '_'*30
        # print '\t\tInit'
        # print '_'*30
        self.__rootPath = 'E:/siteAthos/photos/'
        self.__rootHTML = 'E:/siteAthos/'

        self.__startTime = 0
        self.__verbose = False
        # pattern = 'info.log'
        for root, sub, files in os.walk(self.__rootPath):
            # print root, sub, files
            if self.logExists(root) == False and not sub == []:
                print 'log'
                self.log(root)
                #build HTML ?
            elif self.logExists(root) == True:
                if self.__verbose:
                    print 'Log found for : %s' %root
    
    def log(self, path):
        '''
            Creates a log file containing all the folders at a time.
        '''
        output = ''
        logFile = open(os.path.join(path,'info.log'), 'w')
        listdirs = os.listdir(path)
        for dir in listdirs:
            if os.path.isdir(os.path.join(path, dir)):
                output += dir+'\n'
        logFile.write(output)
        logFile.close()

    def logExists(self, path):
        '''
            Check if the log files exists
            To be used to determine if there is need to create it
        '''
        logFile = os.path.join(path, 'info.log')
        # print logFile +'***'
        if not os.path.isfile(logFile):
            return False
        else:
            return True

    def logDiff(self, path):
        '''
            Compares the log to the actual list of dirs to see if there's a difference.
            Returns True if yes
        '''
        currentPath = path
        listdirs = os.listdir(currentPath)
        try:
            listdirs.remove('info.log')
        except:
            print '\t\tNo log found in %s' %currentPath
            # pass
        try:
            listdirs.remove('folder.jpg')
        except:
            print '\t\tNo folder.jpg found in %s' %currentPath
        try :
            listdirs.remove('index.html')
        except:
            print '\t\tNo HTML found in %s' %currentPath
        logFilePath = os.path.join(path, 'info.log')
        try:
            logFile = open(logFilePath, 'r')
            logFile = logFile.readlines()
        except  IOError:
            # print 'Log file could not be opened'
            logFile = []
            return -1

        if len(listdirs) == len(logFile):
            # print 'No new file detected'
            return False
        elif len(listdirs) > len(logFile):
            # print 'New file detected'
            return True
        elif len(listdirs) < len(logFile):
            # print 'Folder or file suppression detected'
            return True
    
    def createMainIndex(self, path, force = False):
        '''
            Creates the main HTML index page, listing all the folders in /photos/
        '''
        if path == None:
            inpath = self.__rootPath
        else:
            inpath = path
        
        listFolder  = os.listdir(inpath)
        indexFile   = os.path.join(self.__rootHTML, 'index.html')
        print 'CHECK FOR MAIN INDEX'
        if self.logExists(inpath) == False or os.path.isfile(indexFile) == False:
            indexPath = inpath.split('photos')[0]
            try:
                listFolder.remove('info.log')
            except:
                pass
            output = self.buildMainIndexHTML(listFolder)
            print '\tbuildHTML init'
            outputFile = open(os.path.join(indexPath, 'index.html'), 'w')
            outputFile.write(output)
            outputFile.close()
            self.log(inpath)
            print '\tbuildHTML done'
        else:
            # print 'in ELSE'
            print '\tLog found. Check for logDiff'
            if self.logDiff(inpath) == True or force == True:
                indexPath = inpath.split('photos')[0]
                try:
                    listFolder.remove('info.log')
                except:
                    print 'no log'
                # print indexPath
                output = self.buildMainIndexHTML(listFolder)
                outputFile = open(os.path.join(indexPath, 'index.html'), 'w')
                outputFile.write(output)
                outputFile.close()
                self.log(inpath)
                print '\tIndex written and log updated'
            elif self.logDiff(inpath) == False:
                print '\tNo diff found the main index is correct'
    
    def buildMainIndexHTML(self, dirs):
        '''
            Creates the output for the regular HTML page.
            Not the gallery
        '''
        output = ''
        beginIndexPath = os.path.join(self.__rootHTML, 'beginIndex.html')

        beginFile = open(beginIndexPath, 'r')
        for line in beginFile.readlines():
            output += line
        # print output
        for d in dirs:
            path        = d
            name        = d.split('/')[-1]
            thumbPath   = d.split('photos/')[-1]
            if len(d.split('/')) == 3:
                path = path.split('/')[-1]
            p = './photos/'+path
            output += '''<li>
                <a href='%s/index.html'><em>%s</em><span></span><img src='%s/folder.jpg'  alt='No thumbnail found' /></a>
            </li>\n''' % (p, name, p)
        # print output
        endFilePath = os.path.join(self.__rootHTML, 'end.html')
        endFile = open(endFilePath, 'r')
        for line in endFile.readlines():
            output += line
        beginFile.close()
        endFile.close()
        return output

    def createSubGalleryIndexPage(self, path, force = False):
        '''
            Create and save the subGalleryIndexPage based on the path
            path    -> path to the root photo folder
            force   -> to force the creation even if no differences are found. 
        '''
        if path == None:
            path = self.__rootPath

        mainGalleries = [f for f in os.listdir(path) if f != 'info.log']
        for main in mainGalleries:
            print 'CHECK FOR GALLERY : %s' %main
            pathToSub = os.path.join(path, main)
            print '\tLooking for subGalleries of %s' %main
            print '\t%s' %pathToSub
            subGalleries = [sub for sub in os.listdir(pathToSub) if not sub in ['index.html', 'info.log', 'folder.jpg']]
            #-----If log exists we check logDiff then create or not the index.html
            if self.logExists(pathToSub) == False or os.path.isfile(os.path.join(pathToSub, 'index.html')) == False:
                #---CASE : there is no log os we must create the HTML based on the list dirs and create the log
                print '\tCASE : No log found or no HTML found'
                print '\tBuilding subGalleries init'
                subHTML = self.buildSubGalleryHTML(subGalleries)
                test = open(os.path.join(pathToSub, 'index.html'), 'w')
                test.write(subHTML)
                test.close()
                #----Writing gallery
                pathsToPics = [os.path.join(pathToSub, p) for p in os.listdir(pathToSub) if not p in ['info.log', 'index.html', 'folder.jpg']]
                pathsToPics = [p.replace('\\', '/') for p in pathsToPics]
                # print '_'*50
                # print pathsToPics
                for pathToPic in pathsToPics:
                    galleryHTML = self.buildGalleryHTML(pathToPic)#mainGalleries out
                    try:
                        galleryPath = os.path.join(pathToPic, 'index.html')
                        galleryFile = open(galleryPath, 'w')
                        galleryFile.write(galleryHTML)
                        galleryFile.close()
                    except:
                        print 'Error saving the gallery %s'%pathToPic
                self.log(pathToSub)
                print '\tBuilding subGalleries done'
            else:
                #---CASE : Log found and need to check for logDiff
                print '\tCASE : Log found. Checking logDiff'
                if self.logDiff(pathToSub) == True or force == True:
                    subHTML = self.buildSubGalleryHTML(subGalleries)
                    test = open(os.path.join(pathToSub, 'index.html'), 'w')
                    test.write(subHTML)
                    test.close()
                    #----Writing gallery
                    pathsToPics = [os.path.join(pathToSub, p) for p in os.listdir(pathToSub) if not p in ['info.log', 'index.html', 'folder.jpg']]
                    pathsToPics = [p.replace('\\', '/') for p in pathsToPics]
                    # print '_'*50
                    # print pathsToPics
                    for pathToPic in pathsToPics:
                        galleryHTML = self.buildGalleryHTML(pathToPic)#mainGalleries out
                        try:
                            galleryPath = os.path.join(pathToPic, 'index.html')
                            galleryFile = open(galleryPath, 'w')
                            galleryFile.write(galleryHTML)
                            galleryFile.close()
                        except:
                            print 'Error saving the gallery %s'%pathToPic
                    # print'_'*50
                    # for folder in os.listdir(pathToSub):
                        
                    
                    self.log(pathToSub)
                    print '_'*30
                    print '\tDone for %s and log updated\n\n' %pathToSub.split('/')[-1]
                    
                elif self.logDiff(pathToSub) == False:
                    print '\tNo diff found in %s, hence no update of the HTML file' %pathToSub
                    print '_'*30

    def buildSubGalleryHTML(self, dirs):
        '''
            Creates the HTML output for the subgallery
        '''
        output = ''
        beginSubPath = os.path.join(self.__rootHTML, 'beginSub.html')

        beginFile = open(beginSubPath, 'r')

        for line in beginFile.readlines():
            output += line
        output = self.breadCrumb(dirs, 'sub')
        for d in dirs:
            path        = d
            name        = d.split('/')[-1]
            thumbPath   = d.split('photos/')[-1]
            if len(d.split('/')) == 3:
                path = path.split('/')[-1]
            
            p = './'+path #path to the link and folder.jpeg

            output += '''<li>
                <a href='%s/index.html'><em>%s</em><span></span><img src='%s/folder.jpg'  alt='No thumbnail found' /></a>
            </li>\n''' % (p, name, p)
        # print output
        endFilePath = os.path.join(self.__rootHTML, 'end.html')
        endFile = open(endFilePath, 'r')
        for line in endFile.readlines():
            output += line
        beginFile.close()
        endFile.close()
        return output

    def breadCrumb(self, dirs, type):
        '''
            Creates the breadCrumbs links for a given page
            To be called before saving HTML files
        '''
        TYPES = ['main', 'sub', 'Gall']
        print dirs
        if not type in TYPES:
            return 'Wrong type passed'
        else:
            if type == 'sub':
                pBreadCrumb = os.path.join(self.__rootHTML, 'beginSub.html')
                f = open(pBreadCrumb, 'r')
                output = ''
                for l in f.readlines():
                    output += l
                for d in dirs:
                    print '*'*20
                    print d
                    print'*'*20
                    output = output.replace('{$Accueil$}', '<a href=\"../../index.html\">Accueil</a>')
                    output = output.replace('{$Sub$}', '>%s'%d)
                    output = output.replace('{$Gall$}', '')
                f.close()
                return output
            elif type == 'Gall':
                pBreadCrumb = os.path.join(self.__rootHTML, 'beginSub.html')
                f = open(pBreadCrumb, 'r')
                output = ''
                for l in f.readlines():
                    output += l
                
                output = output.replace('{$Accueil$}', '<a href=\"../../../index.html\">Accueil</a>')
                
                d = dirs.split(self.__rootPath)[-1]
                sub = d.split('/')[0]
                g = d.split('/')[-1]
                output = output.replace('{$Sub$}', '<a href=\"../../%s/index.html\"> > %s</a>'% (sub,sub))
                output = output.replace('{$Gall$}', ' > '+g)
                # print output
                f.close()
                return output

    #--------------
    def createGalleryIndexPage(self, path, force = False):
        if path == None:
            path = self.__rootPath
        else:
            path = path
        
        listGalleries = []
        mainGalleries = [f for f in os.listdir(path) if f!= 'info.log']
        
        # print mainGalleries
        
        for main in mainGalleries:
            pathToSub = os.path.join(path, main)
            print pathToSub
            subGalleries = [sub for sub in os.listdir(pathToSub) if not sub in ['index.html', 'info.log', 'folder.jpg']]
            print subGalleries
            for sub in subGalleries:
                sub = os.path.join(pathToSub, sub)
                listGalleries.append(sub)
        print listGalleries

    def buildGalleryHTML(self, pathToPics):
        '''
            Creates the HTML output for the subgallery
        '''
        output = ''

        beginSubPath = os.path.join(self.__rootHTML, 'beginSub.html')
        
        beginFile = open(beginSubPath, 'r')
        for line in beginFile.readlines():
            output += line
        output = self.breadCrumb(pathToPics, 'Gall')
        # output = self.breadCrumb(subs, 'Gall')
        pics = [p for p in os.listdir(pathToPics) if not p in ['info.log', 'index.html', 'folder.jpg']]
        for pic in pics:
            if not pic == 'folder.jpeg' or not pic == 'index.html':
                output += '''<li>
                                <a href=\"%s\" rel='lightbox[billeder]' title=''>
                                <span></span>
                                <img src=\"%s&amp;size=120\"' alt='No thumbs found' />
                                </a>
                                </li>\n''' % (pic, pic)
        # print output
        endFilePath = os.path.join(self.__rootHTML, 'end.html')
        endFile = open(endFilePath, 'r')
        for line in endFile.readlines():
            output += line
        beginFile.close()
        endFile.close()

        # !!! FIX : replace CSS
        output = output.replace('href="../../css', 'href="../../../css')
        output = output.replace('js/', '../../../js/')
        return output

g = GalleryGen()
# print g.breadCrumb(path, 'Gall')
g.createMainIndex(path, False)
g.createSubGalleryIndexPage(path, True)

