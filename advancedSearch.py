#!/usr/bin/env python3

import core
import fnmatch
import os
import yaml
from termcolor import colored

RULES = yaml.safe_load(open('rules.yaml'))
FILETYPE = RULES['filetype']
FILETYPE_WEIGHT = RULES['filetype_weight']
GREP_WORDS = RULES['grep_words']
GREP_WORD_OCCURRENCE = RULES['grep_word_occurrence']
GREP_WORDS_WEIGHT = RULES['grep_words_weight']


class AdvancedSearch(object):

    def __init__(self):
        self._FILETYPE = FILETYPE
        self._FILETYPE_WEIGHT = FILETYPE_WEIGHT
        self._GREP_WORDS = GREP_WORDS
        self._GREP_WORD_OCCURRENCE = GREP_WORD_OCCURRENCE
        self._GREP_WORDS_WEIGHT = GREP_WORDS_WEIGHT
        self._OCCURRANCE_COUNTER = 0
        self._FINAL_WEIGHT = 0
        self._EXIST = True
        self.words = []

    def grepper(self, word):
        for search_expression in self._GREP_WORDS:

            if fnmatch.fnmatch(word.lower(), search_expression):
                self._OCCURRANCE_COUNTER += 1
                self.words.append(word)

        if self._OCCURRANCE_COUNTER >= self._GREP_WORD_OCCURRENCE:
            self._FINAL_WEIGHT += self._GREP_WORDS_WEIGHT

    def filetype_check(self, _file):
        file_name, extension = os.path.splitext(_file)
        for ext in self._FILETYPE:

            if fnmatch.fnmatch(extension, ext):
                self._FINAL_WEIGHT += self._FILETYPE_WEIGHT

    def final(self, _file, data):
        if self._FINAL_WEIGHT >= 10:

            print(colored("INTERESTING FILE HAS BEEN FOUND!!!", 'cyan'))
            print(colored("The rule defined in 'rules.yaml' file has been "
                  + "triggerred. Checkout the file " + _file + " for words: " + str(self.words), 'cyan'))
            core.logger.info("the rule defined in 'rules.yaml' file has been "
                             + "triggerred while analyzing file " + _file + " for words: " + str(self.words))
            data.append({"Finding": "Advanced rule triggerred", "File": _file,
                        "Details": {"filetype": self._FILETYPE,
                                    "filetype_weight": self._FILETYPE_WEIGHT,
                                    "grep_words": self._GREP_WORDS,
                                    "found_words":self.words,
                                    "grep_word_occurrence": self._GREP_WORD_OCCURRENCE,
                                    "grep_words_weight": self._GREP_WORDS_WEIGHT}})

            return True
        else:
            return False
