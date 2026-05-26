
def count_words_in_file(file_path):
    count = {}
    for w in open(file_path).read().split():
        w = take_off_punctuation(w)
        if w in count:
            count[w] += 1
        else:
            count[w] = 1
    for word, times in count.items():
        print("{} was found {} times".format(word, times))

def take_off_punctuation(word):
    word = word.lower()
    return word.strip(" . , ! ` ? ' () : ; -- ")
 
def top_words_in_file(file_path, n):
    print("Top {n} words in {file_path} were:".format(n=n, file_path=file_path))
    count = {}
    for w in open(file_path).read().split():
        w = take_off_punctuation(w)
        if w in count:
            count[w] += 1
        else:
            count[w] = 1
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    for word, times in sorted_count[:n]:
        print(" {} was found {} times".format(word, times))


file_path = "alice.txt"
count_words_in_file(file_path)

input("Press Enter to see the top 10 words in the file...")
top_words_in_file(file_path, 10)

input("Press Enter to exit...")