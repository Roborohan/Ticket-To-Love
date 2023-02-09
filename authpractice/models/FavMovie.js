const { Schema, model } = require("../db/connection.js")

const FavMovieSchema = new Schema({
    username: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
      },
      releaseDate: {
        type: Date,
        required: true
      },
      runtime: {
        type: String,
        required: true
      },
      genre: {
        type: String,
        required: true
      },
      actors: {
        type: String,
        required: true
      },
      director: {
        type: String,
        required: true
      },
      country: {
        type: String,
        required: true
      },
      rating: {
        type: Number,
        required: true
      },
      poster: {
        type: String,
        required: true 
      }
});


const FavMovie = model("FavMovie", FavMovieSchema)

module.exports = FavMovie