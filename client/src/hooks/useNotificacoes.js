import { useEffect, useState, useCallback } from 'react';
import { consultarBadges, marcarComoLidas, exibirNotificacaoPush } from '../services/notifications';

export function useNotificacoes(usuarioLogado, contatoAtivo) {
  const [badges, setBadges] = useState({});
  const [bannerAtivo, setBannerAtivo] = useState(null);
  const [erroConexao, setErroConexao] = useState(false);

  // Consultar badges periodicamente
  useEffect(() => {
    if (!usuarioLogado) return;

    const consultar = async () => {
      try {
        const dados = await consultarBadges();
        setBadges(dados);
        setErroConexao(false);
      } catch (erro) {
        setErroConexao(true);
        console.error('Erro ao consultar badges:', erro);
      }
    };

    consultar();
    const intervalo = setInterval(consultar, 30000); // A cada 30 segundos
    return () => clearInterval(intervalo);
  }, [usuarioLogado]);

  // Exibir banner quando mensagem chega
  const exibirBanner = useCallback((remetente, texto) => {
    setBannerAtivo({ remetente, texto });
    setTimeout(() => {
      setBannerAtivo(null);
    }, 4000);
  }, []);

  // Zerar badge ao abrir conversa
  const zerarBadge = useCallback(async (contato) => {
    try {
      await marcarComoLidas(contato);
      setBadges(prev => {
        const novosBadges = { ...prev };
        delete novosBadges[contato];
        return novosBadges;
      });
    } catch (erro) {
      console.error('Erro ao zerar badge:', erro);
    }
  }, []);

  // Exibir notificação push
  const notificarPush = useCallback((remetente, texto) => {
    if (document.hidden) {
      exibirNotificacaoPush(remetente, texto);
    }
  }, []);

  return {
    badges,
    bannerAtivo,
    erroConexao,
    exibirBanner,
    zerarBadge,
    notificarPush,
  };
}