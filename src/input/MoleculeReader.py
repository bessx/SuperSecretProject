from pathlib import Path

from rdkit import Chem
from rdkit import RDLogger

from SuperSecretProject.src.representation import Molecule
from SuperSecretProject.src.utilities import constants
from SuperSecretProject.unittests import utilities
from SuperSecretProject.src.utilities import logging

# TODO: move to utilities
def fileToString(file):
    """
        Read the entire contents of a file into a string

        @input: file -- valid path to a file
    """
    contents = ""
    with open(file) as f:
        contents = f.read()
    f.close()

    # if file.suffix == '.mol2':
    #     return readMol2File(file, contents)

    return contents


def convertToRDkit(contents, extension):
    """
        Attempt to read and convert the input file into an RdKit.Mol object
        
        @input: contents -- string contents of a file
        @input: mol)file -- input molecule file name
    """
    #Chem.doKekule = False
    
    if (extension == constants.FASTA_FORMAT_EXT):
        return Chem.MolFromFASTA(contents) 

    if (extension == constants.YAML_FORMAT_EXT):
        return Chem.MolFromHELM(contents) 

    if (extension == constants.MOL2_FORMAT_EXT):
        # return Chem.MolFromMol2Block(contents)
        return readMol2File(contents)

    if (extension == constants.MOL_FORMAT_EXT):
        return Chem.MolFromMolBlock(contents)

    if (extension == constants.PDB_FORMAT_EXT):
        return Chem.MolFromPDBBlock(contents) 

    if (extension == constants.SMARTS_FORMAT_EXT):
        return Chem.MolFromSmarts(contents) 

    if (extension == constants.SMILES_FORMAT_EXT):
        return Chem.MolFromSmiles(contents)

    if (extension == constants.TPL_FORMAT_EXT):
        return Chem.MolFromTPLBlock(contents)

    return None

def readMol2File(contents):
    # Turn off rdkit error messages 
    RDLogger.DisableLog('rdApp.*')

    try: 
        return Chem.MolFromMol2Block(contents)
    except:
        pass
    try: 
         return Chem.MolFromMol2Block(contents, kekulize = False)
    except:
        pass
    try: 
         return Chem.MolFromMol2Block(contents, kekulize = False, sanitize = False)
    except:
        pass
    try: 
         return Chem.MolFromMol2Block(contents, sanitize = False)
    except:
        pass
    try: 
        return Chem.MolFromMol2Block(contents, sanitize = False, removeHs = False)
    except: 
        pass
    try: 
        return Chem.MolFromMol2Block(contents, sanitize = False, removeHs = False, cleanupSubstructures = False)
    except: 
        pass

def getMolecules(files):
    """
        From the set of input files, acquire the corresponding Rdkit molecules.
        
        @input: 
        @output: Molecule objects (each containing an Rdkit.Mol object)
    """
    mols = []

    for current_file in files:

        # get the contents of the file and the file type (extension) for processing
        file_contents = fileToString(current_file)
          
        # Attempt to interpret the molecule
        mol = None
        try:
            mol = convertToRDkit(file_contents, current_file.suffix)
        except:
            logging.logger.error(f'RDKit failed to read {current_file.name}')

        # add it to our dataset and update the filenames we have
        if mol is not None:
            mols.append(Molecule.Molecule(mol, current_file.name))
   
    return mols