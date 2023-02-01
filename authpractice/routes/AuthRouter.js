///////////////////////////////
// Import Router
////////////////////////////////
const router = require("express").Router()
const AuthController = require("../controllers/auth.js")
const auth = require("../auth")
//const {
//    checkAuthenticated,
//    checkNotAuthenticated,
//  } = require("../middlewares/authentication")
///////////////////////////////
// Router Specific Middleware
////////////////////////////////

///////////////////////////////
// Router Routes
////////////////////////////////

//CREATE PAGE
router.get("/register", AuthController.getRegister)

//CREATE SUBMISSION
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
router.get('/profile', AuthController.getProfile)

//MATCHES
router.get('/matches', AuthController.getMatches)

//MESSAGES
router.get('/messages', AuthController.getMessages)

//FAVMOVIE
router.get('/favmovie', AuthController.getFavMovie)
///////////////////////////////
// Export Router
////////////////////////////////
module.exports = router