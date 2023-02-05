const { Schema, model } = require("../db/connection.js")

const UserSchema = new Schema({
    photo:       { type: String },
    gender:      { type: String, enum: ["Male", "Female", "Other"], required: true },
    sexuality:   { type: String, enum: ["Male", "Female", "No Preference"], required: true },
    bio:         { type: String, required: true }
})