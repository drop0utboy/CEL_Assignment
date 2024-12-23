import React, { useEffect, useState } from "react";
import api from "../services/api";
import "./TodoList.css";
import nothingToDoImage from "../assets/images/nothing_to_do.jpg"; // 이미지 불러오기

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [editingId, setEditingId] = useState(null); // 현재 편집 중인 항목 ID
  const [editedTask, setEditedTask] = useState(""); // 편집 중인 내용

  // 기존 To-Do 데이터 가져오기
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await api.get("/todos/");
        const data = response.data;

        // 가져온 데이터가 비어있는 경우 기본 항목 추가
        if (data.length === 0) {
          const defaultTask = { task: "아무것도 안한다", completed: true };
          const defaultResponse = await api.post("/todos/", defaultTask);
          setTodos([defaultResponse.data]);
        } else {
          setTodos(data);
        }
      } catch (error) {
        console.error("To-Do 데이터를 가져오는 중 오류 발생:", error);
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
      console.error("To-Do를 추가하는 중 오류 발생:", error);
    }
  };

  // To-Do 완료 상태 변경
  const toggleCompletion = async (todo) => {
    try {
      const updatedTodo = { ...todo, completed: !todo.completed };
      const response = await api.put(`/todos/${todo.id}`, updatedTodo);
      setTodos(todos.map((t) => (t.id === todo.id ? response.data : t)));
    } catch (error) {
      console.error("To-Do 상태를 변경하는 중 오류 발생:", error);
    }
  };

  // To-Do 삭제
  const deleteTodo = async (id) => {
    try {
      await api.delete(`/todos/${id}`);
      setTodos(todos.filter((todo) => todo.id !== id)); // 상태에서 항목 삭제
    } catch (error) {
      console.error("To-Do를 삭제하는 중 오류 발생:", error);
    }
  };

  // 편집 모드 활성화
  const startEditing = (todo) => {
    setEditingId(todo.id);
    setEditedTask(todo.task);
  };

  // To-Do 내용 저장
  const saveTodo = async (id) => {
    try {
      // 편집 중인 항목 가져오기
      const todoToUpdate = todos.find((todo) => todo.id === id);
  
      // FastAPI 스키마에 맞게 데이터 준비
      const updatedTodo = {
        task: editedTask,            // 수정된 작업 내용
        completed: todoToUpdate.completed, // 기존 완료 상태 유지
      };
  
      console.log("Updating Todo:", updatedTodo); // 디버깅용 로그
      const response = await api.put(`/todos/${id}`, updatedTodo);
  
      // 상태 업데이트
      setTodos(todos.map((todo) => (todo.id === id ? response.data : todo)));
      setEditingId(null); // 편집 모드 해제
    } catch (error) {
      console.error("To-Do 내용을 저장하는 중 오류 발생:", error);
    }
  };

  return (
    <div className="container">
      <h1>To-Do List</h1>

      {/* 상단 이미지 추가 */}
      <img src={nothingToDoImage} alt="Nothing to do" className="header-image" />

      {/* To-Do 추가 폼 */}
      <div className="todo-form">
        <input
          type="text"
          placeholder="할 일을 추가하자"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
        />
        <button className="add-btn" onClick={addTodo}>추가</button>
      </div>

      {/* To-Do 리스트 출력 */}
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <span>ID: {todo.id}</span> {/* ID 표시 */}
            {editingId === todo.id ? (
              <>
                <input
                  type="text"
                  value={editedTask}
                  onChange={(e) => setEditedTask(e.target.value)}
                />
                <button className="save-btn" onClick={() => saveTodo(todo.id)}>저장</button>
                <button className="cancel-btn" onClick={() => setEditingId(null)}>취소</button>
              </>
            ) : (
              <>
                <span
                  className={todo.completed ? "completed" : ""}
                  onClick={() => toggleCompletion(todo)}
                >
                  {todo.task}
                </span>
                <button className="edit-btn" onClick={() => startEditing(todo)}>수정</button>
                <button className="delete-btn" onClick={() => deleteTodo(todo.id)}>삭제</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
