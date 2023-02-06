const { Schema, model } = require("../db/connection.js")

const ProfileSchema = new Schema({
    username: {
        type: String,
        required: true
    },
    photo: {
        data: Buffer,
        contentType: String
    },
    sexuality: {
        type: String,
        required: true
    },
    gender: {
        type: String,
        required: true
    },
    bio: {
        type: String,
        required: true,
        maxlength: 100
    }
});


const Profile = model("Profile", ProfileSchema)

module.exports = Profile