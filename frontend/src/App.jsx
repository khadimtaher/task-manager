import { useEffect } from "react";
import apiClient from "./api/client";

function App() {
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await apiClient.get("/tasks/");

        console.log("Tasks API Response:", response.data);
      } catch (error) {
        console.error("Tasks API Error:", error);
      }
    };

    fetchTasks();
  }, []);

  return <h1>Task Manager</h1>;
}

export default App;
