# IMDB Film Reveune Predictor
<img src="img/IMDB.jpg" height=40%  width=47%  alt="IMDB Logo" ALIGN="right">

Predicting opening weekend box office revenue of films based on IMDB data.

__Abstract:__ This project uses the largely categorical data publicly available on IMDB to train machine learning algorithems to predict the box office revenue of fictional or future films.

__Results:__ Using a gradient-boosted trees model the flask application can make live predictions on randomly generated films with ~50% better than baseline accuracy.

All of the film data used was gathered off of the IMDB api and through web scraping of IMDB Pro for the years 2015-2019.

See the presentation slides [Here](). See the video [Here]().
<br clear="right">

# Background & Motivation

So many different factors can go into the financial success or failure of a film. More people go to see films with famous actors in them. The size of a films budget is a strong indicator of the investment in marketing. Which company distributes a film can affect how many theatres it releases in. MPAA Rating could limit the audience. The month a film is released determines how many people are off-work or out of school and looking for a film to go see.

It's clear that all of these factors play a role in determining the outcome, but can we train a machine learning algorithem to pick up on these factors and predict the opening box office revenue of films that never existed? What about guessing the box office for films that have yet to release?

For this project I will be using the largely categorical data from IMDB to build this general model that aims to predict the opening box office weekend of any film.

# The Data
#### The basics of film release strategy

<img src="img/AvgBoxOffice_byMonth3.png" height=60% width=60% alt="Average BO by Month" ALIGN="right"> There are certain Hollywood tropes that every young film student learns. Some are more obvious than others, like - "family movies come out around the Holidays" or "documentaries don't make any money" or "action movies release during the summer months". 

It turns out that these are not just meaningless stereotypes about film studio behavior, but they are tried and tested strategies by the film industry to expose their films to the largest and most excited audience that they are able to gather.

<img src="img/AvgOpeningByGenre.png" alt="Average Opening by Genre" ALIGN="center"><br><br>

#### Capturing Star-Power
<img src="img/FilmCountByActor4.png" height=50% width=50% alt="Top Most Seen Actors in Dataset" ALIGN="right"><br>Capturing the power of having a big name celebrity in your film is not such a cut and dry case. Even the most popular and hardest working actors in hollywood (Samuel L. Jackson for example) are only in 10 or so movies out of 5 years of data. We are going to need a different strategy to capture the importance of star power in films.


<br><br>
<img src="img/AllActorPop-v-OpeningWknd3.png" height=50% width=50% alt="Actor popularity score vs opening weekend" ALIGN="left"> <br>
IMDB keeps a running "Star-Score" on every actor on IMDB. This number is uniquely assigned and decreases as the actor rises in popularity. As such this score has a strong inverse releationship with the high budgets and high revenue films that these Hollywood elite are able to participate in. This will prove to be much more useful information in capturing the impact of a "star".

#### That "other" information at the bottom of the credits

Most people don't read the credits. Once a movie is over they simply grab their belongings and leave the theare. However, lurking in those credits are names that gather more signal for our model. Who was the Executive Producer? What major Studios backed the project? Which companies invested into the distribution of the title?

Most movie-goers don't pay much attention to this information, but we will be looking at just the main Producer, Executive Producer, Director, Production Studio, and Distribution Studio in order to help our model more accurately predict the success of a film.

# Modeling

#### Initial approaches

The average film from our dataset pulls in $6,284,064 on its opening weekend box office. If we repeat this guess for all of the films and calculate our RMSE we get $21,204,973. This will be our baseline on which to improve.

I one-hot encoded for release month, MPAA rating, and the lead actors name. I added this data to the budget information and fit several models. On this simple model Linear Regression was able to perform quite well, but only turned in a $16.1M RMSE which was a mere 24.9% improvement on the baseline. I think we can improve this score further.

There are simply too many actors to take them into account on an individual basis. So, I used the popularity score to categorize actors into "A-list", "B-list", etc, and then I did one hot encoding based on the position on the bill. So lead actor being A-list became its own column etc. With this strategy I was able to improve the linear Regression to $15.7M which brought the score up to a 26% improvement from the baseline.

#### Advanced Approach

There are simply too many Production Companies, Producers, and Executives and the sample size is far too small to have a hope of picking up on their signal individually. Also worth factoring in is the combination of Directors with studios, Actors with Directors, or Actors with one-another. For this reason I selected to convert all of the text features into a string, and perform feature hashing