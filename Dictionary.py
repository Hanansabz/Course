import sys

def read_file_content_to_dictionary(file_name):
    with open(file_name) as file:
        d = {}
        for line in file:
            splitted_line = line.split()
            for word in splitted_line:
                if word in d:
                    d[word] += 1
                else:
                    d[word] = 1
        return d

def sort_dictionary_by_value(d, n):
    l = sorted(d.items(), key=lambda item: item[1], reverse=True)
    l = l[:n] # Keep only the top n items
    sorted_d = dict(l) # Convert the list of tuples back to a dictionary
    return sorted_d

if __name__ == "__main__":
    if len(sys.argv) > 1:
        n = int(sys.argv[1])   #type into terminal: python Dictionary.py 10 to display the top 10 words for example 
    else:
        print("Please provide the number of top words to display as a command-line argument.")

    import os
    file_name = os.path.join(os.path.dirname(__file__), "Storytext.txt")
    d = read_file_content_to_dictionary(file_name)
    sorted_d = sort_dictionary_by_value(d, n)
    for key, value in sorted_d.items():
        print(f"Word: {key} Appears {value} times")

