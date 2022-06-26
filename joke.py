#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# University of Zurich
# Department of Computational Linguistics

# Authors: Cui Ding(olatname: cding)
# Matriculation Numbers: 21-718-945
# 			Mia Tatjana Egli (olatname: miaegl)
# Matriculation Numbers: 21-700-406

import time
from typing import List, Tuple, Dict
import re
import random
import csv
from lxml import etree
import json


class Joke:
    """The Joke object contains the joke, and some metadata on that joke. One can compare the jokes by upvotes"""
    def __init__(self, raw_joke):
        self.raw_joke = raw_joke
        self.author = self.raw_joke[0]
        self.link = self.raw_joke[1]
        self.joke = self.raw_joke[2]
        self.rating = int(self.raw_joke[3])
        self.time = self.raw_joke[4]

        self.sentences_joke = self.split_into_sentences()
        self.tokenized_joke = self._tokenize()
        self.filtered_joke = self.filter_profanity()[0]
        self.num_profanities = self.filter_profanity()[1]

        # TODO: Save representations in xml and json
        self.joke_repr_x = self._get_xml_repr()
        self.joke_repr_j = self._get_json_repr()
        self.joke_repr_sj = ''                  # It is not that necessary

    def split_into_sentences(self) -> List[str]:
        """Split text into sentences"""
        output = re.findall(r' ?([^.!?\n]+[.?!]*|\n)', self.joke)
        return output

    def _tokenize(self) -> List[List[str]]:
        """Tokenize all the words in the sentences"""
        output = []
        for sentence in self.sentences_joke:
            tokenized_sentence = re.findall(r'([\w\']+|\?|\.|\n|,|!)', sentence)
            output.append(tokenized_sentence)
        return output

    def filter_profanity(self, filename="profanities.txt") -> Tuple[List[List[str]], int]:
        """Filter out all the profanity"""

        output = []

        # Count number of profanities
        num_profanities = 0

        # Read in profanity file
        with open(filename, "r")as file:
            profanities = file.read().split("\n")

        for sentence in self.tokenized_joke:
            no_profanity = True
            text_sentence = " ".join(sentence)
            for profanity in profanities:

                # Check if there is profanity in the sentence
                if profanity in text_sentence:
                    profanity_in_text = True
                else:
                    profanity_in_text = False

                while profanity_in_text:
                    num_profanities += 1
                    no_profanity = False

                    # Find the index of the profanity
                    index = text_sentence.index(profanity)
                    front = text_sentence[:index - 1]

                    # Find the words that need to be replaced
                    num_words_before_profanity = len(front.split(" "))
                    num_profanity_words = len(profanity.split(" "))
                    profanity_in_sentence = sentence[num_words_before_profanity: num_words_before_profanity + num_profanity_words]

                    # Replace the profanity with '#'
                    replacement = ["#" * len(word) for word in profanity_in_sentence]

                    # Construct new sentence composed of the parts with and without profanity
                    new_sent = []
                    new_sent.extend(sentence[:num_words_before_profanity])
                    new_sent.extend(replacement)
                    new_sent.extend(sentence[num_words_before_profanity + len(replacement):])
                    text_sentence = " ".join(new_sent)
                    sentence = new_sent

                    # Check if there is still profanity in the sentence
                    if profanity in text_sentence:
                        profanity_in_text = True

                    else:
                        profanity_in_text = False
                        output.append(new_sent)

            # Add sentence immediately if there are no profanities in the sentence
            if no_profanity:
                output.append(sentence)
        return output, num_profanities

    def tell_joke(self):
        if len(self.filtered_joke) > 1:
            build_up = self.filtered_joke[:-1]
            punch_line = self.filtered_joke[-1:]

            print(self.pretty_print(build_up))
            time.sleep(1)
            print(self.pretty_print(punch_line))
        else:
            print(self.pretty_print(self.filtered_joke))

    @staticmethod
    def pretty_print(joke) -> str:
        """Print in a humanly readable way"""
        output = ""
        for sentence in joke:
            output += " ".join(sentence) + " "
        return output

    def _get_xml_repr(self) -> etree.Element:
        """Get the xml representation of the Joke with all its attributes as nodes"""
        parent = etree.Element("joke")
        etree.SubElement(parent, "text").text = self.joke
        etree.SubElement(parent, "author").text = self.author
        etree.SubElement(parent, "link").text = self.link
        etree.SubElement(parent, "rating").text = str(self.rating)
        etree.SubElement(parent, "time").text = self.time
        etree.SubElement(parent, "profanity_score").text = str(self.num_profanities)
        joke_bytes = etree.tostring(parent, encoding='utf-8')
        joke = joke_bytes.decode('utf-8')
        return joke

    def _get_json_repr(self) -> Dict:
        """Get the json representation of the Joke with all its attributes as nodes"""
        joke_hash = dict()
        joke_hash['author'] = self.author
        joke_hash['link'] = self.link
        joke_hash['text'] = self.joke
        joke_hash['rating'] = self.rating
        joke_hash['time'] = self.time
        joke_hash['profanity_score'] = self.num_profanities
        joke = json.dumps(joke_hash, indent=2)
        self.joke_repr_sj = joke
        jj_dict = json.loads(joke)
        return jj_dict

    def __repr__(self):
        """Allows for printing"""
        return self.pretty_print(self.filtered_joke)

    def __eq__(self, other):
        """Equal rating"""
        return self.rating == other.rating

    def __lt__(self, other):
        """less than rating"""
        return self.rating > other.rating

    def __gt__(self, other):
        """greater than rating"""
        return self.rating < other.rating

    def __le__(self, other):
        """less than or equal rating"""
        return self.rating >= other.rating

    def __ge__(self, other):
        """greater than or equal rating"""
        return self.rating <= other.rating


class JokeGenerator:
    def __init__(self, filename="reddit_dadjokes.csv"):
        self.filename = filename
        self.jokes = self.make_jokes_objects()

    def make_jokes_objects(self):
        """Accept .json or .csv file, generate Joke objects from them."""
        with open(self.filename, "r") as infile:
            if self.filename.endswith(".csv"):
                lines = csv.reader(infile, delimiter=',')
            else:
                json_data = json.load(infile)
                lines = []
                for joke_id in json_data.keys():
                    line = [json_data[joke_id][header] for header in json_data[joke_id].keys()]
                    lines.append(line)
            jokes = [Joke(row) for row in lines]
            return jokes

    def generate_jokes(self):
        for joke in self.jokes:
            if len(joke.filtered_joke) > 1:
                joke.tell_joke()
            time.sleep(10)

    def random_joke(self):
        joke = random.sample(self.jokes, 1)[0]
        joke.tell_joke()

    def save_jokes_xml(self, outfile: str) -> None:
        """Save all the jokes of the Generator in their xml representation to the outfile"""
        with open(outfile, 'w', encoding='utf-8') as tf:
            root = etree.Element("jokes")
            for joke_obj in self.jokes:
                parent = etree.fromstring(joke_obj.joke_repr_x.encode('utf-8'))
                root.append(parent)
            jokes = etree.tostring(root, encoding='UTF-8', pretty_print=True, xml_declaration=True).decode('utf-8')
            tf.write(jokes)
        return None

    def save_jokes_json(self, outfile: str) -> None:
        """Save all the jokes of the Generator in their json representation to the outfile"""
        with open(outfile, 'w') as tf:
            jokes_hash = dict()
            i = 0
            for joke_obj in self.jokes:
                # we didn't find "the indices (starting from 1) taken from the jokes attribute list"
                # so we assigned a local variable i
                i += 1
                jokes_hash[i] = joke_obj.joke_repr_j
            json.dump(jokes_hash, tf, indent=2)
        return None


if __name__ == "__main__":
    # You can use the following commands for testing your implementation
    gen = JokeGenerator("reddit_dadjokes.csv")
    gen.save_jokes_xml('reddit_dadjokes.xml')
    gen.save_jokes_json('reddit_dadjokes.json')

    gen_json = gen = JokeGenerator("reddit_dadjokes.json")
    gen_json.random_joke()
    
    
    
    
    
def edit_distance(target_list: List[str], source_list: List[str]) -> int:
    # imagine a matrix, the first row is "#" plus the target list
    # the first column is "#" plus the source list
    m = len(target_list)
    n = len(source_list)
    grid = {}
    for j in range(n):
        if j == 0:
            for i in range(m):
                if i == 0:
                    grid[(j, i)] = 0
                else:
                    grid[(j, i)] = 3.0 * int(i)
        else:
            for i in range(m):
                if i == 0:
                    grid[(j, i)] = 2.0 * int(j)
                else:
                    left_neigh = grid[(j, i-1)]
                    upper_neigh = grid[(j-1, i)]
                    diagonal_neigh = grid[(j-1, i-1)]
                    minimum = min(left_neigh, upper_neigh, diagonal_neigh)

                    if source_list[j] == target_list[i]:
                        grid[(j, i)] = minimum
                    else:
                        if ((j < n-1) or (i < m-1)) and (j > i):
                            grid[(j, i)] = minimum + 2.0
                        elif ((j < n-1) or (i < m-1)) and (j < i):
                            grid[(j, i)] = minimum + 3.0
                        else:
                            if source_list[j].isdigit() and target_list[i].isdigit():
                                grid[(j, i)] = minimum + 0.5
                            elif (source_list[j] in string.punctuation) and (target_list[i] in string.punctuation):
                                grid[(j, i)] = minimum + 0.1
                            elif (not source_list[j].isascii()) or (not target_list[i].isascii()):
                                grid[(j, i)] = minimum + 4.0
                            else:
                                grid[(j, i)] = minimum + 1.3
    return round(grid[(n-1, m-1)], 1)
