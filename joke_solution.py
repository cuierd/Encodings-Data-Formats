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

        self.xml_repr = self._get_xml_repr()
        self.json_repr = self._get_json_repr()

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
        joke_node = etree.Element('joke')
        text_node = etree.SubElement(joke_node, 'text')
        text_node.text = self.joke
        author_node = etree.SubElement(joke_node, 'author')
        author_node.text = self.author
        link_node = etree.SubElement(joke_node, 'link')
        link_node.text = self.link
        rating_node = etree.SubElement(joke_node, 'rating')
        rating_node.text = str(self.rating)
        time_node = etree.SubElement(joke_node, 'time')
        time_node.text = self.time
        profanities_node = etree.SubElement(joke_node, 'profanity_score')
        profanities_node.text = str(self.num_profanities)
        return joke_node

    def _get_json_repr(self) -> Dict:
        return {'author': self.author, 'link': self.link, 'text': self.joke, 'rating': self.rating, 'time': self.time,
                'profanity_score': self.num_profanities}

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
        if self.filename.endswith('.csv'):
            with open(self.filename, "r") as lines:
                lines = csv.reader(lines, delimiter=',')
                jokes = [Joke(row) for row in lines]
                return jokes
        elif self.filename.endswith('.json'):
            with open(self.filename, "r") as infile:
                jokes_dict = json.load(infile)
                return [Joke(list(joke.values())[:-1]) for joke in jokes_dict.values()]
        else:
            raise Warning('unsupported file type')

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
        root = etree.Element('jokes')
        for joke in self.jokes:
            root.append(joke.xml_repr)
        xml_bytes = etree.tostring(
            root, encoding='UTF-8', pretty_print=True, xml_declaration=True)
        xml_str = xml_bytes.decode("utf-8")

        with open(outfile, 'w', encoding='utf-8') as file:
            file.write(xml_str)

    def save_jokes_json(self, outfile: str) -> None:
        """Save all the jokes of the Generator in their json representation to the outfile"""
        jokes = {index+1: joke.json_repr for index, joke in enumerate(self.jokes)}
        for index, joke in enumerate(self.jokes):
            json_repr = joke.json_repr
            jokes[index+1] = json_repr
        with open(outfile, 'w', encoding='utf-8') as file:
            json.dump(jokes, file, indent=4)


if __name__ == "__main__":
    gen = JokeGenerator("reddit_dadjokes.csv")
    gen.save_jokes_xml('reddit_dadjokes.xml')
    gen.save_jokes_json('reddit_dadjokes.json')

    gen_json = gen = JokeGenerator("reddit_dadjokes.json")
    gen_json.random_joke()
