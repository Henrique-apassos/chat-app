import { useEffect, useState, useCallback } from 'react';
import { 
  consultarBadges, 
  marcarComoLidas, 
  exibirNotificacaoPush,
  tocarSomNotificacao
} from '../services/notifications';

export function useNotificacoes(usuarioLogado, contatoAtivo) {
  const [badges, setBadges] = useState({});
  const [bannerAtivo, setBannerAtivo] = useState(null);
  const [erroConexao, setErroConexao] = useState(false);

  const atualizarBadges = useCallback(async () => {
    if (!usuarioLogado) return;
    try {
      const dados = await consultarBadges();
      setBadges(dados);
      setErroConexao(false);
    } catch (erro) {
      setErroConexao(true);
      console.error('Erro ao consultar badges:', erro);
    }
  }, [usuarioLogado]);

  useEffect(() => {
    atualizarBadges();
    const intervalo = setInterval(atualizarBadges, 30000);
    return () => clearInterval(intervalo);
  }, [atualizarBadges]);

  useEffect(() => {
    const totalNaoLidas = Object.values(badges).reduce((sum, val) => sum + val, 0);
    if (totalNaoLidas > 0) {
      document.title = `(${totalNaoLidas}) Chapp`;
    } else {
      document.title = 'Chapp';
    }
  }, [badges]);

  const exibirBanner = useCallback((remetente, texto) => {
    setBannerAtivo({ remetente, texto });
    setTimeout(() => {
      setBannerAtivo(null);
    }, 4000);
  }, []);

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

  const incrementarBadge = useCallback(() => {
    atualizarBadges();
  }, [atualizarBadges]);

  const notificarPushESom = useCallback((remetente, texto) => {
    if (document.hidden) {
      exibirNotificacaoPush(remetente, texto);
    }
    tocarSomNotificacao(remetente);
  }, []);

  return {
    badges,
    bannerAtivo,
    erroConexao,
    exibirBanner,
    zerarBadge,
    incrementarBadge,
    notificarPushESom,
  };
}