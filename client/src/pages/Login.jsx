import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../services/api'
import FormCard from '../components/FormCard'
import { API_URL } from '../services/api'

export default function Login({ embedded = false }) {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', senha: '' })
  const [erro, setErro] = useState('')
  const [carregando, setCarregando] = useState(false)

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
    setErro('')
  }

  async function handleSubmit() {
    setCarregando(true)
    try {
      const response = await login(form)
      const data = await response.json()

      if (response.ok) {
        // Salva o token de autorização
        localStorage.setItem('token', data.access_token)
        
        // Bate na rota /me para pegar o nome de usuário real
        try {
          const meResponse = await fetch(`${API_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${data.access_token}` }
          })

          if (meResponse.ok) {
            const meData = await meResponse.json()
            // Salva o nome_usuario real que veio do banco de dados!
            localStorage.setItem('usuario', meData.nome_usuario || meData.usuario)
          }
        } catch (error) {
          console.error("Erro ao buscar dados do usuário", error)
        }
        navigate('/chat')
      }
      else {
        setErro(data.detail || 'Erro ao fazer login')
        setForm({ ...form, senha: '' })
      }
    } catch {
      setErro('Erro de conexão com o servidor')
    } finally {
      setCarregando(false)
    }
  }

  const card = (
    <FormCard titulo="Login">
      <input
        data-cy="input-email"
        name="email"
        type="email"
        placeholder="e-mail"
        value={form.email}
        onChange={handleChange}
        className="w-full bg-[#A2DAE0] rounded-lg px-4 py-2 mb-3 text-[#06065D] placeholder-[#06065D] outline-none"
      />
      <input
        data-cy="input-senha"
        name="senha"
        type="password"
        placeholder="senha"
        value={form.senha}
        onChange={handleChange}
        className="w-full bg-[#A2DAE0] rounded-lg px-4 py-2 mb-3 text-[#06065D] placeholder-[#06065D] outline-none"
      />

      {erro && (
        <p data-cy="msg-erro" className="text-[#ED0101] text-sm text-center mb-3">{erro}</p>
      )}

      <button
        data-cy="btn-entrar"
        onClick={handleSubmit}
        disabled={carregando}
        className="w-full bg-[#0E49B5] text-white py-3 rounded-full font-semibold hover:opacity-90 transition mb-3"
      >
        {carregando ? 'Entrando...' : 'Entrar'}
      </button>

      <p className="text-center text-sm text-[#06065D]">
        <button onClick={() => navigate('/cadastro')} className="hover:underline">
          Criar conta
        </button>
      </p>
    </FormCard>
  )

  if (embedded) return card

  return (
    <div className="min-h-screen bg-[#06065D] flex items-center justify-center p-6">
      {card}
    </div>
  )
}