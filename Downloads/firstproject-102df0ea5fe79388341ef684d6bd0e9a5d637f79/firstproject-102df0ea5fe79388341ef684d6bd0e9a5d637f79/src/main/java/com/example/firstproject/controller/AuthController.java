package com.example.firstproject.controller;

import com.example.firstproject.dto.UserForm;
import com.example.firstproject.entity.User;
import com.example.firstproject.service.AuthService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
// 이거로 요청 구분
@RequestMapping("/auth")
public class AuthController {
    @Autowired
    private AuthService authService;

    @GetMapping("login")
    public String login() {
        return "LOGIN";
    }
    @PostMapping("login")
    public String createArticle(UserForm form) {
        User user = form.toEntity();
        log.info(user.toString());
        return authService.login(form);
    }
}
