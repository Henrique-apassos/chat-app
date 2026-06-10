// Descobre o IP de quem acessou a página
const HOST = window.location.hostname;

// Monta as URLs base do backend
export const API_URL = `http://${HOST}:8000`;
export const WS_URL = `ws://${HOST}:8000`;

export async function cadastrar(dados) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados),
  })
  return response
}

export async function login(dados) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados),
  })
  return response
}

export async function buscarPerfil(usuario) {
  const response = await fetch(`${API_URL}/user/profile/${usuario}`)
  return response
}

export async function atualizarPerfil(dados) {
  const response = await fetch(`${API_URL}/user/profile`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados),
  })

  return response
}

export async function excluirConta(usuario, senha) {
  const response = await fetch(`${API_URL}/user/profile/${usuario}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ senha }),
  })

  return response
}