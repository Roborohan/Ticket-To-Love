module.exports = (req,res,next) => {
    if(req.session.user){
        next()
    }
    else {
        res.redirect("../")
        res.json({message: "not logged in"})
    }
}