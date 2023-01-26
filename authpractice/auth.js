module.exports = (req,res,next) => {
    if(req.sessions.user){
        next()
    }
    else {
        res.json({message: "not logged in"})
    }
}