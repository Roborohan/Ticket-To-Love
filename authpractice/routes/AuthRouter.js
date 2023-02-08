///////////////////////////////
// Import Router
////////////////////////////////
const router = require("express").Router()
const AuthController = require("../controllers/auth.js")
const auth = require("../auth")
const multer = require("multer");
const path = require("path");
const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, 'public/images/');
    },
    filename: function(req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
});
const upload = multer({
    storage: storage
});

///////////////////////////////
// Router Specific Middleware
////////////////////////////////

///////////////////////////////
// Router Routes
////////////////////////////////

//REGISTER
router.get("/register", AuthController.getRegister)

//REGISTER ACCOUNT
router.post("/register", AuthController.registerSubmit)

//LOGIN
router.get("/login", AuthController.getLogin)

//LOGIN SUBMIT
router.post("/login", AuthController.loginSubmit)

//LOGOUT
router.get("/logout", AuthController.logout)

//TEST
router.get("/test", auth, AuthController.test) //auth means that this page is only accessible when logged in

//ABOUT
router.get('/about', AuthController.about)

//PROFILE
router.get('/profile', auth, AuthController.getProfile)

//PROFILE SUBMIT
router.post('/profile', auth, upload.single("photo"), AuthController.profileSubmit)

//MATCHES
router.get('/matches', auth, AuthController.getMatches)

//MESSAGES
router.get('/messages', auth, AuthController.getMessages)

//FAVMOVIE
router.get('/favmovie', auth, AuthController.getFavMovie)

//FAVMOVIE SUBMIT
router.post('/favmovie', auth, AuthController.favMovieSubmit)

///////////////////////////////
// Export Router
////////////////////////////////
module.exports = router