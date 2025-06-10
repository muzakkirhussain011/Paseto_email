package com.example.api1.controller;

import java.util.Map;
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import com.example.api1.model.RegistrationRequest;
import com.example.api1.model.VerifyRequest;
import com.example.api1.model.LoginRequest;

import jakarta.servlet.http.HttpSession;

@RestController
@RequestMapping("/api")
public class AuthController {
    private final RestTemplate rest = new RestTemplate();
    private final Map<String, String> otpStore = new ConcurrentHashMap<>();
    private final String api2Url = "http://localhost:8000"; // API-2 base URL
    private final String apiKey = "test-api-key"; // hardcoded API-2 key

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegistrationRequest req) {
        String otp = String.format("%06d", new Random().nextInt(1_000_000));
        otpStore.put(req.getEmail(), otp);

        HttpHeaders headers = new HttpHeaders();
        headers.set("X-API-Key", apiKey);
        headers.setContentType(MediaType.APPLICATION_JSON);
        Map<String, Object> payload = Map.of(
                "email_address", req.getEmail(),
                "subject", "Your verification code",
                "body", "Your OTP is " + otp
        );
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);
        rest.postForEntity(api2Url + "/internal/send_email", entity, String.class);
        return ResponseEntity.ok(Map.of("status", "otp_sent"));
    }

    @PostMapping("/verify")
    public ResponseEntity<?> verify(@RequestBody VerifyRequest req, HttpSession session) {
        String expected = otpStore.get(req.getEmail());
        if (expected == null || !expected.equals(req.getOtp())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("error", "Invalid OTP"));
        }
        HttpHeaders headers = new HttpHeaders();
        headers.set("X-API-Key", apiKey);
        headers.setContentType(MediaType.APPLICATION_JSON);
        Map<String, Object> payload = Map.of(
                "user_id", "123",
                "email_address", req.getEmail()
        );
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);
        ResponseEntity<Map> res = rest.postForEntity(api2Url + "/internal/token", entity, Map.class);
        String token = (String) res.getBody().get("access_token");
        session.setAttribute("token", token);
        return ResponseEntity.ok(Map.of("token", token));
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest req, HttpSession session) {
        if (!"password123".equals(req.getPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("error", "Bad credentials"));
        }
        HttpHeaders headers = new HttpHeaders();
        headers.set("X-API-Key", apiKey);
        headers.setContentType(MediaType.APPLICATION_JSON);
        Map<String, Object> payload = Map.of(
                "user_id", "123",
                "email_address", req.getEmail()
        );
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);
        ResponseEntity<Map> res = rest.postForEntity(api2Url + "/internal/login", entity, Map.class);
        String token = (String) res.getBody().get("access_token");
        session.setAttribute("token", token);
        return ResponseEntity.ok(Map.of("token", token));
    }

    @GetMapping("/ping")
    public ResponseEntity<?> ping(HttpSession session) {
        String token = (String) session.getAttribute("token");
        if (token == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("error", "No session"));
        }
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(token);
        HttpEntity<Void> entity = new HttpEntity<>(headers);
        ResponseEntity<String> res = rest.exchange(api2Url + "/protected/ping", HttpMethod.GET, entity, String.class);
        return ResponseEntity.ok(res.getBody());
    }
}
