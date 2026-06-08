import { useNavigate } from 'react-router-dom'

export default function CadastroSucesso() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-[#06065D] flex items-center justify-center p-6">
      <div className="text-center">
        <h1 data-cy="msg-sucesso" className="text-white text-4xl font-bold mb-10">
          Cadastro<br />realizado<br />com sucesso!
        </h1>
        <button
          onClick={() => navigate('/login')}
          className="bg-[#0E49B5] text-white px-12 py-3 rounded-full text-lg font-semibold hover:opacity-90 transition"
        >
          Entrar
        </button>
      </div>
    </div>
  )
}