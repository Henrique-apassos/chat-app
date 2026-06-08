import { useNavigate } from 'react-router-dom'
import Login from './Login'

export default function Welcome() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen flex">
      {/* Lado esquerdo — sempre visível */}
      <div className="bg-white flex flex-col items-center justify-center p-10 w-full md:w-1/2">
        <div className="bg-[#0E49B5] p-4 rounded-2xl mb-6">
          <span className="text-4xl">💬</span>
        </div>
        <h1 className="text-[#06065D] text-4xl font-bold mb-2 text-center">
          Bem-vindo ao <span className="italic">Chapp!</span>
        </h1>
        <p className="text-[#A2DAE0] text-lg mb-10 text-center">
          Seu app de mensagens favorito!
        </p>
        {/* Botão só aparece no mobile */}
        <button
          onClick={() => navigate('/login')}
          className="md:hidden bg-[#0E49B5] text-white px-12 py-3 rounded-full text-lg font-semibold hover:opacity-90 transition"
        >
          Entrar
        </button>
      </div>

      {/* Lado direito — só aparece no desktop */}
      <div className="hidden md:flex bg-[#0E49B5] w-1/2 items-center justify-center">
        <Login embedded />
      </div>
    </div>
  )
}