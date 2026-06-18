from shared.word_counting import count_words, top_n_words


def count_words_in_file(file_path):
    word_freq = count_words(file_path)
    for word, times in word_freq.items():
        print("{} was found {} times".format(word, times))


def top_words_in_file(file_path, n):
    print("Top {n} words in {file_path} were:".format(n=n, file_path=file_path))
    word_freq = count_words(file_path)
    for word, times in top_n_words(word_freq, n):
        print(" {} was found {} times".format(word, times))


file_path = "alice.txt"
count_words_in_file(file_path)

input("Press Enter to see the top 10 words in the file...")
top_words_in_file(file_path, 10)

input("Press Enter to exit...")
