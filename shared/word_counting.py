"""Shared word counting and frequency analysis utilities."""

import re


def clean_word(word):
    """Normalize a word by lowercasing and removing punctuation."""
    word = word.lower()
    word = re.sub(r'[^\w\s]', '', word)
    return word.strip()


def count_words(file_path):
    """Read a file and return a dictionary of word frequencies."""
    word_freq = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for word in f.read().split():
            word = clean_word(word)
            if not word:
                continue
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
    return word_freq


def top_n_words(word_freq, n):
    """Return the top N most frequent words as a sorted list of (word, count) tuples."""
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:n]


def print_word_frequencies(word_freq, top_n=None):
    """Print word frequencies, optionally limited to top N."""
    if top_n:
        items = top_n_words(word_freq, top_n)
    else:
        items = word_freq.items()

    for i, (word, count) in enumerate(items, 1):
        print(f"{i}. {word} - {count} times")
