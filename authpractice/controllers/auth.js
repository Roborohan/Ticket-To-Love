const bcrypt = require("bcryptjs")
const User = require("../models/User")
const Profile = require("../models/Profile")
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

const logout = (req,res) => {
    req.session.user = undefined
    res.redirect("../")
}

const test = (req,res) => {
    res.send("logged in")
}

const about = (req,res) => {
    res.render('auth/about')
}

const getProfile = async (req, res) => {
    try {
        const profile = await Profile.findOne({ username: req.session.user });
        res.render('auth/profile', { 
            profile: profile, 
            username: req.session.user, 
            photo: profile && profile.photo ? profile.photo.data.toString('base64') : '', 
            contentType: profile && profile.photo ? profile.photo.contentType : '',
            sexuality: profile ? profile.sexuality : '', 
            gender: profile ? profile.gender : '', 
            bio: profile ? profile.bio : '', 
            charCount: profile ? profile.bio.length + "/100" : '' });
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
        req.body.username = req.session.user;
        const existingProfile = await Profile.findOne({ username: req.body.username });
        if (existingProfile) {
            await Profile.findOneAndUpdate({ username: req.body.username }, req.body);
        } else {
            const profile = new Profile(req.body);
            await profile.save();
        }
        if (req.file) {
            const profile = await Profile.findOne({ username: req.body.username });
            profile.photo = {
                data: fs.readFileSync(req.file.path),
                contentType: req.file.mimetype
            };
            await profile.save();
        }

        // fetch profile data from the database
        const updatedProfile = await Profile.findOne({ username: req.body.username });
        res.render('auth/profile', { profile: updatedProfile });
    } catch (error) {
        res.send('Error updating profile: ' + error);
    }
};




  



const getMatches = (req,res) => {
    res.render('auth/matches')
}

const getMessages = (req,res) => {
    res.render('auth/messages')
}

const getFavMovie = (req,res) => {
    res.render('auth/favmovie')
}


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
    profileSubmit
}