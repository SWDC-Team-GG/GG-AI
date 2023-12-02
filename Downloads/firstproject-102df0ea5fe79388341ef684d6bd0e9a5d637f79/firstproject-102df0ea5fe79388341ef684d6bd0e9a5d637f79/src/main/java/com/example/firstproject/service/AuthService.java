package com.example.firstproject.service;

import com.example.firstproject.dto.UserForm;
import com.example.firstproject.entity.User;
import com.example.firstproject.repository.AuthRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Objects;

@Service
public class AuthService {

    @Autowired
    private AuthRepository authRepository;
    public List<User> findByName(String name) {
        return authRepository.findByName(name);
    }
    public String login(UserForm userForm) {
        User user = (User) authRepository.findByName(userForm.getName());
        if (Objects.equals(user.getPassword(), userForm.password)) {
            return "sec";
        }
        return "no sec";
    }
}
