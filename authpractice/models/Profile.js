const { Schema, model } = require("../db/connection.js")

const ProfileSchema = new Schema({
    username:    { type: String, unique: true, required: false },
    photo:       { type: String },
    gender:      { type: String, enum: ["Male", "Female", "Other"], required: true },
    sexuality:   { type: String, enum: ["Male", "Female", "No Preference"], required: true },
    bio:         { type: String, required: true }
})

const Profile = model("Profile", ProfileSchema)

module.exports = Profile