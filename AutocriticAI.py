import streamlit as st
import re
import language_tool_python
import string

from textstat import flesch_reading_ease, flesch_kincaid_grade
from spellchecker import SpellChecker
from transformers import pipeline

def calculate_readability(text):
    reading_ease = flesch_reading_ease(text)
    grade_level = flesch_kincaid_grade(text)
    return reading_ease, grade_level

def check_spelling(text):
    spell = SpellChecker()
    text_no_punct = text.translate(str.maketrans('', '', string.punctuation))
    words = text_no_punct.split()
    misspelled = spell.unknown(words)
    
    for word in misspelled:
        st.write(f"Misspelled word: {word}")
        suggestions = spell.candidates(word)
        if suggestions:
            st.write(f"Suggestions: {suggestions}")
            best_suggestion = suggestions.pop()
            st.write(f"Best suggestion: {best_suggestion}")
        else:
            st.write("No suggestions available.")


def summary(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(texet, max_length=150, min_length=50, do_sample=False)
    st.write("Summary:", summary[0]['summary_text'])

def grade_essay(text):
    reading_ease, grade_level = calculate_readability(text)
    st.write(f"Reading Ease Score: {reading_ease}")
    st.write(f"Grade Level: {grade_level:.2f}")
    check_spelling(text)
    summary(text)

st.title('AutocriticAI')

essay = st.text_area('Enter your essay here:', height=200)

if st.button('Grade Essay'):
    if essay:
        grade_essay(essay)
    else:
        st.write("Please enter an essay before grading.")