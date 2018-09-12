# GensimSimilarityIndexing
Prompt: 

How well or poorly does part-of-speech or syntactic dependency selection change/improve/destroy the effectiveness of some method of measuring the similarity between texts?  For example, if I drop everything but the nouns, and then compare texts via, say, gensim's similarity indexing, what happens?  

Corpuses:
-	Shakespeare’s plays 
-	1900-09 Top Fiction Bestsellers ( https://www.ocf.berkeley.edu/~immer/books1900s )
		
Mary Johnston, To Have and To Hold
		Winston Churchill, The Crisis
Owen Wister, The Virginian
Mary Augusta Ward, Lady Rose's Daughter
Winston Churchill, The Crossing
Mary Augusta Ward, The Marriage of William Ashe
Winston Churchill, Coniston
Frances Little, The Lady of the Decoration
Winston Churchill, Mr. Crewe's Career
Basil King, The Inner Shrine

Explanation: 

For my final project I followed the class notes from April 16th and implemented the Gensim similarity index. I compared two different corpuses, one containing Shakespeare’s plays and the other being composed of top 10 fiction bestsellers from the first decade of the 20th century. Each corpus had two different types of transformations performed on them – the first being to only find the similarity using the raw text, and the other being the extraction of just all the nouns and finding similarity in that. Extracting the nouns from the corpus will provide a better analysis of topics (and potentially themes) covered in the text.

At a high level, the algorithm accepts a transformed corpus, vectorizes it, gets the tf-idf scores for relative frequency of words, and then compares one text to the entire corpus using Gensim’s unsupervised algorithm for Latent Semantic Indexing. This will provide us with a similarity score that will better demonstrate relationships across texts as well as analyze topical structure across texts.



Notes about Implementation:

-	Downloaded NLTK via Terminal
-	I worked across 4 different Python notebooks so that it was easy to distinguish from each implementation
o	Shakespeare (raw, nouns)
o	Novels (raw, nouns)
-	The block of code under Implementation preprocesses and transforms the words from the corpus to either use the raw text or the text filtered to output only the nouns
-	There is a markdown section in each of the docs called Begin LSI Transformation. There is a variable called “user-text-choice” this is a variable that can be changed to map the initial text to measure against the corpus.
o	Shakespeare: Macbeth
o	1900-09 Novels: The Crisis (shown in Python notebook)
♣	1900-09 Novels: The Crisis (results shown later in this analysis)

Problems:

-	The biggest issue I faced during this assignment was the initial implementation I had for filtering the text for nouns. The way I tried to loop over it initially slowed the code to take about 10 minutes every time that I wanted to transform the corpus. The code did work and completed its job, but it was slow and not optimal. From there I googled and found an optimized way to solve my issue after reading through stack overflow. After that I made a few changes after reading the NLTK documentation and came to my current solution.
-	Notebook I/O exceeded
o	I tried running all of this in one python notebook initially. 
o	It was not ideal and kept running very slowly
o	Additionally I was worried about confusing variable names and accidently having another implementation’s results mistakenly factor into the others  so I ended up making 4 different notebook

Analysis:

For this analysis, I wanted to note the important distinction in the two corpuses that were run on the Gensim similarity index algorithm. 
1)	Shakespeare corpus all have the same author, whereas the 1900-09 corpus has some of the same novelists but not all
2)	One corpus analyzes plays, while the other is measuring novels
a.	Length with be a factor that plays into both


For Shakespeare I did not anticipate the similarity index to change that much, meaning that I did not expect the values to fall below 0.9 or deviate too much from the raw text. The results did exemplify this hypothesis. The transferred “noun only” text did exemplify more similarity across the texts, which does make sense given the language/themes across Shakespearian texts are often fairly similar.

For the early 20th century novels, I anticipated that the similarity would be much lower than that of the result from the Shakespeare corpus. This time we are working with a longer piece of text and differing authors throughout the corpus. I found it interesting to run the similarity based off a text by Winston Churchill. He has a total of 4 pieces in the corpus, and the nouns implementation was slightly better at mapping the similarity across these – in terms of having the first set of high similarity results all being Churchill’s work.  

Based on these results, I would argue that filtering only the nouns from the corpus provides a better representation similarity across texts based off topical structure, language, and themes present.
