#==============================================================================
# Common entity source class for world2vec project
#------------------------------------------------------------------------------
#
#
#------------------------------------------------------------------------------
from siqo_lib      import journal


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_INV  = '0123456789@#$§%^&*()°-_—=+<>"/„“\|’‘\''
_WRD  = ' ,;:.!?…\n\t'
_SNT  = '.!?…'

_EOF  = '_end_of_file_'
_ERR  = '_this_is_bad_'

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# class EntitySource
#------------------------------------------------------------------------------
class EntitySource():

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name, fname, enc = 'utf-8'):
        "Call constructor of EntitySource and initialise it"

        journal.I( 'EntitySource constructor for {}...'.format(name), 10 )
        
        self.name     = name      # unique name for particle in Your project
        self.fname    = fname     # filename of entity source
        self.state    = 'close'   # state of source
        
        self.posRaw   = 0         # number of readed character from file 
        self.posChar  = 0         # number of returned valid characters
        self.posWord  = 0         # number of returned words
        self.posSent  = 0         # number of returned sentences
        
        self.enc      = enc       # used encoding or page
        self.low      = True      # if raw input will be transformed into low
        
        self.inv      = set([char for char in _INV]) # invisible characters
        self.wrd      = set([char for char in _WRD]) # word's terminators
        self.snt      = set([char for char in _SNT]) # sentence's terminators
        
        #----------------------------------------------------------------------
        # file opening
        
        try   : 
            self.file  = open(self.fname, 'r', encoding = self.enc )
            self.state = 'open'
            journal.O( 'EntitySource {} created from {} '.format(self.name, self.fname), 10 )
            
        except: 
            self.file = False
            journal.O( 'EntitySource {} ERROR for "{}" '.format(self.name, self.fname), 9 )

    #==========================================================================
    # Tools for Source setting
    #--------------------------------------------------------------------------

    #==========================================================================
    # Tools for Source usage & navigation
    #--------------------------------------------------------------------------
    def nextVisible(self):
        "Return next visible character"
        
        while self.state == 'open':
            
            ch = self.file.read(1)
            self.posRaw += 1
            
            # if reached end of file
            if not ch:
                self.file.close()
                self.state = 'close'
                return _EOF
            
            if self.low: ch = ch.lower()
            
            # if is visible character
            if ch not in self.inv: return ch
        
        return '_ERR'
    
    #--------------------------------------------------------------------------
    def nextChar(self):
        "Return next visible non term character"
        
        # return next non term character
        while self.state == 'open':
            
            ch = self.nextVisible()
            if ch == _EOF: return _EOF
            
            if ch not in self.wrd: 
                self.posChar += 1
                return ch
        
        return _ERR
    
    #--------------------------------------------------------------------------
    def nextWord(self):
        "Return next word"
        
        # ziskam 1 validny znak
        word = self.nextChar()
        if word == _EOF : return _EOF
        
        # pridavam viditelne znaky az kym nenarazim na term
        while self.state == 'open':
            
            ch = self.nextVisible()
            if ch == _EOF: return word
            
            if ch not in self.wrd: word += ch
            else                 : 
                self.posWord += 1
                return word
            
        return _ERR
    
    #--------------------------------------------------------------------------
    def nextSentence(self):
        "Return next sentence"
        
        sent = []
        
        return sent

    #==========================================================================
    # Tools for extraction & persistency
    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json record for EntitySource"
        
        json = {'name':self.name }
        
        journal.M( 'EntitySource {} getJson created'.format(self.name), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def print(self):
        "Print EntitySource's properties"
        
        print( "EntitySource '{}' is from file '{}'".format(self.name, self.fname) )
        print( "=======================================================================" )
        
#------------------------------------------------------------------------------
print('EntitySource class ver 0.02')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
