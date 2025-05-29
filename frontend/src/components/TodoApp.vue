<template>
  <div class="todo-app">
    <h1>Todo List</h1>
    <form @submit.prevent="addCategory">
      <input v-model="newCategory" placeholder="New category..." />
      <button type="submit">Add</button>
    </form>
    <div class="category">
    <select v-model="selectedCategory">
      <option value="">All Categories</option>
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>   
    </div> 

    <button @click="isModalOpen = true">+ Add Todo</button>
<!-- Modal (oddiy Vue shartli render bilan) -->
    <div v-if="isModalOpen" class="modal-overlay">
      <div class="modal-box">
        <h3>Add New Todo</h3>
        <form @submit.prevent="addTodo">
          <input v-model="newTodo" placeholder="New todo..." />
          <select v-model="selectedCategory">
            <option disabled value="">Select Category</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
          <div class="modal-buttons">
            <button type="submit">Add</button>
            <button type="button" @click="isModalOpen = false">Cancel</button>  
          </div>
        </form>
      </div>
    </div>

    <div class="search-box">
      <input v-model="searchQuery" placeholder="Search todos..." />
    </div>
    <h3>🕒 Incomplete</h3>
    <ul>
      <li v-for="todo in incompleteTodos" :key="todo.id">

        <template v-if="editingId === todo.id">
          <input v-model="editText" />
          <button @click="saveEdit(todo.id)">💾</button>
          <button @click="cancelEdit">❌</button>
        </template>
        <template v-else>
          {{ todo.title }}
          <button @click="startEdit(todo)">✏️</button>
          <button @click="deleteTodo(todo.id)">🗑️</button>
          <button @click="toggleComplete(todo)">✅</button>
        </template>
      </li>
    </ul>

    <h3>✅ Completed</h3>
    <ul>
      <li v-for="todo in completedTodos" :key="todo.id" :class="{ completed: todo.is_complete }">
        <template v-if="editingId === todo.id">
          <input v-model="editText" />
          <button @click="saveEdit(todo.id)">💾</button>
          <button @click="cancelEdit">❌</button>
        </template>
        <template v-else>
          {{ todo.title }}
          <button @click="startEdit(todo)">✏️</button>
          <button @click="deleteTodo(todo.id)">🗑️</button>
          <button @click="toggleComplete(todo)">🕒</button>
        </template>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const todos = ref([])
const newTodo = ref('')
const editingId = ref(null)
const editText = ref('')
const searchQuery = ref('')
const categories = ref([])
const newCategory = ref('')
const isModalOpen = ref(false)
const selectedCategory = ref('')
const weather = ref([])

const filteredTodos = computed(() => {
  return todos.value.filter(todo => {
    const matchesSearch = todo.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === '' || todo.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

const incompleteTodos = computed(() => {
  return filteredTodos.value.filter(todo => !todo.is_complete)
})

const completedTodos = computed(() => {
  return filteredTodos.value
    .filter(todo => todo.is_complete)
    .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
})

// Fetch all todos on page load
const fetchTodos = async () => {
  const response = await axios.get('http://localhost:8000/api/todos/')
  todos.value = response.data
}

// Add a new todo
const addTodo = async () => {
  if (newTodo.value.trim() === '' || selectedCategory.value === '') return
  const response = await axios.post('http://localhost:8000/api/todos/', {
    title: newTodo.value,
    category: selectedCategory.value
  })
  todos.value.unshift(response.data)
  newTodo.value = ''
  selectedCategory.value = ''
  isModalOpen.value = false
}

// Delete a todo
const deleteTodo = async (id) => {
  const confirmDelete = confirm("Are you sure you want to delete this todo?")
  if (!confirmDelete) return
  await axios.delete(`http://localhost:8000/api/todos/${id}/`)
  todos.value = todos.value.filter(todo => todo.id !== id)
}

// Start editing a todo
const startEdit = (todo) => {
  editingId.value = todo.id
  editText.value = todo.title
}

// Cancel edit mode
const cancelEdit = () => {
  editingId.value = null
  editText.value = ''
}

// Save changes to a todo
const saveEdit = async (id) => {
  if (editText.value.trim() === '') return
  try {
    const response = await axios.patch(`http://localhost:8000/api/todos/${id}/`, {
      title: editText.value,
      is_complete: false
    })
    // 1. Eski todo'ni olib tashlaymiz
    const index = todos.value.findIndex(todo => todo.id === id)
    if (index !== -1) {
      todos.value.splice(index, 1) // o‘chirish
    }

    // 2. Yangilangan todo'ni boshiga qo‘shamiz
    todos.value.unshift(response.data)
    cancelEdit()
  } catch (err) {
    alert("Error updating the todo")
    console.error(err)
  }
}

// Toggle completion status
const toggleComplete = async (todo) => {
  try {
    // 1. PATCH orqali yangilaymiz
    const response = await axios.patch(`http://localhost:8000/api/todos/${todo.id}/`, {
      is_complete: !todo.is_complete
    })

    // 2. Eski todo’ni o‘chir
    const index = todos.value.findIndex(t => t.id === todo.id)
    console.log(index)
    console.log(todos.value[index])
    if (index !== -1) {
      todos.value.splice(index, 1)
    }
    console.log(response.data)
    // 3. Qaytgan todo ni boshiga qo‘sh (yangilangan status va updated_at bilan)
    todos.value.unshift(response.data)

  } catch (err) {
    alert("Error toggling status")
    console.error(err)
  }
}

// Category
const addCategory = async () => {
  if (newCategory.value.trim() === '') return
  const response = await axios.post('http://localhost:8000/api/categories/', {
    name: newCategory.value
  })
  categories.value.unshift(response.data)
  newCategory.value = ''
}

const deleteCategory = async (id) => {
  const confirmDelete = confirm("Are you sure you want to delete this category?")
  if (!confirmDelete) return
  await axios.delete(`http://localhost:8000/api/categories/${id}/`)
  categories.value = categories.value.filter(category => category.id !== id)
}

const fetchCategories = async () => {
  const response = await axios.get('http://localhost:8000/api/categories/')
  categories.value = response.data
}

onMounted(fetchTodos)
onMounted(fetchCategories)
</script>







<style scoped>
.todo-app {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', sans-serif;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  flex-grow: 1;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
}

button {
  padding: 10px 12px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  opacity: 0.9;
}

button[type="submit"] {
  background-color: #42b883;
  color: white;
}

li {
  list-style: none;
  background: #f9f9f9;
  padding: 10px;
  margin-bottom: 8px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

li.completed {
  text-decoration: line-through;
  color: gray;
  opacity: 0.6;
}

h3 {
  margin-top: 30px;
  color: #666;
}

.search-box {
  margin-bottom: 15px;
}

.search-box input {
  margin-top: 20px;
  width: 74%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  display: block;
}

.category {
  margin-bottom: 20px;
}

select {
  width: 74%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  display: block;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-box {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
</style>
