import axios from "axios";

// Axios 인스턴스 생성
const api = axios.create({
  baseURL: "http://localhost:8000", // FastAPI 서버 주소
  timeout: 5000, // 요청 타임아웃 설정 (선택적)
});

// API 인스턴스 내보내기
export default api;
