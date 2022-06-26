# Exercise 4
Hand in until **April 26th**.

## Introduction

This exercise is about encodings and data formats. You will have a look at different formats, think about their advantages and disadvantages, and learn how to convert from one to the other (and back).

Please use modules from Python’s standard library only, unless it is stated otherwise in the exercise description.


### GitLab

To submit your code, use GitLab. Have a look at the instructions on ```OLAT > Material > Tutorial > instructions.pdf``` if you're unsure how to submit your work.


### To Submit

* ```joke.py``` with all your implemented functions for Task 1
* ``` reddit_dadjokes.xml```  containing all jokes from reddit_dadjokes.csv in XML representation
* ``` reddit_dadjokes.json```  containing all jokes from reddit_dadjokes.csv in JSON representation
* ```task_2.py``` with the functions you used to convert the encodings in Task 2
* ```encoding_utf-8.txt``` containing all the jokes from Task 2 in *utf-8* encoding
* ```task_3.txt``` with your answers to the questions in Task 3

It is **mandatory** to work in pairs. If you have no partner, please contact us so we can set you up with someone. Before submitting, make sure all your code runs and your repository contains all the files you need to hand in.


## Task 1: XML and JSON

In this task you will extend the Joke and JokeGenerator classes to save their attributes
in XML or JSON representation.

### Task 1.1: Saving XML representation

Implement the function `def _get_xml_repr(self) -> etree.Element:` of the Joke class.
It should return a lxml element (for a tutorial on lxml click [here](https://lxml.de/tutorial.html)) called _joke_ containing
all attributes as subelements, which will be saved as an attribute in the init method.
The following could be an example for such a XML representation:

```xml
<joke>
    <text>Doctor: "So, you're telling me that you have a problem with one of your ears. Are you sure?" Me: "YES Doctor,  I'm definite. "</text>
    <author>VERBERD</author>
    <link>https://old.reddit.com/r/dadjokes/comments/rvzg8l/doctor_so_youre_telling_me_that_you_have_a/</link>
    <rating>1</rating>
    <time>04.01.22 17:16</time>
    <profanity_score>0</profanity_score>
  </joke>
```
For combining and saving all jokes of the reddit_dadjokes.csv file, implement the function ``def save_jokes_xml(self, outfile: str) -> None:``
of the JokeGenerator class. This function will introduce a new superelement called _jokes_ with all the joke nodes as subelements.
A pretty printed version including a XML declaration should then be saved inside the provided outfile called _reddit_dadjokes.xml_.
Take a look at the following example of what the output inside your file should look like:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<jokes>
  <joke>
    <text>Doctor: "So, you're telling me that you have a problem with one of your ears. Are you sure?" Me: "YES Doctor,  I'm definite. "</text>
    <author>VERBERD</author>
    <link>https://old.reddit.com/r/dadjokes/comments/rvzg8l/doctor_so_youre_telling_me_that_you_have_a/</link>
    <rating>1</rating>
    <time>04.01.22 17:16</time>
    <profanity_score>0</profanity_score>
  </joke>
  <joke>
    <text>A grizzly kept talking to me and annoyed me He was unbearable</text>
    <author>MHSPres</author>
    <link>https://old.reddit.com/r/dadjokes/comments/rvzf8h/a_grizzly_kept_talking_to_me_and_annoyed_me/</link>
    <rating>1</rating>
    <time>04.01.22 17:14</time>
    <profanity_score>0</profanity_score>
  </joke>
...
</jokes>
```

#### Outcome
* Your implementation for `def _get_xml_repr(self) -> etree.Element:` and ``def save_jokes_xml(self, outfile: str) -> None:``
* The file reddit_dadjokes.xml containing all jokes from reddit_dadjokes.csv in XML representation

### Task 1.2: Saving JSON representation
The goal of this task is similar to Task 1.1, however this time the attributes of the Joke class should be saved using a
JSON representation. To achieve this, you will need to implement the function `_get_json_repr(self) -> Dict:` of the Joke
class, which will return a dictionary containing all attributes. Do not forget to store the outcome of the function inside
the init method of the Joke class. As an example, take a look at the following joke:

```JSON
{
    "author": "VERBERD",
    "link": "https://old.reddit.com/r/dadjokes/comments/rvzg8l/doctor_so_youre_telling_me_that_you_have_a/",
    "text": "Doctor: \"So, you're telling me that you have a problem with one of your ears. Are you sure?\" Me: \"YES Doctor,  I'm definite. \"",
    "rating": 1,
    "time": "04.01.22 17:16",
    "profanity_score": 0
  }
```
For combining and saving all jokes of the reddit_dadjokes.csv file, implement the function ``def save_jokes_json(self, outfile: str) -> None:`` of the JokeGenerator class. This function will
introduce a new dictionary containing all the jokes from the jokes attribute. The indices (starting from 1) taken from the jokes attribute
list should be the keys of this jokes dictionary and the individual JSON representations of the jokes stored in their init method
should be the values. Consider example.json as an example file. Save your json representation inside the file _reddit_dadjokes.json_.

#### Outcome
* Your implementation for `def _get_json_repr(self) -> etree.Element:` and ``def save_jokes_json(self, outfile: str) -> None:``
* The file reddit_dadjokes.json containing all jokes from reddit_dadjokes.csv in JSON representation

### Task 1.3: Instantiating the JokeGenerator with a JSON file
For this task you will adept the ``make_jokes_objects(self)`` method from the JokeGenerator class so that it will also 
accept files containing jokes in a JSON representation. The method should still return a list containing all the jokes from
the file as Joke objects, so that no changes outside the function have to be made. If you could not solve Task 1.2, then
feel free to use the provided _example.json_ as an example input. If you managed to solve the task, then please use your
own _reddit_dadjokes.json_ from the previous subtask.

#### Outcome
* Your implementation for ``make_jokes_objects(self)``



## Task 2: Encodings

So far you've mostly worked with the *utf-8* encoding. But not every file you encounter will be encoded in the same way, and might even use an encoding you really hate. In this task, you will convert two files with different encodings into *utf-8*.

You recieve two files, ```encoding_1.txt``` and ```encoding_2.txt```. One is encoded in [ISO 8859-1](https://www.charset.org/charsets/iso-8859-1), the other in [ASCII](https://en.wikipedia.org/wiki/ASCII#Printable_characters). 

For this exercise, you will have to:

* find out which file is in which encoding
* convert both files to *utf-8* and save them to the same file called ```encoding_utf-8.txt```

**Hint**: Once you know in what encoding a file is saved in, you only need the file read, write and append methods from the python standard library in order to convert it. :)


### Outcome
* a python file named ```task_2.py``` with the functions you used to convert the encodings
* a *.txt* file named ```encoding_utf-8.txt``` containing all the jokes from ```encoding_1.txt``` and ```encoding_2.txt``` in *utf-8* encoding.



## Task 3: Text Formats

[CSV](https://simple.wikipedia.org/wiki/Comma-separated_values), [JSON](https://simple.wikipedia.org/wiki/JSON) and [XML](https://simple.wikipedia.org/wiki/XML) are three different text formats you have worked with so far. If you need a quick refresher on what they look like and what they do, have a look at the hyperlinks. Consider what each format is suitable for and what might be a problem when using it. Feel free to compare them to each other to make your point.

a) List one advantage and one disadvantage for each of the data formats (XML, JSON, CSV). \
b) Please give us a short feedback about the exercise. How long did it take you to solve the tasks? What did you struggle with, what was easy? Did you gain any new knowledge by solving the exercises?


### Outcome
* Your answers to a) and b) in a separate text file named ```task_3.txt```.



## Data Sources
```dadjokes_samples.txt```: https://www.kaggle.com/oktayozturk010/reddit-dad-jokes

```profanities.txt```: https://www.freewebheaders.com/full-list-of-bad-words-banned-by-google/
