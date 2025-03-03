const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const jwt = require("jsonwebtoken");
const { exec } = require("child_process");

const app = express();
app.use(express.json());

// Hardcoded secret key (Security Issue)
const SECRET_KEY = "mysecretkey123";

// Connect to SQLite database (No input sanitization)
const db = new sqlite3.Database(":memory:");
db.run("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)");

app.post("/login", (req, res) => {
    const { username, password } = req.body;

    // 🚨 SQL Injection Vulnerability 🚨
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    db.get(query, (err, row) => {
        if (row) {
            const token = jwt.sign({ username }, SECRET_KEY);
            res.json({ token });
        } else {
            res.status(401).send("Invalid credentials");
        }
    });
});

// 🚨 Command Injection Vulnerability 🚨
app.get("/exec", (req, res) => {
    const command = req.query.cmd;
    exec(command, (error, stdout) => {
        res.send(stdout || error.message);
    });
});

app.listen(3000, () => {
    console.log("Vulnerable app running on http://localhost:3000");
});
