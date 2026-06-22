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
    const intervalo = setInterval(consultar, 30000);
    return () => clearInterval(intervalo);
  }, [usuarioLogado]);

  // Atualiza o título da aba do navegador (Cenário do Feature)
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

  // Notifica visualmente (Push) e com áudio
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
    notificarPushESom,
  };
}