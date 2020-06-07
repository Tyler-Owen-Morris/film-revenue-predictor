# IMDB Film Reveune Predictor
<img src="img/IMDB.jpg" height=40%  width=47%  alt="What's hiding inside your phone?" ALIGN="right">

Predicting opening weekend box office revenue of films based on IMDB data.

__Abstract:__ This project uses the largely categorical data publicly available on IMDB to train machine learning algorithems to predict the box office revenue of fictional or future films.

__Results:__ Using a gradient-boosted trees model the flask application can make live predictions on randomly generated films with ~50% better than baseline accuracy.

All of the film data used was gathered off of the IMDB api and through web scraping of IMDB Pro for the years 2015-2019.

See the presentation slides [Here](). See the video [Here]().
<br clear="right">

# Background & Motivation

So many different factors can go into the financial success or failure of a film. More people go to see films with famous actors in them. The size of a films budget is a strong indicator of the investment in marketing. Which company distributes a film can affect how many theatres it releases in. MPAA Rating could limit the audience.

It's clear that all of these factors play a role in determining the outcome, but can we train a machine to pick up on these factors?