import React, { useEffect, useState } from "react";
import { getAllTodos, deleteTodo } from "../services/todoService";

const TodoList = () => {
  const [todos, setTodos] = useState([]);

  // 모든 To-Do 항목 가져오기
  useEffect(() => {
    const fetchTodos = async () => {
      const data = await getAllTodos();
      setTodos(data);
    };

    fetchTodos();
  }, []);

  // 항목 삭제 처리
  const handleDelete = async (id) => {
    await deleteTodo(id);
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  return (
    <div>
      <h1>To-Do List</h1>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            {todo.task} - {todo.completed ? "Done" : "Not Done"}
            <button onClick={() => handleDelete(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
