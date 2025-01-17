
#This variable determines the largest fragment size that the program can handle
MaximumAtomicUnit = 300

def getMassSpectrumURL(URL):

    """
    This function will take the NISTWebbook Website URL of a particular molecule and extract the Mass Spectrum URL from that webpage
    INPUT: URL ( NISTWebbook URL of a specific molecule. Example: https://webbook.nist.gov/cgi/cbook.cgi?Name=Methanol&Units=SI )
    OUTPUT: mass_spec_url ( mass spectrum URL of that specific molecule )
    """
    import httplib2
    from bs4 import BeautifulSoup, SoupStrainer

    http = httplib2.Http()
    status, response = http.request(URL)

    all_links = BeautifulSoup(response, parse_only=SoupStrainer('a'), features='html.parser')

    for link in all_links:
        if link.has_attr('href'):
            value = link['href']
            if(value.find('#Mass-Spec')>0):
                domain = 'https://webbook.nist.gov'
                mass_spec_url = domain + value
                return mass_spec_url

def getJDXDownloadURL(mass_spectrum_url):

    """
    This function will take the mass spectrum url of a specific molecule and extract the "Download spectrum in JCAMP-DX format" URL
    INPUT: mass_spectrum_url ( Specific molecule's mass spectrum webpage's URL . Example : https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Units=SI&Mask=200#Mass-Spec )
    OUTPUT: download_url (Specific molecule's mass spectrum's JDX Format file download link. Example : https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C64175&Index=0&Type=Mass )
    """
    import httplib2
    from bs4 import BeautifulSoup, SoupStrainer

    http = httplib2.Http()
    status, response = http.request(mass_spectrum_url)

    all_links = BeautifulSoup(response, parse_only=SoupStrainer('a'), features='html.parser')

    for link in all_links:
        if link.has_attr('href'):
            value = link['href']
            if(value.find('JCAMP')>0):
                domain = 'https://webbook.nist.gov'
                download_url = domain + value
                return download_url

def getMolecularWeight(URL):

    """
    This function will take the specific molecule's NISTWebBook URL and fetch the Molecular weight value from that web page.
    INPUT: URL (specific molecule's NISTWebBook URL that contains the details of that molecule. Example: https://webbook.nist.gov/cgi/cbook.cgi?Name=Methanol&Units=SI ) 
    OUTPUT: molecularWeight ( the molecular weight value from the NISTWebBook page of the specific molecule. The value is in Float dataType )
    """
    import requests
    from bs4 import BeautifulSoup

    webpage = requests.get(URL) 
    soup = BeautifulSoup(webpage.content, "lxml")

    molecularWeight = soup.find("a", attrs={"title": 'IUPAC definition of relative molecular mass (molecular weight)'}).find_parent().nextSibling
    return float(molecularWeight)

def getMolecularFormula(URL):

    """
    This function will extract the Formula from the specific molecule's NISTWebBook URL.
    INPUT: URL (specific molecule's NISTWebBook URL that contains the details of that molecule. Example: https://webbook.nist.gov/cgi/cbook.cgi?Name=Methanol&Units=SI)
    OUTPUT: formula (extracted molecular formula string from the NISTWebBook URL)
    """
    import bs4
    import requests
    from bs4 import BeautifulSoup
    
    webpage = requests.get(URL) 
    soup = BeautifulSoup(webpage.content, "lxml")

    formula_tag = soup.find("a", attrs={"title": 'IUPAC definition of empirical formula'}).find_parent().next_siblings
    formula = ''
    for sib in formula_tag:                                                                                             #sib is the siblings inside formula_tag
        if(type(sib) == bs4.element.Tag):
            formula = formula +sib.text
        else:
            formula = formula + sib

    return formula

def getElectronNumbers(formula):

    """
    This function will take the molecular formula string and using the pymatgen's function to output the total electron number of the specific molecule.
    INPUT: formula ( molecular formula string of the specific molecule. Example: CH4 )
    OUTPUT: total_electrons ( total electron count of the specific molecule )
    """
    import pymatgen.core.composition

    comp = pymatgen.core.composition.Composition(formula)
    return comp.total_electrons

def getJDXDownloadURL(mass_spectrum_url):
    """
    This function will take in the URL of the mass spectrum webpage  of the specific molecule and extract the JDX download URL from that page.
    INPUT: mass_spectrum_url(specific molecule's mass spectrum webpage's URL)
    OUTPUT: mass_spec_url ( specific molecule's mass spectrum in JCAMP-DX format download URL)
    """
    import httplib2
    from bs4 import BeautifulSoup, SoupStrainer

    http = httplib2.Http()
    status, response = http.request(mass_spectrum_url)

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features='html.parser'):
        if link.has_attr('href'):
            value = link['href']
            if(value.find('JCAMP')>0):
                domain = 'https://webbook.nist.gov'
                mass_spec_url = domain + value
                return mass_spec_url

def getJDX(URL,molecule_name):

    """
    This function retrieves the JDX Formatted file of a specific molecule taking in the NISTWebBook URL and the molecule's name
    INPUT: URL (mass spectrum in JCAMP-DX format download URL) | molecule_name (specific molecule's name to name the jdx formatted file in the output directory)
    OUTPUT: returns the filename with the output directory path
    """
    import urllib.request
    import cgi

    # URL = "https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C67561&Index=0&Type=Mass"
    remotefile = urllib.request.urlopen(URL)
    remotefileName = remotefile.info()['Content-Disposition']
    value, params = cgi.parse_header(remotefileName)
    outputdirectory = "JDXFiles"
    filename = "%s\\%s" %(outputdirectory,molecule_name+".jdx")
    urllib.request.urlretrieve(URL, filename)
    return filename

def getOverAllArray(listOfFiles):
    
    import JCampSG

    OverallArray=[]
    holderArray=[]
    # for i in listOfFiles:
    jcampDict=JCampSG.JCAMP_reader(listOfFiles)
    holderArray=createArray(jcampDict)
    OverallArray=combineArray(OverallArray, holderArray)
    return OverallArray

def createArray(jcampDict):
    DataArray =[]

    counterY=0
    counter =0
    for number in jcampDict['x']:    
        counter = counter +1
        counterY2=0
        while counter != float(number):
        
            DataArray.append(0)
            #fileData.write('%f,'%zero)
            #fileData.write('\n')
            counter = counter +1 

        for number2 in jcampDict['y']:
            if counterY2 == counterY:
                
                DataArray.append(number2) 
                #fileData.write('%f,'%number2)
                #fileData.write('\n')
                #counterY2 =counterY2 + 1
                break;
            else:
                counterY2=counterY2 +1  

        counterY= counterY +1

    if len(DataArray) < MaximumAtomicUnit:
        for i in range(len(DataArray), MaximumAtomicUnit):
            DataArray.append(0)
    return DataArray

def combineArray(Array1, Array2):
    
    for i in range(MaximumAtomicUnit):
        Array1.append(Array2[i])
    
    
    return Array1

def getSpectrumDataFromLocalJDX(JDXFilesList):
    """
    This function will take in a JDX file and extract the spectrum data into a python Array
    INPUT: JDXFilesList(This must be a list of path+filename . Example : ['JDXFiles\\Ethanol.jdx','JDXFiles\\Methanol.jdx'])
    OUTPUT: AllSpectraData(Python list of spectrum data retrieved from the JDX)
    """
    
    import JCampSG

    AllSpectraData=[]
    individual_spectrum=[]
    for file in JDXFilesList:
        stripped_fileName = file.strip()
        if('.jdx' not in stripped_fileName):
            filename = stripped_fileName+'.jdx'
        else:
            filename = stripped_fileName

        jcampDict=JCampSG.JCAMP_reader(filename)
        individual_spectrum=createArray(jcampDict)
        AllSpectraData=combineArray(AllSpectraData, individual_spectrum)
    return AllSpectraData

def exportToCSV(filename, OverallArray, MoleculeNames, ENumbers, MWeights, knownMoleculeIonizationTypes, knownIonizationFactorsRelativeToN2, SourceOfFragmentationPatterns, SourceOfIonizationData, delimeter=';'):
    """
    This function basically takes in all the metadata of molecules and write them into csv file/files
    """
    import os.path

    if(os.path.exists(filename)):
        f5 = open(filename, 'w')
    else:
        directory_name = filename.split('\\')[0]
        if(not os.path.isdir(directory_name)):
            os.mkdir(directory_name)
        f5 = open(filename, 'w')

    f5.write('#CommentsLine:')
    for i in range(len(MoleculeNames)):
        f5.write(delimeter)
    f5.write('\n')
    
    #write the molecules
    f5.write('Molecules')
    for i in MoleculeNames:
        f5.write(f'{delimeter}{i}')
    f5.write('\n')

    #write the Electron Numbers
    f5.write('Electron Numbers')
    for i in ENumbers:
        f5.write(f"{delimeter}{float(i)}")
    # f5.write(str(ENumbers))
    f5.write('\n')
    
    #write the ionization type
    f5.write('knownMoleculesIonizationTypes')
    for i in knownMoleculeIonizationTypes:
        f5.write(f'{delimeter}{i}')
    f5.write('\n')
    
    #write the ionization factor
    f5.write('knownIonizationFactorsRelativeToN2')
    for i in knownIonizationFactorsRelativeToN2:
        f5.write(f'{delimeter}{i}')
    f5.write('\n')
    
    #write the header
    f5.write('SourceOfFragmentationPatterns')
    for i in SourceOfFragmentationPatterns:
        f5.write(f'{delimeter}{i}')
    f5.write('\n')
    
    #write the ionization data source
    f5.write("SourceOfIonizationData")
    for i in SourceOfIonizationData:
        f5.write(f'{delimeter}{i}')
    f5.write('\n')
    
    #write the molecular weights
    f5.write('Molecular Mass')
    for i in MWeights:
        f5.write(f'{delimeter}{float(i)}')
    # f5.write(str(MWeights))
    f5.write('\n')
    
    Array1=OverallArray
    printRow= len(Array1)//MaximumAtomicUnit #TODO: printRow is not a good variable name, this should be changed.
    printArray =[]
    zeros = True

    for i in range(1,MaximumAtomicUnit+1):
        zeros = True
        for k in range(printRow):
            if Array1[MaximumAtomicUnit*k +i-1] != 0: #The -1 is for array indexing
                zeros =False                
        if zeros == False:
            f5.write('%d'%(i))    
            for y in range(printRow):    
                f5.write(f'{delimeter}{int(Array1[MaximumAtomicUnit*y +i-1])}') #The -1 is for array indexing
            f5.write('\n')
            
    f5.close()

def takeInputAsList(molecule_name):
    """
    This function converts the user given molecule names separated by semicolon into a list of string
    INPUT: molecule_name(Molecule names in semicolon separated format. Example: Methane;Methanol;Ethane)
    OUTPUT: molecule_names(Molecule names in list of string format. Example: ['Methane','Methanol','Ethane'])
    """
    molecule_names = []
    molecule_name = molecule_name.split(';')
    for name in molecule_name:
        molecule_names.append(name)
    return molecule_names

def getMetaDataForMoleculeFromOnline(molecule_name):
    """
    This function takes in a specific molecule's name and return its meta data
    INPUT: dataBase_data_holder_for_specific_molecule (Python list of metadata that we get from the database CSV File) | molecule_name ( name of the molecule which meta data will be returned )
    OUTPUT: returns the molecular information of the specific molecule
    """
    try:
        url = f'https://webbook.nist.gov/cgi/cbook.cgi?Name={molecule_name}&Units=SI'

        molecular_formula = getMolecularFormula(url)
        molecular_weight = getMolecularWeight(url)
        electron_numbers = getElectronNumbers(molecular_formula)
    except:
        molecular_formula = 'unknown'
        molecular_weight = 'unknown'
        electron_numbers = 'unknown'

        #print(f'Metadata for {molecule_name} NOT FOUND in NIST Webbook. Molecular Formula, Molecular Weight & Electron Number are set to Unknown') #commenting this out because it can cause confusion to the user.
        

    return molecular_formula,molecular_weight,electron_numbers

def getSpectrumForMoleculeFromOnline(molecule_name):
    """
    This function will get the Spectrum data from Online source.
    INPUT: molecule_name ( Specific Molecule's Name which spectrum data the user want from online )
    OUTPUT: spectrum_data ( Data array containing the spectrum data from online ) | SourceOfFragmentationPattern ( As we are retrieving the data from online, it will be NIST Webbook in this case)
    """
    url = f'https://webbook.nist.gov/cgi/cbook.cgi?Name={molecule_name}&Units=SI'

    try:
        mass_spectrum_url = getMassSpectrumURL(url)
        jdx_download_url = getJDXDownloadURL(mass_spectrum_url)
        jdx_filename = getJDX(jdx_download_url,molecule_name)
        spectrum_data = getOverAllArray(jdx_filename)

        SourceOfFragmentationPattern = 'NIST Webbook'
    except:
        spectrum_data = [0] * MaximumAtomicUnit
        SourceOfFragmentationPattern = 'unknown'

        print(f'Spectrum data for {molecule_name} NOT FOUND in NIST Webbook. It is set to a blank list and SourceOfFragmentationPattern is set to unknown')

    return spectrum_data, SourceOfFragmentationPattern

def readFromLocalDatabaseFile(localDatabaseFileName, delimeter=';'):
    """
    This function will take the local database csv file name and return its content in a python list type variable.
    INPUT: localDatabaseFileName( Full path and name of the database file . Example: MoleculesInfo.csv. Example : Database//MoleculesInfo.csv)
    OUTPUT: 
    """
    import csv

    data_list = []
    #If the provided database file is a CSV formatted file, then it will open with the default encoding
    if('.csv' in localDatabaseFileName):
        spamReader = csv.reader(open(localDatabaseFileName), delimiter=delimeter)

    #Else if the provided database file is a TXT formatted file ( most likely tab delimeted ), then it will open with UTF-16 encoding.
    elif ('.txt' in localDatabaseFileName) or ('.tab' in localDatabaseFileName):
        spamReader = csv.reader(open(localDatabaseFileName,encoding='utf-16'), delimiter=delimeter)
    
    for row in spamReader:
        data_list.append(row)
    
    #the 'data_list' variable will contain all the rows in a list of the provided localDatabaseFileName
    return data_list

def getDataIfMoleculeExists(databaseDataHolderList, molecule_name):
    """
    This function will search inside the databaseDataHolderList if a certain molecule_name exists or not
    INPUT: databaseDataHolderList(contents in list format from MoleculesInfo.csv(default database csv file)) | molecule_name(user provided specific molecule's name)
    OUTPUT: datum ( the data list of the specific molecule name. If not found then empty list will be returned)
    """
    for datum in databaseDataHolderList:
        if(datum[0] == molecule_name): #The very first entry of each 1D list contains the Molecule Name inside the database file
            return datum
    return []

def checkInLocalJDXDirectory(localJDXFileDirectory, molecule_name):
    """
    This function will check inside the local directory where the JDX files are being kept if a particular molecule's JDX data exists there or not.
    INPUT: localJDXFileDirectory ( local JDX directory relative path according to this file. Example: 'JDXFiles//')
    OUTPUT: True/False (Depending on whether the molecule's jdx file exist inside that directory)
    """
    import os

    if(os.path.isdir(localJDXFileDirectory)):
        filesListInsideDirectory = os.listdir(localJDXFileDirectory)
        for filename in filesListInsideDirectory:
            corresponding_molecule_name_from_filename = filename.split('.')[0]
            if(corresponding_molecule_name_from_filename == molecule_name.lower()):
                return True
    return False

def takeMoleculeNamesInputFromUser (DataBase_data_holder):
    """
    This function will prompt the user to continuosly input molecule names and later it will process the inputs and return the total list of molecule names
    INPUT: DataBase_data_holder ( this will contain all the rows of the database file in case the user wants to convert all the molecules inside it )
    OUTPUT: MoleculeNames ( list of molecule names given by the user, it can be a list of single element. Example: ['Methanol', 'Propanol', 'Hexane'] )
    """
    MoleculeNames = []

    #print("If a molecule name has a comma in it (e.g. 1,3-pentadiene) or any other input has a comma in it, we recommend using an _ (e.g. 1_3-pentadiene) since this information is stored in a comma separated value file.")
    print("Press ENTER to automatically create converted spectra for all molecules inside the database specified. Otherwise, enter one or more molecule names, with multiple molecule names separated by ';'")
    moleculeName = input()

    #If the User press Enter, then we will retrieve all the molecule names from the database file
    if(moleculeName == ""):
        # RETRIEVE MOLECULE NAMES FROM DATABASE FILE
        for row in range(1,len(DataBase_data_holder)):
            MoleculeNames.append(DataBase_data_holder[row][0])
    #Else we will continuously prompt the user to input molecule names until they input END
    else:
        while True:
            #Taking continuous input of molecules from the user
            
            if(moleculeName.lower() == 'end'): break
            if(';' in moleculeName):
                MoleculeNames.extend(takeInputAsList(moleculeName))
            else:
                MoleculeNames.append(moleculeName)

            print("ENTER A MOLECULE NAME, OR MULTIPLE MOLECULE NAMES. Separate multiple names using ';'. or Type END to stope entering molecule name")
            moleculeName = input()
    
    return MoleculeNames

def getOutputFileName(outputDirectory, expectedFileName = 'ConvertedSpectra.csv', fileExtension='.csv'):
    """
    This function will check inside the outputDirectory and according to the output filename that exists inside the directory, it will generate the next file name
    INPUT: outputDirectory ( The directory where it will check for the output file. Example: 'OutputFiles//') | expectedFileName (this is an optional argument, the current function will search the directory based on its value ) | fileExtension ( Another optional argument, it will make the function modular for other file extensions.)
    OUTPUT: outputFileName ( Depending on the existing output filename, it will generate the next filename. Example: ConvertedSpectraX.csv )
    """
    import os
    
    #We will first check if the outputDirectory exists or not
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
        
    filesInsideOutputDirectory = os.listdir(outputDirectory) #All the Files list inside the output directory
    baseFileName = expectedFileName.split('.')[0]
    baseFileCounter = 0 #This is the X in ConvertedSpectraX.csv
    fileCountersList = list() #Initiated a list to store all the numbers appened in the files inside output directory

    #Now we will iterate through all the files and populate the fileCountersList. This will be used to get the max value of numbers in the files.
    for file in filesInsideOutputDirectory:
        #First we will check if the baseFilename is a part of the current file's name.
        if baseFileName not in file:
            continue
        #Now we will remove the file extension
        fileName_without_extension = file.split('.')[0]

        existing_number_in_filename = fileName_without_extension.split(baseFileName)[1]
        
        if (existing_number_in_filename.isnumeric()):
            fileCountersList.append(int(existing_number_in_filename))
    
    #Now we will get the max value for the new filename.
    if(len(fileCountersList) > 0):
        maxFileCounter = max(fileCountersList)
    else:
        #If the fileCountersList is empty, that means the existing file in the OutputDirectory is ConvertedSpectra.csv and the next one will be ConvertedSpectra1.csv
        maxFileCounter = baseFileCounter

    #Now we will increase the max counter by 1
    maxFileCounter = maxFileCounter + 1

    expectedFileName = f"{expectedFileName.split('.')[0]}{maxFileCounter}{fileExtension}"
    return expectedFileName

def startCommandLine(dataBaseFileName='MoleculesInfo.csv'):
    """
    Driver function for this application... #TODO: Functionalize this function more, Add more information to the comment section.
    """
    import os.path
    import csv
      
    SourceOfFragmentationPattern = ''
    SourceOfFragmentationPatterns = list()
    SourceOfIonizationDatum = ''
    SourceOfIonizationData = list()
    moleculeName=''
    MoleculeNames=list()
    ENumber = 0
    ENumbers =list()
    MWeight =0.0 
    MWeights=list()
    knownMoleculeIonizationType = ''
    knownMoleculeIonizationTypes = list()
    knownIonizationFactorRelativeToN2 = 0.0
    knownIonizationFactorsRelativeToN2 = list()
    filenames=''
    listOfFiles=list()
    AllSpectra=[]
    individual_spectrum=[]
    DataBase_data_holder=[]
    
    DataBase_data_holder = readFromLocalDatabaseFile(dataBaseFileName)


    fileYorN=''

    print("would you like to load molecular information from a csv file? Enter 'yes' or 'no'. If not, then you will enter files manually.")
    fileYorN=input()


    if (fileYorN =='no'):
        # print("If a molecule name has a comma in it (e.g. 1,3-pentadiene) or any other input has a comma in it, we recommend using an _ (e.g. 1_3-pentadiene) since this information is stored in a comma separated value file.")
        
        while True:
            print("Enter the molecule's Name(Type EXIT if you want to quit): ")
            moleculeName = input()
            if(moleculeName == 'EXIT'): break
            MoleculeNames.append(moleculeName)
            print("Retrieve info from NIST webbook? Y/N")
            WebbookChoice = input()
            if WebbookChoice.lower() == 'Y'.lower():
                spectrum_data,molecular_formula,molecular_weight,electron_numbers,knownMoleculeIonizationType, knownIonizationFactorRelativeToN2, SourceOfFragmentationPattern, SourceOfIonizationDatum = getMetaDataForMolecule(moleculeName)
                knownMoleculeIonizationTypes.append(knownMoleculeIonizationType)
                knownIonizationFactorsRelativeToN2.append(knownIonizationFactorRelativeToN2)
                SourceOfFragmentationPatterns.append(SourceOfFragmentationPattern)
                SourceOfIonizationData.append(SourceOfIonizationDatum)
                MWeights.append(molecular_weight)   
                ENumbers.append(electron_numbers)

                individual_spectrum.extend(spectrum_data)
                AllSpectra = combineArray(AllSpectra , individual_spectrum)

                print(f"RETRIEVED {moleculeName} from NIST WebBook")
 
            else:
        
                print(" enter the electron Number: ")
                ENumber = input()
                ENumbers.append(ENumber)
                print(" enter the molecule's ionization type (Enter unknown if unknown): ")
                knownMoleculeIonizationType = input()
                knownMoleculeIonizationTypes.append(knownMoleculeIonizationType)
                print(" enter the molecule's ionization factor relative to N2 (Enter a unknown if unknown): ")
                knownIonizationFactorRelativeToN2 = input()
                knownIonizationFactorsRelativeToN2.append(knownIonizationFactorRelativeToN2)
                print(" enter the source of the fragmention pattern: ")
                SourceOfFragmentationPattern = input()
                SourceOfFragmentationPatterns.append(SourceOfFragmentationPattern)
                print(" enter the source of the ionization data: ")
                SourceOfIonizationDatum = input()
                SourceOfIonizationData.append(SourceOfIonizationDatum)
                print(" enter the Molecular Weight:")
                MWeight= input()
                MWeights.append(MWeight)        
                print("enter the file name(EX: oxygen.jdx):")
                print("If the file is in a separate directory, \ninclude the path(EX: JDXFiles\oxygen.jdx):")
                filename=input()
                listOfFiles.append(filename)

                AllSpectra = getSpectrumDataFromLocalJDX(listOfFiles)

                print("Enter the name of the next molecule or type EXIT to finish entering molecules")
                moleculeName=input()

    elif(fileYorN=='yes'):
        fileInputName=''
        print("enter the file input name please:")
        fileInputName=input()
        #input_file ='attempt.csv'
        list_holder=[]
        spamReader = csv.reader(open('%s' %fileInputName), delimiter=',')
        for row in spamReader:
            list_holder.append(row)
            
            
    #The user is provided with the option to direct the functions output as they would like.  
    print("Would you like to specify an output location? If yes, type the path to the location. For default, hit enter.")
    outputDirectory = input()
    #If the user selects default, then the output is piped to "OutputFiles"
    if outputDirectory == "":
        outputDirectory = "OutputFiles"


    #mkaing the directory for exported files, if it isn't already there
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    #only if files exist to draw from
    if fileYorN == 'yes':
    #Checking if a directory exists to be drawn from
        if os.path.isdir("JDXFiles"):
        #This for loop draws from a directory of the user's choice (hard-coded)
            for i in range(1, len(list_holder)):
                
    # The below line has been added to allow the program to draw files from 
    # outside it's own directory.
                list_holder[i][3] = "JDXFiles\\" + list_holder[i][3]
        
                MoleculeNames.append(list_holder[i][0])
                ENumbers.append(list_holder[i][1])
                MWeights.append(list_holder[i][2])
                listOfFiles.append(list_holder[i][3])
                knownMoleculeIonizationTypes.append(list_holder[i][4])
                knownIonizationFactorsRelativeToN2.append(list_holder[i][5])
                SourceOfFragmentationPatterns.append(list_holder[i][6])
                SourceOfIonizationData.append(list_holder[i][7])
                
    #Otherwise, assume that the files are in the directory of the JDXConv-UI
        else:
        
    #This for loop draws files from the current directory
            for i in range(1, len(list_holder)):
                
                MoleculeNames.append(list_holder[i][0])
                ENumbers.append(list_holder[i][1])
                MWeights.append(list_holder[i][2])
                listOfFiles.append(list_holder[i][3])
                knownMoleculeIonizationTypes.append(list_holder[i][4])
                knownIonizationFactorsRelativeToN2.append(list_holder[i][5])
                SourceOfFragmentationPatterns.append(list_holder[i][6])
                SourceOfIonizationData.append(list_holder[i][7])

        #This outer If block handles the manual file selection logic from Local path, so adding this spectrumData Fetching at the end of this IF block.        
        AllSpectra = getSpectrumDataFromLocalJDX(listOfFiles)

    exportToCSV("%s\\ConvertedSpectra.csv" %outputDirectory, AllSpectra,  MoleculeNames, ENumbers, MWeights, knownMoleculeIonizationTypes, knownIonizationFactorsRelativeToN2, SourceOfFragmentationPatterns, SourceOfIonizationData)

def startCommandLineInterface(dataBaseFileName='MoleculesInfo.csv', JDXFilesLocation='JDXFiles//', delimeter=","):
    """
    This function will start the JDX Converter application and handle the user/app flow. #TODO: The function name will be renamed later accordingly.
    """
    import os

    #Initialized some variable variable
    SourceOfFragmentationPattern = ''
    SourcesOfFragmentationPattern = list()
    SourceOfIonizationDatum = ''
    SourceOfIonizationData = list()
    ENumber = 0
    ENumbers =list()
    MWeight =0.0 
    MWeights=list()
    knownMoleculeIonizationType = ''
    knownMoleculeIonizationTypes = list()
    knownIonizationFactorRelativeToN2 = 0.0
    knownIonizationFactorsRelativeToN2 = list()
    JDXfilename=''
    listOfJDXFileNames=list()
    AllSpectra=[]
    individual_spectrum=[]

    MoleculeNames=list()
    DataBase_data_holder=[]

    outputFileDirectoryPath = 'OutputFiles' #This is by default the output file directory path
    defaultOutputFileName = 'ConvertedSpectra.csv'
    print("****JDXConverter Started:****")
    #Prompting the user to choose the database file
    print('Press ENTER to use default database file (MoleculesInfo.csv). Otherwise, input "csv" for MoleculesInfo.csv or "txt" for (MoleculesInfoTable.txt) or "tab" for (MoleculesInfoTable.tab).')
    databaseFileChoice = input()

    #If the user inputs txt, then we will take the MoleculesInfoTable.txt file as our database file
    if(databaseFileChoice == "txt"):
        dataBaseFileName = "MoleculesInfoTable.txt"
        delimeter = '\t'
    elif(databaseFileChoice == "tab"):
        dataBaseFileName = "MoleculesInfoTable.tab"
        delimeter = '\t'
    else:
        dataBaseFileName = "MoleculesInfo.csv"
        delimeter = ';' 
    #Else it will be remain as MoleculesInfo.csv file as the default database file

    #Reading the information from database file
    #print(f"LOADING Information from {dataBaseFileName}")
    DataBase_data_holder = readFromLocalDatabaseFile(dataBaseFileName, delimeter=delimeter) #This variable will contain the full list or data of the CSV file in the link : https://github.com/AdityaSavara/JDX_Converter/blob/master/MoleculesInfo.csv
   
    #Starting text for the application , also instructions for the User to start
    MoleculeNames = takeMoleculeNamesInputFromUser(DataBase_data_holder) #MoleculeNames is a list of molecule names, provided by the user. The DataBase_data_holder is passed into this function in case the user wants to convert all the molecules from the database.
    
    for moleculeName in MoleculeNames:    
        JDXfilename = moleculeName #Default value for JDXFilename will be the molecule name, if the database has a filename specified inside it, we will replace it later.
        #Getting the Data list if the Molecule name exists inside the database CSV file
        molecule_meta_data_from_database = getDataIfMoleculeExists(DataBase_data_holder , moleculeName) #getDataIfMoleculeExists will return the existing metadata inside the database_data_holder

        molecule_final_meta_data = [''] * 8 # Indices will contain , 0: moleculeName, 1: ENumber, 2: MWeight, 3: JDXFileName , 4: knownMoleculesIonizationTypes, 5: knownIonizationFactorsRelativeToN2, 6: SourceOfFragmentationPatterns, 7: SourceOfIonizationData
        molecule_final_meta_data_status = [False] * 8

        #Now We will check if the molecule's data exist inside the database file
        if (len(molecule_meta_data_from_database) != 0):
            #Molecule FOUND inside the DATABASE FILE
            #TODO: Populating these variables can be a function itself
            
            #Now we will check if there's a jdx filename specified inside the database CSV file for the molecule
            filenameFromDatabase = molecule_meta_data_from_database[3].strip()
            if(filenameFromDatabase != ''):
                if(filenameFromDatabase in os.listdir(JDXFilesLocation)):
                    JDXfilename = JDXFilesLocation + filenameFromDatabase
                    individual_spectrum = getSpectrumDataFromLocalJDX([JDXfilename])
                    SourceOfFragmentationPattern = molecule_meta_data_from_database[6]
                else:
                    #This line will get all the data from online along with the individual spectrum data for the molecule. However we will only use the Spectrum data in this case
                    spectrum_data, SourceOfFragmentationPatternOnline = getSpectrumForMoleculeFromOnline(moleculeName)
                    individual_spectrum = spectrum_data
                    SourceOfFragmentationPattern = SourceOfFragmentationPatternOnline

            #Now we will check if any of the values inside the database is blank or unknown
            for datum in molecule_meta_data_from_database:
                metadata_index = molecule_meta_data_from_database.index(datum)
                if(datum == '' or datum == 'unknown'):
                    molecule_final_meta_data_status[metadata_index] = False
                else:
                    molecule_final_meta_data[metadata_index] = datum
                    molecule_final_meta_data_status[metadata_index] = True

            #Now we will check if the Unknown values are retrievable from online or not
            if False in molecule_final_meta_data_status:
                #We will only try to retrieve the data from online only if they are retrievable from online. Such data exist inside the first 3 indices.
                #We will consider the data after index three is not retrievable from online.
                molecular_formula_online , Mass_online, Electrons_online = getMetaDataForMoleculeFromOnline(moleculeName)
                for index in range(1,8): #looping over the indices of the data/metadata, index 0 is skipped because that is the molecule name
                    if((index == 1) and (molecule_final_meta_data_status[index] == False)):
                        molecule_final_meta_data[index] = Electrons_online
                    elif(index == 2 and (molecule_final_meta_data_status[index] == False)):
                        molecule_final_meta_data[index] = Mass_online
                    elif(molecule_final_meta_data_status[index] == False):
                        molecule_final_meta_data[index] = 'unknown'

            #This block will populate the necessary variables with the metadata from the database CSV file
            ENumber = int(molecule_final_meta_data[1])
            MWeight = float(molecule_final_meta_data[2])
            knownMoleculeIonizationType = molecule_final_meta_data[4]
            knownIonizationFactorRelativeToN2 = molecule_final_meta_data[5]
            SourceOfIonizationDatum = molecule_final_meta_data[7]

        #Now we will check if the corresponding JDX file for the molecule exists in the local directory or not
        elif(checkInLocalJDXDirectory(JDXFilesLocation, JDXfilename)):
            #Now we will retrieve the spectrum information from the local JDX file
            JDXFilePathWithName = JDXFilesLocation + JDXfilename
            individual_spectrum = getSpectrumDataFromLocalJDX([JDXFilePathWithName])
            
            #As the metadata for the molecule is not present inside the database csv file, we will now retrieve them from online
            molecular_formula,molecular_weight,electron_number = getMetaDataForMoleculeFromOnline(moleculeName)
            ENumber = int(electron_number)
            MWeight = float(molecular_weight)
            knownMoleculeIonizationType = 'unknown'
            knownIonizationFactorRelativeToN2 = 'unknown'
            SourceOfFragmentationPattern = SourceOfFragmentationPatternOnline
            SourceOfIonizationDatum = 'unknown'

        #Otherwise we will get all the metadata + spectrum data from online
        else:
            molecular_formula,molecular_weight,electron_number = getMetaDataForMoleculeFromOnline(moleculeName)
            spectrum_data, SourceOfFragmentationPatternOnline = getSpectrumForMoleculeFromOnline(moleculeName)
            
            if electron_number is not 'unknown':
                ENumber = int(electron_number)
            else:
                ENumber = 0
            
            if molecular_weight is not 'unknown':
                MWeight = float(molecular_weight)
            else:
                MWeight = 0

            knownMoleculeIonizationType = 'unknown'
            knownIonizationFactorRelativeToN2 = 'unknown'
            SourceOfFragmentationPattern = SourceOfFragmentationPatternOnline
            SourceOfIonizationDatum = 'unknown'

            individual_spectrum = spectrum_data
        
        #Now we will add all the spectrum data and metadata into list like variables which will be passed into the exportToCSV function
        #These variables are the implied returns of this functions and we will keep populating them as long as the user keeps giving molecule names. 
        #These variables will hold all the metadata and spectrum data all together for all the molecules and pass them into the exportTOCSV function
        ENumbers.append(ENumber)
        MWeights.append(MWeight)
        listOfJDXFileNames.append(JDXfilename)
        knownMoleculeIonizationTypes.append(knownMoleculeIonizationType)
        knownIonizationFactorsRelativeToN2.append(knownIonizationFactorRelativeToN2)
        SourcesOfFragmentationPattern.append(SourceOfFragmentationPattern)
        SourceOfIonizationData.append(SourceOfIonizationDatum)

        AllSpectra = combineArray(AllSpectra,individual_spectrum)

    #mkaing the directory for exported files, if it isn't already there
    if not os.path.exists(outputFileDirectoryPath):
        os.makedirs(outputFileDirectoryPath)
   
    #Now we will get the appropriate file name for the output. The OutputFiles will have a number at the end which is 1 or higher and the lowest number will be used.
    outputFileNameCSV = getOutputFileName(outputFileDirectoryPath)
    outputFileNameTXT = getOutputFileName(outputFileDirectoryPath, expectedFileName='ConvertedSpectraTable.txt', fileExtension='.txt')
    outputFileNameTAB = getOutputFileName(outputFileDirectoryPath, expectedFileName='ConvertedSpectraTable.tab', fileExtension='.tab')

    #Now we have all the implied returns of this function and now we will call the exportToCSV function to write all the metadata and spectrum data to the csv file
    OutputfilePathAndName = f"{outputFileDirectoryPath}\\{outputFileNameCSV}"
    exportToCSV(OutputfilePathAndName , AllSpectra, MoleculeNames , ENumbers , MWeights , knownMoleculeIonizationTypes , knownIonizationFactorsRelativeToN2 , SourcesOfFragmentationPattern , SourceOfIonizationData, delimeter=';')

    OutputfilePathAndName = f"{outputFileDirectoryPath}\\{outputFileNameTXT}"
    exportToCSV(OutputfilePathAndName , AllSpectra, MoleculeNames , ENumbers , MWeights , knownMoleculeIonizationTypes , knownIonizationFactorsRelativeToN2 , SourcesOfFragmentationPattern , SourceOfIonizationData, delimeter='\t')

    OutputfilePathAndName = f"{outputFileDirectoryPath}\\{outputFileNameTAB}"
    exportToCSV(OutputfilePathAndName , AllSpectra, MoleculeNames , ENumbers , MWeights , knownMoleculeIonizationTypes , knownIonizationFactorsRelativeToN2 , SourcesOfFragmentationPattern , SourceOfIonizationData, delimeter='\t')

    #Now this function will terminate showing the user where the output has been written
    print(f"Conversion complete: outputs written in ./{outputFileDirectoryPath}/{outputFileNameCSV}, ./{outputFileDirectoryPath}/{outputFileNameTXT}, and /{outputFileDirectoryPath}/{outputFileNameTAB}")

if __name__ == "__main__":
    # getMultipleSpectrumFromNIST()
    
    # startCommandLine()
    # checkInLocalJDXDirectory('JDXFiles//','Ethanol')
    # print(takeMoleculeNamesInputFromUser())
    # print(getOutputFileName('OutputFiles//'))
    startCommandLineInterface()