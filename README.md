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
The project includes research questions as follows:

1) How does gender impact actors' career opportunities and success, particularly in terms of the types of roles and reward opportunities offered?
2) Is there a relation between gender and character complexity based on character relation network and plot summaries in the movies?
3) Does semantic analysis of role types reveal any distinct differences in the assignment of roles based on gender?
4) Does the gender composition of cast and crew causally influence the critical success of films, evaluated by IMDb ratings?
5) Are there specific movie genres that demonstrate a minimal or no gender gap in terms of character representation?
Does the balance of male and female characters impact a film's critical success?


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

    iii)imdb scores dataset:
    In order to have a success measure, we extracted imdb scores based on the imdb ids that we extracted by using FreebaseIDs and Wikidata API.

2) Oscar award dataset: 

    To analyse Oscar awards data by gender, focusing on nominee and winner gender proportions, revealing industry gender biases and progress towards equality in film awards, we plan to use the following dataset:

    The data is taken from https://www.kaggle.com/datasets/unanimad/the-oscar-award/data?select=the_oscar_award.csv.


# Methods

Step 1: Data scraping, pre-processing and dataset construction

Step 2: Create and visualize the gender related data 

Step 3: Sentiment analysis of the characters portrayed based on genders
Subtasks:
- Perform sentiment analysis to the description of character types that are portrayed
- Perform sentiment analysis to the verbs and adjectives that are associated with the characters coming from the CoreNLP summaries to investigate further and reveal whether the sentiments based on gender changes in time

Step 4: Perform hypothesis testing based on Oscar nominees and Bechdel test results

Step 5: Character analysis over plot
Subtasks: 
- Extracting character vector representations from plot, utilizing unsupervised techniques, word embeddings, sentence transformers combined with CoreNLP data.
- Visualizing similaries or distances between characters in our representation, through dimensionality reduction techniques (t-SNE, UMAP)
- Inpecting common word occurences associated with characters of different gender. 
- Determine the character importance based on the CoreNLP summaries. 
- Character complexity by defining some metric, for example number of actions a character takes in the movie plot summary. - Problems are some plot descriptions are only a sentence. Looking at the type of actions with CoreNLP, extract the sentences associated by the characters, extract adjectives. Analyse the complexity across female and male characters.

Step 6: Provide detailed analysis for each research question

Step 7: Create data story

Step 8: Creating the web page

# Proposed timeline
20/11/2023 - 26/11/2023
- Finalise the preprocessing of data. Tasks include handling missing values, handling invalid values, combining datasets, removing data points. 
- Create a word embedding which is associated to each character. Create plots visualising frequency of words used to describe male and female actors, and other exploratory plots. 

27/11/2023 - 3/12/2023
- Step 5: Perform clusterings on the word embeddings. Try several algorithms and use visualisations such as UMAP or tSNE plots. Initial study of the clusters by gender. 
- define a character complexity metric based on verbs used to describe a character on the CoreNLP outputs. 
- Step 3: Inspection of sentiment analysis findings as a temporal analysis. 
- Step 4: Perform the hypothesis testing to reveal the gender representation differences between the oscar nominees or winners

4/11/2023 - 10/12/2023
- Step 5 continued: Perform more in depth studies of the clusters, correlating to character attributes, movie attributes and as a temporal analysis. 

11/12/2023 - 17/12/2023
- begin creation of the website. 
- create any further visualisations.
- continue analysis on the clusters.  

18/12/2023 - 22/12/2023
- continue work on the website.
- finalise the notebook and repository to be submitted.

# Organization Within the Team
Zeynep: Step 2, Step 4 

Adam: Step 5 

Berke: Step 1, Step 5 

Nazlıcan: Step 3

Kenta: Step 2

Step 6 step 7, step 8: will be performed by each group member in collaboration

# References

[1] [Learning Latent Personas of Film Characters](http://www.cs.cmu.edu/~dbamman/pubs/pdf/bamman+oconnor+smith.acl13.pdf)
David Bamman, Brendan O'Connor, and Noah A. Smith
ACL 2013, Sofia, Bulgaria, August 2013
