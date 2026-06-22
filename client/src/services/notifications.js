import { API_URL } from './api';

export async function consultarBadges() {
  const token = localStorage.getItem('token');
  const headers = token
    ? { 'Authorization': `Bearer ${token}` }
    : {};

  const response = await fetch(`${API_URL}/api/v1/notifications/badges`, {
    method: 'GET',
    headers,
  });

  if (!response.ok) {
    if (response.status === 503) {
      throw new Error('Serviço temporariamente indisponível');
    }
    throw new Error('Erro ao consultar notificações');
  }

  return response.json();
}

export async function marcarComoLidas(contato) {
  const token = localStorage.getItem('token');
  const usuario = localStorage.getItem('usuario');
  const headers = token
    ? { 'Authorization': `Bearer ${token}` }
    : {};

  const response = await fetch(
    `${API_URL}/mensagens/${usuario}/${contato}/lidas`,
    {
      method: 'POST',
      headers,
    }
  );

  if (!response.ok) {
    throw new Error('Erro ao marcar mensagens como lidas');
  }

  return response.json();
}

export function solicitarPermissaoNotificacoes() {
  if ('Notification' in window) {
    Notification.requestPermission().then(permission => {
      if (permission === 'granted') {
        console.log('Permissão de notificação concedida');
      }
    });
  }
}

export function exibirNotificacaoPush(remetente, texto) {
  if ('Notification' in window && Notification.permission === 'granted') {
    const notificacao = new Notification(`Nova mensagem de ${remetente}`, {
      body: texto,
      icon: '/favicon.svg',
    });

    notificacao.onclick = () => {
      window.focus();
      notificacao.close();
    };
  }
}

export function tocarSomNotificacao(remetente) {
  const sonsCustomizados = JSON.parse(localStorage.getItem('sons_customizados') || '{}');
  const somUrl = sonsCustomizados[remetente] || '/sounds/notification.mp3';

  const audio = new Audio(somUrl);
  audio.play().catch(e => {
    console.warn('Áudio bloqueado pelo navegador. É necessário interagir com a tela antes.', e);
  });
}