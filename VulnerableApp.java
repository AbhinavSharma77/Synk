import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import java.sql.*;

@SpringBootApplication
@RestController
public class VulnerableApp {
    // Hardcoded database credentials (Security Issue)
    private static final String DB_URL = "jdbc:sqlite:test.db";
    private static final String DB_USER = "admin";
    private static final String DB_PASS = "password123";

    @GetMapping("/login")
    public String login(@RequestParam String username, @RequestParam String password) {
        try {
            Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
            Statement stmt = conn.createStatement();

            // 🚨 SQL Injection Vulnerability 🚨
            String query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
            ResultSet rs = stmt.executeQuery(query);

            if (rs.next()) {
                return "Welcome, " + username + "!";
            } else {
                return "Invalid credentials!";
            }
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }

    // 🚨 XSS Vulnerability 🚨
    @PostMapping("/submit")
    public String submit(@RequestBody String userInput) {
        return "User submitted: " + userInput; // No sanitization = XSS
    }

    public static void main(String[] args) {
        SpringApplication.run(VulnerableApp.class, args);
    }
}
