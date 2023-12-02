package com.example.firstproject.repository;

import com.example.firstproject.entity.User;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface AuthRepository extends CrudRepository<User, Long> {

    List<User> findByName(String name);
}
