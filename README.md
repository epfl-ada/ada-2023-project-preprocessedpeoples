# Unveiling the Balance in Gender Representation in the Movie Industry

# Abstract
Quantitative analysis of films facilitates a better understanding of whether the gender representation in the film industry has improved since its first inception. This study tries to reveal the gender representation differences and examines whether the representation of females in the movie industry has improved in time to come up with the female under-representation and stereotyping insights. We start by performing simple analysis, studying the distribution of male and female characters and their character representations. Furthermore, we perform more complex analysis using word embeddings of the verbs associated with that particular character from the plot summaries and then cluster them to study the importance of characters portrayed by male and female actors. Our initial analysis reveals that female characters are lower in proportion compared to their male counterparts in most of the genres and they are portraying less range of character archetypes with wider ranges of sentiments.

# Introduction
Films play an important role in perpetuating ideas and stereotypes, and gender is no exception. Traditionally, female characters have been portrayed in the roles of mothers, wife, girlfriend, or sex object motifs while male actors have dominated the leading roles. With the rise of feminism in the 1960s, 1990s, and more recently in the 2010's especially with the rise of movements such as the MeToo movement, we must ask whether improvements have been made in the balance of gender representation in the Film Industry. We attempt to make a temporal analysis with respect to the representation of male and female characters using the CMU Film Synopsis Corpus. Additionally, we will investigate the male-female distribution not only for the actors but also for the film crew thanks to the additional dataset in order to reveal the imbalance in gender representation in the Movie Industry.
During the analysis, we utilized a variety of chart types to improve the depth of interpretation. Here are same samples from our initial analysis below:
<p align="middle">
  <img src="output/image/avg_age.png" width="200" />
  <img src="output/image/avg_percentage_temporal.png" width="200" /> 
  <img src="output/image/boxplot_mean_proportions.png" width="200" />
</p>

# Research Questions:
The project includes research questions from two domains : Stationary Analysis & Time Series Analysis

Stationary Analysis

Questions:

1) How does the gender composition of cast and crew correlate with a film's success, measured in terms of box office revenue and award recognitions?
2) Are there specific movie genres that demonstrate a minimal or no gender gap in terms of character representation?
Does the balance of male and female characters impact a film's financial success?
3) What is the gender representation trend in the most popular movie genres?
4) Do films that pass the Bechdel test (explained in the proposed additional datasets part) perform differently at the box office compared to those that don't pass?
5) How does gender representation in award-winning films compare to those that did not win major awards?
6) How does gender representation in the film industry vary across different countries?
7) What are the character types that are portrayed by uniquely female actresses and male actors? How are the character descriptions sentiments differing with respect to the gender? Is it the same for unisex characters that can be portrayed by both genders?

Time Series Analysis

Questions:

1) How has the gender balance among cast and crew evolved over the years in the film industry?
2) In the Oscars, how does gender representation among nominees and winners vary over time?
3) What are the long-term trends in gender representation in movies?

# Proposed additional datasets (if any):
We have already used CMU Movie Dataset with Stanford CoreNLP-processed summaries. In addition to that, we plan to use three additional datasets to enrich our research results.

1) Data collected by us: 
    i) Crew and cast dataset:
    We created an additional dataset by using Freebase IDs and Wikidata API to extract IMDb IDs.
    TMDB API is used for acquiring gender information of cast and crew members.
    The results are stored in movie_with_gender_info.csv file.

    ii)Character description dataset: 
    A dataset manually created by matching the existing 73 tv tropes character types and the retrieved tv tropes character definitions from tv tropes website.
    Resulting dataset is stored in unique_character_types.csv file.

2) Oscar award dataset: 

    To analyse Oscar awards data by gender, focusing on nominee and winner gender proportions, revealing industry gender biases and progress towards equality in film awards, we plan to use the following dataset:

    The data is taken from https://www.kaggle.com/datasets/unanimad/the-oscar-award/data?select=the_oscar_award.csv.

3) Bechdel test : A measure to assess the representation of women in films

    The test involves three criteria:

    1) Two Women: The movie must have at least two women in it.
    2) Who Talk to Each Other: These women must talk to each other at some point.
    3) About Something Besides a Man: Their conversation must be about something other than a man.

    The data is taken from https://www.kaggle.com/datasets/alisonyao/movie-bechdel-test-scores.

# Methods

Step 1: Data scraping, pre-processing and dataset construction

Step 2: Create and visualize the gender related data 

Step 3: Perform sentiment analysis to the character types/descriptions

Step 4: Perform sentiment analysis to the plots and reveal the change in time

Step 5: Perform hypothesis testing (tentative) based on Oscar nominees and Bechdel test results

Step 6: Extracting character **BERKE - combine with  Determine the character importance based on the CoreNLP summaries
Character complexity by defining some metric, for example number of actions a character takes in the movie plot summary. Problems are some plot descriptions are only a sentence. Looking at the type of actions with CoreNLP, extract the sentences associated by the characters, extract adjectives. Analyse the complexity across female and male characters.

Step 7: Provide detailed analysis for each research question

Step 8: Create data story

Step 9: Creating the web page

# Proposed timeline
20/11/2023 - 26/11/2023
- Finalise the preprocessing of data. Tasks include handling missing values, handling invalid values, combining datasets, removing data points. 
- Create a word embedding which is associated to each character. Create plots visualising frequency of words used to describe male and female actors, and other exploratory plots. 

27/11/2023 - 3/12/2023
- Step 6: Perform clusterings on the word embeddings. Try several algorithms and use visualisations such as UMAP or tSNE plots. Initial study of the clusters by gender. 
- define a character complexity metric based on verbs used to describe a character on the CoreNLP outputs. 
- Step 4: Analysis of sentiment analysis results as a temporal analysis. 
- Step 5: Perform the hypothesis testing to reveal the gender reprasantation differences between the oscar nominees or winners

4/11/2023 - 10/12/2023
- step 6 continued: Perform more in depth studies of the clusters, correlating to character attributes, movie attributes and as a temporal analysis. 

11/12/2023 - 17/12/2023
- begin creation of the website. 
- create any further visualisations.
- continue analysis on the clusters.  

18/12/2023 - 22/12/2023
- continue work on the website.
- finalise the notebook and repository to be submitted.

# Organization Within the Team
Zeynep: Step 2, Step 5 
Adam: Step 6 
Berke: Step 1, Step 6 
Nazlıcan: Step 3, Step 4 
Kenta: Step 2
Step 7 step 8, step 9: will be performed by each group member in collaboration

# References

[1] [Learning Latent Personas of Film Characters](http://www.cs.cmu.edu/~dbamman/pubs/pdf/bamman+oconnor+smith.acl13.pdf)
David Bamman, Brendan O'Connor, and Noah A. Smith
ACL 2013, Sofia, Bulgaria, August 2013
