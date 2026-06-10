import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { buscarPerfil, atualizarPerfil, excluirConta } from '../services/api'

export default function Perfil({ onClose }) {
  const navigate = useNavigate()

  const [form, setForm] = useState({
  nome: '',
  sobrenome: '',
  novo_usuario: '',
  telefone: '',
  email: '',
  biografia: '',
    })

    const [usuarioAtual, setUsuarioAtual] = useState('')
    const [mensagem, setMensagem] = useState('')
    const [erro, setErro] = useState('')
    const [carregando, setCarregando] = useState(true)
    const [errosCampos, setErrosCampos] = useState({})
    const [modalExcluirAberto, setModalExcluirAberto] = useState(false)
    const [senhaExclusao, setSenhaExclusao] = useState('')
    const [erroExclusao, setErroExclusao] = useState('')
    const [fotoPreview, setFotoPreview] = useState('')

    function obterUsuarioDoToken() {
        const token = localStorage.getItem('token')

        if (!token) return null

        try {
            const payload = JSON.parse(atob(token.split('.')[1]))
            return payload.sub
        } catch {
            return null
        }
    }

    useEffect(() => {
  async function carregarPerfil() {
    const usuarioSalvo = obterUsuarioDoToken() || localStorage.getItem('usuario')
    const fotoSalva = localStorage.getItem(`foto_${usuarioSalvo}`)

    if (fotoSalva) {
    setFotoPreview(fotoSalva)
    }

    if (!usuarioSalvo) {
      setErro('Usuário não encontrado no navegador. Faça login novamente.')
      setCarregando(false)
      return
    }

    setUsuarioAtual(usuarioSalvo)
    localStorage.setItem('usuario', usuarioSalvo)

    const response = await buscarPerfil(usuarioSalvo)
    const data = await response.json()

    if (response.ok) {
      setForm({
        nome: data.nome || '',
        sobrenome: data.sobrenome || '',
        novo_usuario: data.usuario || '',
        telefone: data.telefone || '',
        email: data.email || '',
        biografia: data.biografia || '',
      })
    } else {
      setErro(data.detail || 'Erro ao carregar perfil')
    }

    setCarregando(false)
  }

  carregarPerfil()
}, [])

function handleSelecionarFoto(e) {
  const arquivo = e.target.files[0]

  if (!arquivo) return

  const leitor = new FileReader()

  leitor.onloadend = () => {
    const imagemBase64 = leitor.result

    setFotoPreview(imagemBase64)
    localStorage.setItem(`foto_${usuarioAtual}`, imagemBase64)
  }

  leitor.readAsDataURL(arquivo)
}

function handleChange(e) {
  const { name, value } = e.target

  setForm({ ...form, [name]: value })
  setMensagem('')
  setErro('')

  setErrosCampos({
    ...errosCampos,
    [name]: '',
  })
}

async function handleSalvar() {
  const dados = {
    usuario: usuarioAtual,
    novo_usuario: form.novo_usuario,
    nome: form.nome,
    sobrenome: form.sobrenome,
    telefone: form.telefone,
    email: form.email,
    biografia: form.biografia,
  }

  const response = await atualizarPerfil(dados)
  const data = await response.json()

  if (response.ok) {
    setMensagem('Perfil atualizado com sucesso')

    if (form.novo_usuario !== usuarioAtual) {
      localStorage.setItem('usuario', form.novo_usuario)
      setUsuarioAtual(form.novo_usuario)
    }
  } else {
    setErro(data.detail || 'Erro ao atualizar perfil')
  }
}

function tratarErroCampo(data) {
  const mensagemErro = data.detail

  if (typeof mensagemErro === 'string') {
    if (mensagemErro.includes('E-mail')) {
      setErrosCampos({ email: mensagemErro })
      return
    }

    if (mensagemErro.includes('Telefone')) {
      setErrosCampos({ telefone: mensagemErro })
      return
    }

    if (mensagemErro.includes('Nome de usuário')) {
      setErrosCampos({ novo_usuario: mensagemErro })
      return
    }

    setErro(mensagemErro)
    return
  }

  if (Array.isArray(mensagemErro)) {
    const errosFormatados = {}

    mensagemErro.forEach((erro) => {
      const campo = erro.loc?.[1]
      const mensagem = erro.msg?.replace('Value error, ', '')

      if (campo === 'biografia') {
        errosFormatados.biografia = mensagem
      }

      if (campo === 'email') {
        errosFormatados.email = mensagem
      }
    })

    setErrosCampos(errosFormatados)
    return
  }

  setErro('Erro ao atualizar perfil')
}

async function handleSalvarEFechar() {
    setErro('')
    setErrosCampos({})

  const dados = {
    usuario: usuarioAtual,
    novo_usuario: form.novo_usuario,
    nome: form.nome,
    sobrenome: form.sobrenome,
    telefone: form.telefone,
    email: form.email,
    biografia: form.biografia,
  }

  const response = await atualizarPerfil(dados)
  const data = await response.json()

  if (response.ok) {
    if (form.novo_usuario !== usuarioAtual) {
      localStorage.setItem('usuario', form.novo_usuario)
      setUsuarioAtual(form.novo_usuario)
    }

    onClose?.()
  } else {
    tratarErroCampo(data)
  }
}

if (carregando) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      Carregando perfil...
    </div>
  )
}

async function handleExcluirConta() {
  setErroExclusao('')

  const response = await excluirConta(usuarioAtual, senhaExclusao)
  const data = await response.json()

  if (response.ok) {
    localStorage.removeItem('usuario')
    localStorage.removeItem('token')
    navigate('/')
  } else {
    setErroExclusao(data.detail || 'Erro ao excluir conta')
  }
}

  return (
    <div
      className="flex items-center justify-center">
      <div
        data-cy="modal-configuracoes"
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-5xl bg-white rounded-3xl shadow-lg overflow-hidden flex"
      >
        <aside className="w-2/5 bg-[#EEEEEE] p-8">
          <h1 className="text-4xl font-bold text-[#06065D] mb-10">
            Configurações
          </h1>

          <div className="border-b border-gray-300 pb-5 mb-5">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold text-[#06065D] text-lg">
                  Configurações de perfil
                </h2>
                <p className="text-sm text-[#0E49B5] mt-2 max-w-64 leading-tight">
                  Imagem de perfil, nome, sobrenome, nome de usuário,
                  telefone, email e biografia.
                </p>
              </div>

              <span className="text-3xl text-[#06065D]">›</span>
            </div>
          </div>

            <div className="border-b border-gray-300 pb-5 mb-5 flex items-center justify-between">
                <h2 className="font-bold text-[#06065D] text-lg">
                    Notificações
                </h2>

                <div className="w-12 h-7 bg-gray-300 rounded-full flex items-center px-1">
                    <div className="w-5 h-5 bg-white rounded-full shadow" />
                </div>
                </div>

                <button
                 data-cy="btn-sair-conta"
                onClick={() => {
                    localStorage.removeItem('usuario')
                    localStorage.removeItem('token')
                    navigate('/')
                }}
                className="block text-[#06065D] text-lg mb-5 hover:underline"
                >
                Sair da conta
                </button>

                <button
                data-cy="btn-excluir-conta"
                onClick={() => setModalExcluirAberto(true)}
                className="text-red-600 text-lg hover:underline"
                >
                Excluir conta
                </button>
        </aside>

        <main className="w-3/5 p-8">
          <div className="flex gap-8">
            <div className="flex flex-col items-center">
              <div className="w-28 h-28 bg-[#B5C9CC] rounded-full flex items-center justify-center relative">

                {fotoPreview ? (
                    <img
                    data-cy="foto-perfil"
                    src={fotoPreview}
                    alt="Foto de perfil"
                    className="w-full h-full object-cover rounded-full"
                    />
                ) : (
                    <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="white"
                    className="w-20 h-20"
                    >
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4Zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4Z" />
                    </svg>
                )}

                <input
                    data-cy="input-foto"
                    id="input-foto"
                    type="file"
                    accept="image/*"
                    onChange={handleSelecionarFoto}
                    className="hidden"
                />

                <label
                    htmlFor="input-foto"
                    className="absolute bottom-0 right-0 w-9 h-9 bg-[#06065D] text-white rounded-full flex items-center justify-center cursor-pointer"
                >
                    <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="white"
                    className="w-5 h-5"
                    >
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25Zm17.71-10.04a1.003 1.003 0 0 0 0-1.42l-2.5-2.5a1.003 1.003 0 0 0-1.42 0l-1.96 1.96 3.75 3.75 2.13-1.79Z" />
                    </svg>
                </label>

                </div>
            </div>

            <div className="flex-1">
              <input
                data-cy="input-nome"
                name="nome"
                value={form.nome}
                onChange={handleChange}
                placeholder="Nome"
                className="w-full bg-[#D1F0F2] rounded-xl px-4 py-3 mb-3 text-[#06065D] outline-none"
              />

              <input
                data-cy="input-sobrenome"
                name="sobrenome"
                value={form.sobrenome}
                onChange={handleChange}
                placeholder="Sobrenome"
                className="w-full bg-[#D1F0F2] rounded-xl px-4 py-3 mb-3 text-[#06065D] outline-none"
              />

              <input
                data-cy="input-usuario"
                name="novo_usuario"
                value={form.novo_usuario}
                onChange={handleChange}
                placeholder="Nome de usuário"
                className="w-full bg-[#D1F0F2] rounded-xl px-4 py-3 mb-4 text-[#06065D] outline-none"
              />

              {errosCampos.novo_usuario && (
               
                <p data-cy="erro-usuario" className="text-red-600 text-xs mb-3 -mt-2">
                    {errosCampos.novo_usuario}
                </p>
                )}
            </div>
          </div>

          <input
            data-cy="input-telefone"
            name="telefone"
            value={form.telefone}
            onChange={handleChange}
            placeholder="Telefone"
            className="w-full bg-[#D1F0F2] rounded-xl px-4 py-4 mb-4 text-[#06065D] outline-none"
          />

          {errosCampos.telefone && (
            <p data-cy="erro-telefone" className="text-red-600 text-xs mb-3 -mt-2">
                {errosCampos.telefone}
            </p>
            )}

          <input
            data-cy="input-email-perfil"
            name="email"
            value={form.email}
            onChange={handleChange}
            placeholder="Email"
            type="email"
            className="w-full bg-[#D1F0F2] rounded-xl px-4 py-4 mb-4 text-[#06065D] outline-none"
          />

          {errosCampos.email && (
            <p data-cy="erro-email" className="text-red-600 text-xs mb-3 -mt-2">
                {errosCampos.email}
            </p>
            )}

          <textarea
            data-cy="input-biografia"
            name="biografia"
            value={form.biografia}
            onChange={handleChange}
            placeholder="Biografia"
            className="w-full bg-[#D1F0F2] rounded-xl px-4 py-4 h-44 resize-none text-[#06065D] outline-none"
          />

            {errosCampos.biografia && (
                <p data-cy="erro-biografia" className="text-red-600 text-xs mb-3 mt-1">
                    {errosCampos.biografia}
                </p>
                )}

            {erro && Object.keys(errosCampos).length === 0 && (
            <p data-cy="erro-generico" className="text-red-600 text-sm text-center mt-4">
                {erro}
            </p>
            )}

          <div className="flex justify-end mt-8">
            <button 
            data-cy="btn-ok-perfil"
            onClick={handleSalvarEFechar}
            className="bg-[#0E49B5] text-white px-14 py-3 rounded-full font-semibold hover:opacity-90 transition">
              Ok
            </button>
          </div>
        </main>
      </div>
      {modalExcluirAberto && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
            <div 
                data-cy="modal-excluir-conta"
                onClick={(e) => e.stopPropagation()}
                className="bg-white rounded-2xl p-8 w-full max-w-md shadow-lg">
            <h2 className="text-2xl font-bold text-[#06065D] mb-3">
                Excluir conta
            </h2>

            <p className="text-[#06065D] mb-5">
                Para confirmar a exclusão da conta, digite sua senha.
            </p>

            <input
                data-cy="input-senha-exclusao"
                type="password"
                value={senhaExclusao}
                onChange={(e) => {
                setSenhaExclusao(e.target.value)
                setErroExclusao('')
                }}
                placeholder="Senha"
                className="w-full bg-[#D1F0F2] rounded-xl px-4 py-3 mb-3 text-[#06065D] outline-none"
            />

            {erroExclusao && (
                <p data-cy="erro-exclusao" className="text-red-600 text-sm mb-4">
                {erroExclusao}
                </p>
            )}

            <div className="flex justify-end gap-3 mt-6">
                <button
                data-cy="btn-cancelar-exclusao"
                onClick={() => {
                    setModalExcluirAberto(false)
                    setSenhaExclusao('')
                    setErroExclusao('')
                }}
                className="px-6 py-3 rounded-full bg-gray-300 text-[#06065D] font-semibold"
                >
                Cancelar
                </button>

                <button
                data-cy="btn-confirmar-exclusao"
                onClick={handleExcluirConta}
                className="px-6 py-3 rounded-full bg-red-600 text-white font-semibold hover:opacity-90"
                >
                Excluir
                </button>
            </div>
            </div>
        </div>
        )}
    </div>
  )
}