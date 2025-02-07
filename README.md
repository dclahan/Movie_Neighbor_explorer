# Movie neighborhood explorer

This is a simple Flask app that uses the TMDB API to find movies that are connected to a given movie.

The definition of "neighbor" is somewhat arbitrary, but it's based on the following criteria (the rules of [cine2nerdle](https://www.cinenerdle2.app/how-to-play/battle/classic) ): 

A neighbor is a movie that shares a similar actor, director, cinematographer, composer, or writer. Neighbors include 
* movies (A,B), where actor x acted in both A and B
* movies (A,B), where the director of movie A was an actor (or different valid role) in movie B. 
    - For example, David Lynch did not direct The Fabelmans (2022), but the movies (The Fabelmans (2022), Mulholland Drive) satisfy the neighbor property and are valid neighbors.

## Usage

*This app is not intended to be used to cheat while playing cine2nerdle*

Its main purpose is to be used as a reference when exploring the neighborhood of a given movie. Its much easier than following all the links manually.

Its gonna be slow for movies with a lot of connections, its best used to look at the neighors of an obscure movie, where you arent sure about the connections 
- ex: I am familiar with >5 actors in the movie "Barbie (2023)", I do not need to check all the connections to find out what movies are connected to Barbie

This app only show the top 100 connections, ordered by popularity (tmdb definition of popularity so not the best)