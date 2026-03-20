# 1.Keywords play an important role when reading a long text to understand the subject and context of the text
# 2.Search engines also analyze an article’s keywords before indexing it. In this article
# 3.In this PROGRAMME, I will walk you through how to extract keywords using Python.

from rake_nltk import Rake

text_paragraph = """ The reason why paragraphs should be “headlined” with reference to the overall
argument is to keep that argument in the reader’s mind, thereby making it easier for them to see the relevance of the rest of the paragraph.
This way, the reader doesn’t lose track, and neither do you as you write.
"""     
r = Rake()
r.extract_keywords_from_text(text_paragraph)
keywords = r.get_ranked_phrases()
# print(e) --> returns None
print(keywords)
             