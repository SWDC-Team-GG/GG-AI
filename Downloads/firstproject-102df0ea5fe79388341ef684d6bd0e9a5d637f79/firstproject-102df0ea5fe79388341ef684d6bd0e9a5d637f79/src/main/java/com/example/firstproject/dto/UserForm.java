package com.example.firstproject.dto;

import com.example.firstproject.entity.User;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

// 어노테이션이라 부른다
// 이걸로 함수 안써도 됨
// 코드 간결성

@AllArgsConstructor
@ToString
public class UserForm {
    @Getter
    private String name;
    public String password;
    public User toEntity() {
        return new User(null, name, password);
    }

}
