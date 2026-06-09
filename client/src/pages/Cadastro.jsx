import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { cadastrar } from '../services/api'
import FormCard from '../components/FormCard'

export default function Cadastro() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    email: '',
    telefone: '',
    usuario: '',
    senha: '',
  })
  const [erro, setErro] = useState('')
  const [carregando, setCarregando] = useState(false)

  function handleChange(e) {
    let { name, value } = e.target

    if (name === 'telefone') {
      value = value.replace(/\D/g, '')
      if (value.length <= 10) {
        value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3')
      } else {
        value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3')
      }
    }

    setForm({ ...form, [name]: value })
    setErro('')
  }

  function validar() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    const telefoneRegex = /^\(\d{2}\) \d{4,5}-\d{4}$/

    if (!emailRegex.test(form.email)) {
      setErro('E-mail inválido')
      return false
    }
    if (!telefoneRegex.test(form.telefone)) {
      setErro('Telefone inválido. Use o formato (88) 98888-8888')
      return false
    }
    if (form.usuario.trim().length < 3) {
      setErro('Nome de usuário deve ter no mínimo 3 caracteres')
      return false
    }
    if (form.senha.length < 6) {
      setErro('A senha deve ter no mínimo 6 caracteres')
      return false
    }
    return true
  }

  async function handleSubmit() {
    if (!validar()) return

    setCarregando(true)
    try {
      const response = await cadastrar(form)
      const data = await response.json()

      if (response.ok) {
        navigate('/cadastro-sucesso')
      } else {
        setErro(data.detail || 'Erro ao cadastrar')
      }
    } catch {
      setErro('Erro de conexão com o servidor')
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#06065D] flex items-center justify-center p-6">
      <FormCard titulo="Cadastro">
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
          data-cy="input-telefone"
          name="telefone"
          type="text"
          placeholder="(88) 98888-8888"
          value={form.telefone}
          onChange={handleChange}
          maxLength={15}
          className="w-full bg-[#A2DAE0] rounded-lg px-4 py-2 mb-3 text-[#06065D] placeholder-[#06065D] outline-none"
        />
        <input
          data-cy="input-usuario"
          name="usuario"
          type="text"
          placeholder="nome de usuário"
          value={form.usuario}
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
          className="w-full bg-[#A2DAE0] rounded-lg px-4 py-2 mb-1 text-[#06065D] placeholder-[#06065D] outline-none"
        />
        <p className="text-xs text-gray-400 mb-3">mínimo 6 caracteres</p>

        {erro && (
          <p data-cy="msg-erro" className="text-[#ED0101] text-sm text-center mb-3">{erro}</p>
        )}

        <button
          data-cy="btn-cadastrar"
          onClick={handleSubmit}
          disabled={carregando}
          className="w-full bg-[#0E49B5] text-white py-3 rounded-full font-semibold hover:opacity-90 transition mb-3"
        >
          {carregando ? 'Cadastrando...' : 'Cadastre-se'}
        </button>

        <p className="text-center text-sm text-[#06065D]">
          Já tem conta?{' '}
          <button onClick={() => navigate('/')} className="hover:underline font-semibold">
            Entrar
          </button>
        </p>
      </FormCard>
    </div>
  )
}