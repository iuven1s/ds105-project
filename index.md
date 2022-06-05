# Predicting Track Genres using Audio Features
---
## Executive Summary
This project is focused on predicting the genre of a song/track (available on Spotify) based on 10 high-level audio features. We chose to explore this topic since we were interested in finding out if there are characteristics contained within a song (outside of instruments used and societal/cultural influence) that defines the makeup of a genre. We believe this project is especially relevant in today's landscape, since music is ever increasingly pushing boundaries in terms of stylistic choices. We were keen to explore whether a supervised machine learning approach could help answer the question and further help us infer if there are any other genres influencing the sound of a song.

For this project, we collated over 7,000 songs belonging to 9 different genres which were collected from automatically-generated playlists found on [Every Noise at Once](everynoise.com). We manually collected and tagged the relevant playlist ID's and then used Spotify's Web APIs to retrieve the relevant data for preprocessing and analysis. With the relevant preprocessing and exploratory data analysis complete, we had a final dataset of over 6,500 songs each containing 10 high-level audio features.

With our dataset at hand, we began exploring machine learning techniques that could be used for this project. We explored a handful of techniques (even some within the deep learning domain) and ultimately decided on using a Label Powerset approach with a Logistic Regression base classifier. Using these techniques, we found that



## Motivation and Justification
Classifying music based on a signature 'sound' or 'feel' (i.e. a genre) is a surprisingly difficult task; whether we are aware of it or not, our favourite songs are influenced by the sound and feel of songs dating decades back (indeed, one can trace the roots of EDM all the way back to rhythm and blues!) However, 