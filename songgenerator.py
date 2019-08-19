import nltk
from nltk.util import bigrams
from nltk import FreqDist
import random
import re
import sys

def collect_bigrams(file):
	with open(file, 'r') as f:
		data = f.readlines()
	bigrams_ = []
	for line in data:
		tok_line = []
		for w in nltk.word_tokenize(line):
			if not re.findall(r"(\.|,|\-|\?|\!|;|:|\"|'|\(|\)')+", w) and w!="\n":
				tok_line.append(w)
		bigrams_.extend(list(bigrams(tok_line, pad_right=True, right_pad_symbol='.',
					                   pad_left=True, left_pad_symbol='<**>')))
	return bigrams_

def get_most_common_bigram(word, bigrams_):
	w_bigrams = [b for b in bigrams_ if b[0] == word]
	freq_bigrams = [b[0] for b in FreqDist(w_bigrams).most_common(11)]
	freq_bigrams = [b for b in freq_bigrams if b != ('<**>', '.')]
	if len(freq_bigrams) == 11:
		freq_bigrams.remove(freq_bigrams[-1])
	try:
		return random.choice(freq_bigrams)
	except IndexError:
		return None

def generate_line(first_word, bigrams_):
	line_length = random.randint(3,11)
	line = [first_word,]
	for i in range(line_length):
		if line[-1] != ".":
			next_bigram = get_most_common_bigram(line[-1], bigrams_)
		else:
			line[0] = line[0].capitalize()
			line = " ".join(line)
			return line
		line.append(next_bigram[1])
	line[0] = line[0].capitalize()
	line = " ".join(line)
	return line
	
def pretty_line(line):
	line = line.strip("<**>")
	line = line.strip(" ")
	line = line.rstrip(".")
	line = re.sub(r" ([',?!.]|n't|na)", r"\1", line)
	return line + "\n"

def generate_song(first_word, file):
	song = ""
	bigrams_ = collect_bigrams(file)
	first_line = generate_line(first_word, bigrams_)
	first_line = pretty_line(first_line)
	song += first_line
	for i in range(9):
		line = generate_line("<**>", bigrams_)
		line = pretty_line(line)
		song += line
	print (song)
	


# print(generate_song("devil", "/media/my_disk/programming/cl_school/summer-school-2019/students/olga/lyrics_cof.txt"))

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print ("Usage: python3 " + sys.argv[0] + " \"First word\" \"Lyrics corpus file\"")
	else:
		try:
			generate_song(sys.argv[1], sys.argv[2])
		except TypeError:
			print("First word not found. Please try again.")
		except Exception as e:
			print(e)
