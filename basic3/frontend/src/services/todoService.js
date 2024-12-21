import api from "./api"; // Axios 설정 파일

// 모든 To-Do 항목 조회
export const getAllTodos = async () => {
  const response = await api.get("/todos/");
  return response.data;
};

// 특정 To-Do 항목 조회
export const getTodoById = async (id) => {
  const response = await api.get(`/todos/${id}`);
  return response.data;
};

// To-Do 항목 생성
export const createTodo = async (todo) => {
  const response = await api.post("/todos/", todo);
  return response.data;
};

// To-Do 항목 업데이트
export const updateTodo = async (id, todo) => {
  const response = await api.put(`/todos/${id}`, todo);
  return response.data;
};

// To-Do 항목 삭제
export const deleteTodo = async (id) => {
  const response = await api.delete(`/todos/${id}`);
  return response.data;
};
