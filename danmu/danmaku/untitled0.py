# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 23:03:38 2021

@author: 59154
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
example_text = "University College London, which operates as UCL, is a major public research university located in London, United Kingdom. UCL is a member institution of the federal University of London, and is the second-largest university in the United Kingdom by total enrolment[6] and is the largest by postgraduate enrolment. UCL is consistently ranked as one of the best universities in the world, and admission to its programmes is highly selective."
print(sent_tokenize(example_text))