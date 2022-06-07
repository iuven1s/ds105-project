<p align="center">
	<img src="https://raw.githubusercontent.com/iuven1s/ds105-project/main/img/logo.png" />
</p>

---

This project classifies the genre of given tracks (available on Spotify) using machine learning techniques. By compiling a custom dataset using data collected from [Every Noise at Once](https://everynoise.com) and Spotify's Web APIs, we were able to collect data on over 6,500 unique tracks, including each track's 13 high-level audio features (e.g. energy, valence, danceability, tempo, etc.).

## Why?
We made this project in fulfillment of the requirements for the DS105L course taught by the [DSI](https://www.lse.ac.uk/DSI) at London School of Economics. But also because we like music and wanted to explore how technology and music could mix and match! 🎵 

## How can I test it out?
Our model is available online [here](https://ds105.herokuapp.com) (it may be a little slow to load at first because the dyno may be asleep! 💤).

## Where can I learn more about this project?
You can read our project report on our GitHub Pages site: [Predicting Track Genres using Audio Features](https://iuven1s.github.io/ds105-project) ✍️

## Dependencies
- NumPy >= 1.22.4
- pandas >= 1.4.2
- scikit-learn >= 1.1.1
- scikit-multilearn >= 0.2.0
- Spotify Web API Client ID and Client Secret Keys (set as environment variables `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` respectively)
