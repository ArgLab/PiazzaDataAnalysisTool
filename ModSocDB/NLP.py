#!/usr/bin/env python
"""
NLP.py
:Author: Collin F. Lynch
:Date: 1/07/2015

This code provides for basic NLP capabilities within the library
and will pre-construct and pre-train some relevant taggers and
tokenizers for the work.
"""

# ============================================================
# Imports.
# ============================================================

import string
import nltk.tokenize
import nltk.tag
import name_tools

# ============================================================
# People Finding.
# ============================================================

def findPeopleInText(Text):
    """
    Given a block of text find all individuals tagged as a
    person from it.  This uses code inspired by:
    http://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk

    It will first construct a list of sentence tokens from
    the text and then for each sentence it will perform a word
    tokenization and use part of speech tagging to identify
    persons.  Those will then be returned as a list.

    This relies on the POS tagger to find subtrees that are
    named entities.
    """
    Result = []
    
    # Iterate over sentences in the text extracting a list of
    # tokenized words from the list.  Then for each word extract
    # the relevant subtrees and return the text sets by type.  
    Sents = nltk.tokenize.sent_tokenize(Text)

    for Sentence in Sents:

        Words = nltk.tokenize.word_tokenize(Sentence)
        Pos   = nltk.tag.pos_tag(Words)
        Tree  = nltk.chunk.ne_chunk(Pos, binary=True)
                
        for Subtree in Tree.subtrees():
            print Subtree
            if (Subtree.node == "NE"):
                NewName = [M[0] for M in Subtree.leaves()]
                Result.append(NewName)

    return Result
                



# def findNameInText(Name, Text):
#     """
#     Given a real name represented as a string search for it or the
#     components of it within a piece of text.  This will try to use
#     canonicalization to check for related elements but basically
#     relies on a form of string parsing to chunk the text and to
#     locate similar names.
#     """
#     # Tokenizer = nltk.tokenize.TreebankWordTokenizer()
#     Result = []

#     # Generate the split name that will be used for matching the
#     # individual words.
#     CanonicalName = name_tools.canonicalize(Name)
#     SplitName     = name_tools.split(CanonicalName)
#     FirstName     = SplitName[1]
#     LastName      = SplitName[2]
    
#     # Iterate over sentences in the text extracting a list of
#     # tokenized words from the list.  Then for each word extract
#     # the relevant subtrees.  These subtrees will then be searched
#     # for a match with the individual name using 
#     Sents = nltk.tokenize.sent_tokenize(Text)

#     for Sentence in Sents:

#         Words    = nltk.tokenize.word_tokenize(Sentence)
#         Pos      = nltk.tag.pos_tag(Words)
#         Tree     = nltk.chunk.ne_chunk(Pos, binary=False)
#         StrIndex = 0

#         # Having collected the named entities within the
#         # this code will iterate over them finding them
#         # in the string and copying with replacement into
#         # the replacement text.  
#         for Entity in Tree.subtrees(filter=lambda T: (T.node != "S")):

#             # If we have a singleton entity, that is a tree with one leaf
#             # then we extract the word from it and 
#             Word = Words[WordIdx]
#             WordPos = Pos[WordIdx][1]
#             StrIndex = Text.find(Word, StrIndex)
            
            
#         for Subtree in Tree.subtrees():
#             print Subtree
#             if (Subtree.node == "NE"):
#                 NewName = [M[0] for M in Subtree.leaves()]
#                 Result.append(NewName)

#     return Result


def findNameInText(Name, Text):
    """
    Given a real name represented as a string search for it or the
    components of it within a piece of text.  This will try to use
    canonicalization to check for related elements but basically
    relies on a form of string parsing to chunk the text and to
    locate similar names.
    """
    # Tokenizer = nltk.tokenize.TreebankWordTokenizer()
    Result = []

    # Generate the split name that will be used for matching the
    # individual words.
    CanonicalName = name_tools.canonicalize(Name)
    SplitName     = name_tools.split(CanonicalName)
    FirstName     = SplitName[1]
    LastName      = SplitName[2]
    
    # Iterate over sentences in the text extracting a list of
    # tokenized words from the list.  Then for each word extract
    # the relevant subtrees.  These subtrees will then be searched
    # for a match with the individual name using 
    Sents = nltk.tokenize.sent_tokenize(Text)

    for Sentence in Sents:

        Words    = nltk.tokenize.word_tokenize(Sentence)
        Pos      = nltk.tag.pos_tag(Words)
        # Tree     = nltk.chunk.ne_chunk(Pos, binary=False)
        StrIndex = 0

        # Having collected the named entities within the
        # this code will iterate over them finding them
        # in the string and copying with replacement into
        # the replacement text.  
        # for Entity in Tree.subtrees(filter=lambda T: (T.node != "S")):
        for WordIdx in range(len(Words)):

            # Extract the actual word and POS tags for the word
            # being evaluated. 
            Word = Words[WordIdx]
            WordPos = Pos[WordIdx][1]
            StrIndex = Text.find(Word, StrIndex)

            # Now if the word is one of the NN elements check if it
            # matches either the first or last name of the split
            # name.  In that case we will later replace.
            if ((len(WordPos) > 2) and (WordPos[:2] == "NN")):
                
                if (Word == FirstName):
                    print "Testing Name: %s %s  MATCHED FirstName" \
                      % (Word.encode("UTF-8"), WordPos)
                elif (Word == LastName):
                    print "Testing Name: %s %s  MATCHED LastName" \
                      % (Word.encode("UTF-8"), WordPos)
                # else: print "Testing Name: %s %s No Match" % (Word.encode("UTF-8"), WordPos)




def replaceNameInText(FirstName, LastName, FirstNameRep, LastNameRep, Text):
    """
    Given a FirstName and a LastName, this code will find all instances
    of either one in the text and will then replace them with the
    supplied replacement strings.  It will then make the replacement
    and return the resulting string.

    If no changes are made to the text then this code will return
    None.  Else it will return an updated form of the text. 

    If either name is None then no change will be made for replacement.
    If both names are None then this will simply return None at the outset.
    """
    # Handle the both None case before doing anything else.
    if (FirstName == None) and (LastName == None): return None
    
    # Tokenizer = nltk.tokenize.TreebankWordTokenizer()
    ResultStr = ""
    StrIndex = 0
    StartIndex = 0
    ChangeFlag = False
    
    # Iterate over sentences in the text extracting a list of
    # tokenized words from the list.  Then for each word extract
    # the relevant subtrees.  These subtrees will then be searched
    # for a match with the individual name using 
    Sents = nltk.tokenize.sent_tokenize(Text)

    for Sentence in Sents:
        # print "Checking Sentence: %s" % (Sentence.encode("UTF-8"))
        
        Words    = nltk.tokenize.word_tokenize(Sentence)
        Pos      = nltk.tag.pos_tag(Words)
        # Tree     = nltk.chunk.ne_chunk(Pos, binary=False)
        
        # Having collected the named entities within the
        # this code will iterate over them finding them
        # in the string and copying with replacement into
        # the replacement text.  
        # for Entity in Tree.subtrees(filter=lambda T: (T.node != "S")):
        for WordIdx in range(len(Words) - 1):

            # Extract the actual word and POS tags for the word
            # being evaluated. 
            Word = Words[WordIdx]
            WordPos = Pos[WordIdx][1]
            StrIndex = Text.find(Word, StartIndex)

            # At this point if the StrIndex differs from the Start
            # Index then we need to copy in the differing space.
            # This may be ignored words or other text but it must
            # be added to the result string.
            if (StrIndex > StartIndex):
                ResultStr += Text[StartIndex:StrIndex]
                StartIndex = StrIndex
            
            # Now if the word is one of the NN elements check if it
            # matches either the first or last name of the split
            # name.  In that case we will later replace.
            #
            # If either one matches then we append the replacement
            # text in lieu of the matched word and increment the
            # indicies accordingly. 
            if ((len(WordPos) > 2) and (WordPos[:2] == "NN")):
                
                if (FirstName != None) and (Word == FirstName):
                    #print "Testing Name: %s %s  MATCHED FirstName" \
                    #  % (Word.encode("UTF-8"), WordPos)

                    ChangeFlag = True
                    ResultStr += FirstNameRep
                                      
                elif (LastName != None) and (Word == LastName):
                    #print "Testing Name: %s %s  MATCHED LastName" \
                    #  % (Word.encode("UTF-8"), WordPos)

                    ChangeFlag = True
                    ResultStr += LastNameRep
                

                # Else if it does not match then copy in the word and move
                # on. 
                else:
                    #print "Testing Name: %s %s No Match" \
                    #  % (Word.encode("UTF-8"), WordPos)

                    ResultStr += Word

                # Increment the start index to the end of the word
                # and continue.  
                StartIndex = StrIndex + len(Word)


    # At this point we have copied over every word although
    # there may be tail content after the last word that we
    # need to include so that will be done here.
    #
    # If changes were made then the updated text will be
    # returned else we will return None.
    if (ChangeFlag == False): return None
    else: return ResultStr + Text[StartIndex:]

        
# def findNamesInText(Text):
#     """
#     Given a real name represented as a string search for it or the
#     components of it within a piece of text.  This will try to use
#     canonicalization to check for related elements but basically
#     relies on a form of string parsing to chunk the text and to
#     locate similar names.
#     """
#     # Tokenizer = nltk.tokenize.TreebankWordTokenizer()
#     Result = []

#     # Generate the split name that will be used for matching the
#     # individual words.
#     CanonicalName = name_tools.canonicalize(Name)
#     SplitName     = name_tools.split(CanonicalName)
#     FirstName     = SplitName[1]
#     LastName      = SplitName[2]
    
#     # Iterate over sentences in the text extracting a list of
#     # tokenized words from the list.  Then for each word extract
#     # the relevant subtrees.  These subtrees will then be searched
#     # for a match with the individual name using 
#     Sents = nltk.tokenize.sent_tokenize(Text)

#     for Sentence in Sents:

#         Words    = nltk.tokenize.word_tokenize(Sentence)
#         Pos      = nltk.tag.pos_tag(Words)
#         # Tree     = nltk.chunk.ne_chunk(Pos, binary=False)
#         StrIndex = 0

#         # Having collected the named entities within the
#         # this code will iterate over them finding them
#         # in the string and copying with replacement into
#         # the replacement text.  
#         for Entity in Tree.subtrees(filter=lambda T: (T.node != "S")):

#             # Flatten the entity to get the contents.
#             FlatEnt = Entity.flatten()
            
#             # If we have a singleton entity, that is a tree with one leaf
#             # then we extract the word from it and return that.
            
#             Word = Words[WordIdx]
#             WordPos = Pos[WordIdx][1]
#             StrIndex = Text.find(Word, StrIndex)
            
            
#         for Subtree in Tree.subtrees():
#             print Subtree
#             if (Subtree.node == "NE"):
#                 NewName = [M[0] for M in Subtree.leaves()]
#                 Result.append(NewName)

#     return Result





# ============================================================
# Name Chunking.
# ============================================================

def makeSplitNameDict(Name, Canonicalize=True):
    """
    Given a name as a single string this code will split it into a
    dict containing named name components.  More specifically it
    will return a dict with the fields: Honorific (e.g. Dr.),
    FirstName, MiddleName, LastName, and Postfix (e.g. Jr.).

    If Canonicalize is True (default) then the name will be
    canonicalized before it is split.

    This code relies on the name_tools library for canonicalization
    and name splitting.
    """

    # Perform any necessary canonicalization.
    if (Canonicalize == False): CurrName = Name
    else: CurrName = name_tools.canonicalize(Name)

    # Now perform the split and build up the dict
    # for all but the personal name.
    Split = name_tools.split(CurrName)

    ResultDict = {
        "Honorific" : Split[0],
        "Postfix"   : Split[3]
        }

    PersonalName = Split[1]
    LastName     = Split[2]

    
    # Now parse out the Middle name if it is present.
    # If the personal name (First+Middle) is empty
    # then we have a one name person and set that as
    # the First Name in the dict while setting the
    # middle and last to None.  If it is not empty
    # then just set the LastName and move on.
    if (PersonalName == ''):
        ResultDict["FirstName"]  = LastName
        ResultDict["MiddleName"] = None
        ResultDict["LastName"]   = None
        return ResultDict

    else: ResultDict["LastName"] = LastName

    # Now split the Personal name to extract first and middle
    # Names and set them if present.
    PersonalSplit = string.split(PersonalName, maxsplit=1)
    # print PersonalSplit
    ResultDict["FirstName"] = PersonalSplit[0]
    if (len(PersonalSplit) > 1):
        ResultDict["MiddleName"] = PersonalSplit[1]
    else: ResultDict["MiddleName"] = None

    return ResultDict
