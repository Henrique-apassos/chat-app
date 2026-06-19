import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Welcome from './pages/Welcome'
import Login from './pages/Login'
import Cadastro from './pages/Cadastro'
import CadastroSucesso from './pages/CadastroSucesso'
import Chat from './pages/Chat'
import Perfil from './components/Perfil'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/cadastro-sucesso" element={<CadastroSucesso />} />
        <Route path='/chat' element={<Chat/>} />
        <Route path="/perfil" element={<Perfil />} />
      </Routes>
    </BrowserRouter>
  )
}