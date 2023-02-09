const bcrypt = require("bcryptjs")
const User = require("../models/User")
const Profile = require("../models/Profile")
const FavMovie = require("../models/FavMovie")
const multer = require("multer");
const fs = require("fs");


const getRegister = (req,res) => {
    res.render("auth/register")
}

const registerSubmit = async (req,res) => {
    const salt = await bcrypt.genSalt(10)
    req.body.password = await bcrypt.hash(req.body.password, salt)
    const user = await User.create(req.body)
    res.redirect("/auth/login")
}

const getLogin = (req,res) => {
    res.render("auth/login")
}

const loginSubmit = async (req,res) => {
    try {
        const user = await User.findOne({username: req.body.username})
        if (user){
            const result = await bcrypt.compare(req.body.password, user.password)
            if (result) {
                req.session.user = user.username
                res.redirect("./profile")
            } else {
                res.status(400).json({error: "Incorrect password"})
            }
        } else {
            res.status(400).json({error: "No user with that username"})
        }
    } catch (error) {
        res.json(error)
    }
}

const logout = (req, res) => {
    console.log("Logout function called");
    req.session.destroy((error) => {
        if (error) {
            res.send('Error logging out: ' + error);
        } else {
            res.redirect("../");
        }
    });
};

const test = (req,res) => {
    res.send("logged in")
}

const about = (req,res) => {
    res.render('auth/about')
}
const getProfile = async (req, res) => {
    try {
        let profile = await Profile.findOne({ username: req.session.user });
        let photo = '';
        let contentType = '';
        let sexuality = '';
        let gender = '';
        let bio = '';
        let charCount = '';

        if (!profile) {
            profile = new Profile({
                username: req.session.user
            });
        } else {
            photo = profile.photo ? profile.photo.data.toString('base64') : '';
            contentType = profile.photo ? profile.photo.contentType : '';
            sexuality = profile.sexuality || 'No Preference';
            gender = profile.gender || 'Other';
            bio = profile.bio || '';
            charCount = bio.length + "/100";
        }

        res.render('auth/profile', { 
            profile, 
            username: req.session.user, 
            photo, 
            contentType, 
            sexuality, 
            gender, 
            bio, 
            charCount 
        });
    } catch (error) {
        res.send('Error fetching profile: ' + error);
    }
};

const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, "public/images");
    },
    filename: function(req, file, cb) {
        cb(null, `${req.session.user}-${Date.now()}.${file.mimetype.split("/")[1]}`);
    }
});

const upload = multer({ storage });

const profileSubmit = async (req, res) => {
    try {
        let profile = await Profile.findOne({ username: req.session.user });
        if (!profile) {
            profile = new Profile({
                username: req.session.user
            });
        }

        if (req.files && req.files.photo) {
            profile.photo = {
                data: req.files.photo.data,
                contentType: req.files.photo.mimetype
            };
        }
        profile.sexuality = req.body.sexuality;
        profile.gender = req.body.gender;
        profile.bio = req.body.bio;
        await profile.save();

        res.json({ success: true });
    } catch (error) {
        res.json({ success: false, error: error.message });
    }
};

const getMatches = (req,res) => {
    res.render('auth/matches')
}

const getMessages = (req,res) => {
    res.render('auth/messages')
}

// getFavMovie function
const getFavMovie = async (req, res) => {
    try {
        const favMovies = await FavMovie.find({ username: req.session.user });
        res.render('auth/favmovie', {
            username: req.session.user,
            favMovies: favMovies
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Failed to retrieve favorite movies!" });
    }
};

  
// favMovieSubmit function
const favMovieSubmit = async (req, res) => {
    try {
        const { title, releaseDate, runtime, genre, actors, director, country, rating, poster } = req.body;

        // Check if the user has already reached the maximum limit of 10 favorite movies
        const favMoviesCount = await FavMovie.countDocuments({ username: req.session.user });
        if (favMoviesCount >= 10) {
            console.log("Maximum limit of 10 favorite movies reached!");
            return res.status(400).json({ error: "Maximum limit of 10 favorite movies reached!" });
        }

        // Check if the movie is already in the user's favorite list
        const existingMovie = await FavMovie.findOne({ username: req.session.user, title: title });
        if (existingMovie) {
            console.log("Movie already added to favorites!");
            return res.status(400).json({ error: "Movie already added to favorites!" });
        }

        // Add the new favorite movie
        const favMovie = new FavMovie({
            username: req.session.user,
            title: title,
            releaseDate: releaseDate,
            runtime: runtime,
            genre: genre,
            actors: actors,
            director: director,
            country: country,
            rating: rating,
            poster: poster
        });

        await favMovie.save();
        console.log("Movie added to favorites!");
        res.redirect('/auth/favmovie');
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Failed to add movie to favorites!" });
    }
};

const deleteFavMovie = async (req, res) => {
    try {
      const deletedMovie = await FavMovie.findOneAndDelete({
        username: req.session.user,
        _id: req.body.favId
      });
      if (!deletedMovie) {
        return res.status(404).json({ error: "Movie not found!" });
      }
      res.redirect('/auth/favmovie');
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Failed to delete movie!" });
    }
};
  
module.exports = {
    getRegister,
    getLogin,
    loginSubmit,
    registerSubmit,
    logout,
    test,
    about,
    getProfile,
    getMatches,
    getMessages,
    getFavMovie,
    profileSubmit,
    favMovieSubmit,
    deleteFavMovie
}