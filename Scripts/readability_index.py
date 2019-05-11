# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
'''
    Reference: https://www.geeksforgeeks.org/readability-index-pythonnlp/
    Caution: this file is using python3.6!!!
'''
import spacy
from textstat.textstat import textstatistics, easy_word_set, legacy_round


# Splits the text into sentences, using
# Spacy's sentence segmentation which can
# be found at https://spacy.io/usage/spacy-101
def break_sentences(text):
    nlp = spacy.load('en')
    doc = nlp(text)
    return doc.sents


# Returns Number of Words in the text
def word_count(text):
    sentences = break_sentences(text)
    words = 0
    for sentence in sentences:
        words += len([token for token in sentence])
    return words


# Returns the number of sentences in the text
def sentence_count(text):
    sentences = break_sentences(text)
    return sum(1 for i in sentences)


# Returns average sentence length
def avg_sentence_length(text):
    words = word_count(text)
    sentences = sentence_count(text)
    average_sentence_length = float(words / sentences)
    return average_sentence_length


# Textstat is a python package, to calculate statistics from
# text to determine readability,
# complexity and grade level of a particular corpus.
# Package can be found at https://pypi.python.org/pypi/textstat
def syllables_count_func(word):
    return textstatistics().syllable_count(word)


# Returns the average number of syllables per
# word in the text
def avg_syllables_per_word(text):
    syllable = syllables_count_func(text)
    words = word_count(text)
    ASPW = float(syllable) / float(words)
    return legacy_round(ASPW, 1)


# Return total Difficult Words in a text
def difficult_words(text):
    # Find all words in the text
    words = []
    sentences = break_sentences(text)
    for sentence in sentences:
        words += [token for token in sentence]

        # difficult words are those with syllables >= 2
    # easy_word_set is provide by Textstat as
    # a list of common words
    diff_words_set = set()

    for word in words:
        syllable_count = syllables_count_func(str(word))
        if word not in easy_word_set and syllable_count >= 2:
            diff_words_set.add(word)

    return len(diff_words_set)


# A word is polysyllablic if it has more than 3 syllables
# this functions returns the number of all such words
# present in the text
def poly_syllable_count(text):
    count = 0
    words = []
    sentences = break_sentences(text)
    for sentence in sentences:
        words += [token for token in sentence]

    for word in words:
        syllable_count = syllables_count_func(word)
        if syllable_count >= 3:
            count += 1
    return count


def flesch_reading_ease(text):
    """
        Implements Flesch Formula:
        Reading Ease score = 206.835 - (1.015 × ASL) - (84.6 × ASW)
        Here,
          ASL = average sentence length (number of words
                divided by number of sentences)
          ASW = average word length in syllables (number of syllables
                divided by number of words)
    """
    FRE = 206.835 - float(1.015 * avg_sentence_length(text)) - \
          float(84.6 * avg_syllables_per_word(text))
    return legacy_round(FRE, 2)


def gunning_fog(text):
    per_diff_words = (difficult_words(text) / word_count(text) * 100) + 5
    grade = 0.4 * (avg_sentence_length(text) + per_diff_words)
    return grade


def smog_index(text):
    """
        Implements SMOG Formula / Grading
        SMOG grading = 3 + ?polysyllable count.
        Here,
           polysyllable count = number of words of more
          than two syllables in a sample of 30 sentences.
    """

    if sentence_count(text) >= 3:
        poly_syllab = poly_syllable_count(text)
        SMOG = (1.043 * (30 * (poly_syllab / sentence_count(text))) ** 0.5) \
               + 3.1291
        return legacy_round(SMOG, 1)
    else:
        return 0


def dale_chall_readability_score(text):
    """
        Implements Dale Challe Formula:
        Raw score = 0.1579*(PDW) + 0.0496*(ASL) + 3.6365
        Here,
            PDW = Percentage of difficult words.
            ASL = Average sentence length
    """
    words = word_count(text)
    # Number of words not termed as difficult words
    count = words - difficult_words(text)
    if words > 0:
        # Percentage of words not on difficult word list

        per = float(count) / float(words) * 100

    # diff_words stores percentage of difficult words
    diff_words = 100 - per

    raw_score = (0.1579 * diff_words) + \
                (0.0496 * avg_sentence_length(text))

    # If Percentage of Difficult Words is greater than 5 %, then;
    # Adjusted Score = Raw Score + 3.6365,
    # otherwise Adjusted Score = Raw Score

    if diff_words > 5:
        raw_score += 3.6365

    return legacy_round(raw_score, 2)

if __name__ == "__main__":

    my_sentences = []
    my_sentences.append("No, you cannot. I agree it could make code cleaner, but it is hard for us to grade your code since our submitter will not get your template. We may think out this way in the next semester.")
    my_sentences.append("You may want to use cost explorer. Bills may be a little bit delay.")
    my_sentences.append("Nginx daemonizing on startup by default would cause this issue, you can look for an option to turn this off. Switching off the default daemonizing behavior should work.")
    my_sentences.append("In short, a pod is a group of containers. A pod let their constituents, containers, share the data and communication. It's good practice to add modularity to application or service. It means it's very likely a group of containers will work together. They're not necessarily the same. But, they can share resources and communicate with each other.")
    my_sentences.append("Hi, the recording system encountered some errors today. But, I made another record after today's recitation. It should be able to release soon. Thanks for asking!")
    my_sentences.append("That's right. You see there were some unexpected cost in the Ohio. You can even see if it's tagged etc.")
    my_sentences.append("You should have both stdout and stderr. The feedback is not suggesting that the error is caused by exactly the line before.")
    my_sentences.append("Your output somehow changed to bytes literals. The usage of Popen() here may not be the problem.")
    my_sentences.append("It's good practice to tag all the resources. But, it's not required.")
    my_sentences.append("However, our project's goal is helping you improve you self-learning skills and ability to solve problems on your own. Hope you enjoy the process of tackling the issues!")
    my_sentences.append("Because the frontend in the GCP can access the backend in GCP with internal DNS. But, it cannot access Azure's backend with the same approach. So, you would like to start the Azure backend first and note down the ip.")
    my_sentences.append("We feel very sorry about this case. Because the spot instance tags used to be able to persist if added manually. Spot fleet can help automatically tag the spot instances.")
    for sentence in my_sentences:
        print(dale_chall_readability_score(sentence))
