import React, { useState } from "react";

const TodoForm = ({ onSubmit, initialValues = { task: "", completed: false } }) => {
  const [todo, setTodo] = useState(initialValues);

  // 입력 변경 처리
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setTodo({
      ...todo,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  // 폼 제출 처리
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(todo);
    setTodo({ task: "", completed: false }); // 초기화
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Task:</label>
        <input
          type="text"
          name="task"
          value={todo.task}
          onChange={handleChange}
          placeholder="Enter your task"
          required
        />
      </div>
      <div>
        <label>Completed:</label>
        <input
          type="checkbox"
          name="completed"
          checked={todo.completed}
          onChange={handleChange}
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default TodoForm;
