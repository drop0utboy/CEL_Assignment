import React, { useEffect, useState } from "react";
import api from "../services/api";
import "./TodoList.css";

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [newTask, setNewTask] = useState("");

  // 기존 To-Do 데이터 가져오기
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await api.get("/todos/");
        setTodos(response.data);
      } catch (error) {
        console.error("Error fetching todos:", error);
      }
    };
    fetchTodos();
  }, []);

  // 새로운 To-Do 추가
  const addTodo = async () => {
    if (!newTask.trim()) return; // 빈 값 방지
    try {
      const response = await api.post("/todos/", { task: newTask, completed: false });
      setTodos([...todos, response.data]);
      setNewTask(""); // 입력 필드 초기화
    } catch (error) {
      console.error("Error adding todo:", error);
    }
  };

  // To-Do 완료 상태 변경
  const toggleCompletion = async (todo) => {
    try {
      const updatedTodo = { ...todo, completed: !todo.completed };
      const response = await api.put(`/todos/${todo.id}`, updatedTodo);
      setTodos(todos.map((t) => (t.id === todo.id ? response.data : t)));
    } catch (error) {
      console.error("Error updating todo:", error);
    }
  };

  // To-Do 삭제
  const deleteTodo = async (id) => {
    try {
      await api.delete(`/todos/${id}`);
      setTodos(todos.filter((todo) => todo.id !== id));
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  };

  return (
    <div className="container">
      <h1>To-Do List</h1>

      {/* To-Do 추가 폼 */}
      <div className="todo-form">
        <input
          type="text"
          placeholder="Add a new task..."
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
        />
        <button onClick={addTodo}>Add</button>
      </div>

      {/* To-Do 리스트 출력 */}
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <span
              className={todo.completed ? "completed" : ""}
              onClick={() => toggleCompletion(todo)}
            >
              {todo.task}
            </span>
            <button className="delete-btn" onClick={() => deleteTodo(todo.id)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
