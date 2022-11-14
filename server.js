if(process.env.NODE_ENV !== "production"){
    require("dotenv").config();
} 

//Imports
const express = require("express");
const app = express();
const bcrypt = require("bcrypt");
const passport = require("passport");
const initializePassport = require("./passport-config");
const flash = require("express-flash");
const session = require("express-session");
const methodOverride = require("method-override");

initializePassport(
    passport,
    email => users.find(user => user.email === email),
    id => users.find(user => user.id === id)
    );

const users = []; //replace with db code here

app.set('view-engine', 'ejs');

app.use(express.urlencoded({extended: false}));
app.use(express.static("public"));
app.use(flash());
app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());
app.use(methodOverride("_method"));

app.post("/signin", checkNotAuthenticated, passport.authenticate("local", {
    successRedirect: "/",
    failureRedirect: "/signin",
    failureFlash: true 
}));

app.post("/signup", checkNotAuthenticated, async (req,res) =>{
    try{
        const hashedPassword = await bcrypt.hash(req.body.password,10);
        users.push({
            id: Date.now().toString(),
            name: req.body.name,
            email: req.body.email,
            password: hashedPassword,
            dateofbirth: req.body.dateofbirth
        });
        res.redirect("/signin");
    } catch (e) {
        console.log(e);
        res.redirect("/signup");
    }
});



//Routes
app.get('/', checkAuthenticated, (req,res) =>{
    res.render("index.ejs", {name: req.user.name});
});

app.get('/signin', checkNotAuthenticated, (req,res) =>{
    res.render("signin.ejs");
});

app.get('/signup', checkNotAuthenticated, (req,res) =>{
    res.render("signup.ejs");
});

app.get('/about', checkNotAuthenticated, (req,res) =>{
    res.render("about.ejs");
});

app.get('/profile', checkAuthenticated, (req,res) =>{
    res.render("profile.ejs");
});

app.get('/matches', checkAuthenticated, (req,res) =>{
    res.render("matches.ejs");
});

app.get('/messages', checkAuthenticated, (req,res) =>{
    res.render("messages.ejs");
});
//End Routes

app.delete("/logout", (req,res) =>{
    req.logOut(req.user, err => {
        if (err) return next(err);
        res.redirect("/");
    });
});

function checkAuthenticated(req,res,next){
    if(req.isAuthenticated()){
        return next();
    }
    res.redirect("/signin");
}


function checkNotAuthenticated(req,res,next){
    if(req.isAuthenticated()){
        return res.redirect("/");
    }
    next();
}

app.listen(3000);
