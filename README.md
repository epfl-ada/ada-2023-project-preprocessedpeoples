# CinemaScope - Lens on Gender Shifts

*Preprocessed Peoples : Zeynep Tandogan, Nazlican Turan, Adam Barla, Berke Argin*  
[Data Story](https://zeyneptandogan.github.io/preprocessedpeoples/)

# Abstract
Movies offer viewers the opportunity to share different experiences and emotions. While doing this, films generally focus on the emotions like sorrows and joys, serving as reflections of society. Despite its power and reach, it struggles with a long-standing issue of gender bias. It is believed by some people that there is gender bias in the movie industry. There are many arguments in this gender bias scope, such as stereotypical portrayal of male and female characters and underrepresentation of women.

In this project, it is aimed to perform qualitative and quantitative analysis comprehensively to explore the multifaceted dimensions of gender representation in movies.This study examines whether the representation of female in the movie industry has improved in time to better understand the extent of female under-representation and stereotyping

# Introduction
Films play an important role in perpetuating ideas and stereotypes, and gender is no exception. Traditionally, female characters have been portrayed in the roles of mothers, wife, girlfriend, or sex object motifs while male actors have dominated the leading roles. With the rise of feminism in the 1960s, 1990s, and more recently in the 2010's especially with the rise of movements such as the MeToo movement, we must ask whether improvements have been made in the balance of gender representation in the Film Industry. We attempt to make a temporal analysis with respect to the representation of male and female characters using the CMU Film Synopsis Corpus. Additionally, we will investigate the male-female distribution not only for the actors but also for the film crew thanks to the additional dataset in order to reveal the imbalance in gender representation in the Movie Industry.

# Research Questions:
The project includes research questions as follows:

1) How does gender impact actors' career opportunities, collaborations and success, particularly in terms of the types of role and reward opportunities offered?
2) Do plot summaries contain any gender stereotypes, and if so, in what manner?
3) Does semantic analysis of character types reveal any distinct differences in the assignment of roles based on gender?
4) Does the gender composition of cast and crew influence the critical success of films, evaluated by IMDb ratings?
5) Are there specific movie genres that demonstrate a minimal or no gender gap in terms of character representation?

# Additional datasets:
We have already used CMU Movie Dataset In addition to that, we plan to use three additional datasets to enrich our research results.

1) Data collected by us:
   
    i) Crew and cast dataset:
    We created an additional dataset by using Freebase IDs and Wikidata API to extract IMDb IDs.
    TMDB API is used for acquiring gender information of cast and crew members.
    The results are stored in movie_with_gender_info.csv file.

    ii)Character description dataset: 
    A dataset manually created by matching the existing 73 tv tropes character types and the retrieved tv tropes character definitions from tv tropes website.
    Resulting dataset is stored in unique_character_types.csv file.

   iii) Plot Summaries dataset:
    CoreNLP results exhibit inaccuracies, particularly where it fails to identify a verb when it should be or incorrectly labels something as a verb when it is not. We have created our own pipeline to classify verbs/nouns/adjectives related to each characters in the plot summaries.
   
3) Oscar award dataset:  To analyse Oscar awards data by gender, focusing on nominee and winner gender proportions, revealing industry gender biases and progress towards equality in film awards, we plan to use the following dataset:
    The data is taken from [Oscar Award Dataset](https://www.kaggle.com/datasets/unanimad/the-oscar-award/data?select=the_oscar_award.csv).

4) IMDB Ratings Dataset:
   As a success measure, IMBD ratings are used in the analysis. The data is taken from IMDB Non-commercial datasets. Only the files titled 'title.ratings.tsv.gz' and 'title.basics.tsv.gz' are utilized for this analysis.
   The datasets can be found in [IMDB Ratings Dataset](https://developer.imdb.com/non-commercial-datasets/).
   
# Methods

Step 1: Data scraping, pre-processing and dataset construction
- Organization and missing data handling for CMU Movie Dataset
- Manipulating Oscars dataset and IMDB dataset based on the main dataset (CMU Movie dataset)
- Collecting and retrieving reliable data with plot summaries by using our own pipeline

Step 2: Analysis with hypothesis testing for Reward Opportunities based on Gender
In this part, we have applied hypothesis testings for the following cases:
- The effect of receiving Oscar nominee/win on the career paths based on appearances
- Genre Preference
- Age at First Nomination/Win

Step 3: Sentiment analysis of the characters portrayed based on genders
- Search for the distribution of characters played exclusively by females, exclusively by males, and characters played by both genders.
- Perform sentiment analysis to the description of character types that are portrayed and their definitions.

Step 4: Analysis about the Impact of Gender Composition in Cast and Crew on IMDb Ratings
- Changes in time based on cast and crew distributions
- Average Crew & Cast Gender Distribution
- Performing ANOVA (Analysis of Variance) to test if there are statistically significant differences and Tukey HSD test

Step 5: Creating Network for the Analysis between Actor Collaborations
- NAZLICAN WILL WRITE THIS PART!

Step 6: Character analysis over plot
- BERKE AND ADAM

Step 7: Create data story & the web page

# Proposed timeline
17/11/2023 -> Delivery of the Milestone 2

20/11/2023 - 26/11/2023 -> Hypothesis testing for Reward Opportunities & Sentiment analysis of the characters portrayed based on genders

27/11/2023 - 3/12/2023 ->  Analysis about the Impact of Gender Composition in Cast and Crew on IMDb Ratings

4/11/2023 - 10/12/2023 -> Creating Network for the Analysis between Actor Collaborations

11/12/2023 - 17/12/2023 -> Character analysis over plot

18/12/2023 - 22/12/2023 -> Data Story and Website Preperation

22/12/2023  -> Delivery of the Milestone 3

# Organization Within the Team
| Member    | Tasks                                                              |
|-----------|--------------------------------------------------------------------|
| Zeynep    | - Analysis with hypothesis testing for Reward Opportunities based on Gender<br>- Analysis about the Impact of Gender Composition in Cast and Crew on IMDb Ratings<br>- Initial Creation of the Project website and ReadMe<br>- Obtaining Plotly charts to enhance the visual appeal of the website's charts |
| Adam      | - Plot summaries data extraction from original CoreNLP results    |
| Berke     | - Creation of the verb/noun/adjective extraction pipeline for each character in plot summaries<br>- Analysis based on the results<br>- Collecting crew and cast details by utilizing wikidata ids and freebase ids |
| Nazlıcan  | - Sentiment analysis of the characters portrayed based on genders<br>- Creating Network for the Analysis between Actor Collaborations <br>- Organization of ReadMe file|

Group note: Everyone has been involved in the preparation of data story and website.

Kenta: Kenta is involved until milestone 2, however after that he has not contributed to the project due to personal reasons. 

# References

[1] [Learning Latent Personas of Film Characters](http://www.cs.cmu.edu/~dbamman/pubs/pdf/bamman+oconnor+smith.acl13.pdf)
David Bamman, Brendan O'Connor, and Noah A. Smith
ACL 2013, Sofia, Bulgaria, August 2013
