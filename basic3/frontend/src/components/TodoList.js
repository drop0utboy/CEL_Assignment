import React, { useEffect, useState } from "react";
import api from "../services/api";
import TodoForm from "./TodoForm";
import "./TodoList.css"; // CSS 파일 추가

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

  // To-Do 완료 상태 변경 함수
  const toggleCompletion = async (todo) => {
    try {
      const updatedTodo = { ...todo, completed: !todo.completed }; // 상태 반전
      const response = await api.put(`/todos/${todo.id}`, updatedTodo); // 서버에 PUT 요청
      setTodos(
        todos.map((t) => (t.id === todo.id ? response.data : t)) // 상태 업데이트
      );
    } catch (error) {
      console.error("Error updating todo:", error);
    }
  };

  // To-Do 항목 삭제 함수
  const deleteTodo = async (id) => {
    try {
      await api.delete(`/todos/${id}`); // 서버에 DELETE 요청
      setTodos(todos.filter((todo) => todo.id !== id)); // 상태에서 제거
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  };

  return (
    <div className="container">
      <h1>To-Do List</h1>

      {/* To-Do 추가 폼 */}
      <TodoForm onSubmit={addTodo} />

      {/* To-Do 리스트 출력 */}
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <span
              onClick={() => toggleCompletion(todo)} // 클릭 시 완료 상태 반전
              style={{
                textDecoration: todo.completed ? "line-through" : "none", // 완료 상태에 따라 스타일 변경
                cursor: "pointer",
              }}
            >
              {todo.task}
            </span>
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
