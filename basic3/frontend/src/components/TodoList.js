import React, { useEffect, useState } from "react";
import api from "../services/api";
import TodoForm from "./TodoForm";

const TodoList = () => {
  const [todos, setTodos] = useState([]); // To-Do 리스트 상태

  // API에서 기존 To-Do 데이터 가져오기
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await api.get("/todos/");
        setTodos(response.data); // 서버에서 가져온 데이터로 상태 업데이트
      } catch (error) {
        console.error("Error fetching todos:", error);
      }
    };

    fetchTodos();
  }, []);

  // 새로운 To-Do 추가
  const addTodo = async (newTodo) => {
    try {
      const response = await api.post("/todos/", newTodo); // 서버로 POST 요청
      setTodos([...todos, response.data]); // 성공 시 상태에 추가
    } catch (error) {
      console.error("Error adding todo:", error);
    }
  };

  return (
    <div>
      <h1>To-Do List</h1>

      {/* To-Do 추가 폼 */}
      <TodoForm onSubmit={addTodo} />

      {/* To-Do 리스트 출력 */}
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            {todo.task} - {todo.completed ? "Done" : "Not Done"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
