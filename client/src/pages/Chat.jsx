import React, { useState, useEffect } from 'react';
import Perfil from '../components/Perfil';
import { Sidebar } from '../components/Sidebar';
import { ChatHeader } from '../components/ChatHeader';
import { AreaMensagens } from '../components/AreaMensagens';
import { ChatInput } from '../components/ChatInput';
import { useContatos } from '../hooks/useContatos';
import { useChatMotor } from '../hooks/useChatMotor';
import { useMobile } from '../hooks/useMobile';
import { useNotificacoes } from '../hooks/useNotificacoes';
import BannerNotificacao from '../components/BannerNotificacao';
import { solicitarPermissaoNotificacoes } from '../services/notifications';

export default function Chat() {
  const [usuarioLogado] = useState(localStorage.getItem('usuario') || 'usuario_teste');
  const [contatoAtivo, setContatoAtivo] = useState(null);
  const [perfilAberto, setPerfilAberto] = useState(false);
  const contatos = useContatos();

  const {
    historico,
    isOnline,
    erroEnvio,
    presencas,
    presencaContato,
    enviarMensagem,
    editarMensagem,
    excluirMensagem,
    novaMensagemRecebida
  } = useChatMotor(usuarioLogado, contatoAtivo);

  const {
    badges,
    bannerAtivo,
    erroConexao,
    exibirBanner,
    zerarBadge,
    incrementarBadge,
    notificarPushESom
  } = useNotificacoes(usuarioLogado, contatoAtivo);

  const isMobile = useMobile();
  const mostrarSidebar = !isMobile || (isMobile && !contatoAtivo);
  const mostrarChat = !isMobile || (isMobile && contatoAtivo);

  const handleSelecionarContato = (contato) => {
    setContatoAtivo(contato);
    const idContato = contato.usuario || contato.email;
    zerarBadge(idContato);
  };

  useEffect(() => {
    solicitarPermissaoNotificacoes();
  }, []);

  useEffect(() => {
    if (novaMensagemRecebida) {
      const idContatoAtivo = contatoAtivo?.usuario || contatoAtivo?.email;
      
      if (novaMensagemRecebida.remetente !== idContatoAtivo) {
        exibirBanner(novaMensagemRecebida.remetente, novaMensagemRecebida.texto);
        notificarPushESom(novaMensagemRecebida.remetente, novaMensagemRecebida.texto);
        incrementarBadge(novaMensagemRecebida.remetente);
      }
    }
  }, [novaMensagemRecebida, contatoAtivo, exibirBanner, notificarPushESom, incrementarBadge]);

  return (
    <>
      <BannerNotificacao
        bannerAtivo={bannerAtivo}
        onFechar={() => {}}
      />

      {erroConexao && (
        <div
          data-cy="banner-erro-conexao"
          style={{
            position: 'fixed',
            top: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: '#dc3545',
            color: '#fff',
            padding: '15px 25px',
            borderRadius: '8px',
            zIndex: 9999,
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
          }}
        >
          Sem conexao. Verifique sua internet.
        </div>
      )}

      <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>
        {mostrarSidebar && (
          <Sidebar
            usuarioLogado={usuarioLogado}
            contatos={contatos}
            contatoAtivo={contatoAtivo}
            presencas={presencas}
            badges={badges}
            onSelectContato={handleSelecionarContato}
            onOpenPerfil={() => setPerfilAberto(true)}
            isMobile={isMobile}
          />
        )}
        {mostrarChat && (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', width: isMobile ? '100%' : 'auto' }}>
            {contatoAtivo ? (
              <>
                <ChatHeader
                  contatoAtivo={contatoAtivo}
                  presencaContato={presencaContato}
                  isMobile={isMobile}
                  onVoltar={() => setContatoAtivo(null)}
                />
                <AreaMensagens
                  historico={historico}
                  usuarioLogado={usuarioLogado}
                  onEditar={editarMensagem}
                  onExcluir={excluirMensagem}
                />
                {erroEnvio && (
                  <div
                    data-cy="alerta-envio"
                    style={{
                      padding: '10px 20px',
                      backgroundColor: '#fff4d6',
                      color: '#6d5200',
                      borderTop: '1px solid #ead18a',
                      fontSize: '0.9rem'
                    }}
                  >
                    {erroEnvio}
                  </div>
                )}
                <ChatInput
                  isOnline={isOnline}
                  onEnviar={enviarMensagem}
                  isMobile={isMobile}
                />
              </>
            ) : (
              <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f4f4f4' }}>
                <h2 style={{ color: '#888' }}>Clique em um contato na barra lateral para iniciar</h2>
              </div>
            )}
          </div>
        )}
      </div>

      {perfilAberto && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(6, 6, 93, 0.35)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
          <Perfil onClose={() => setPerfilAberto(false)} />
        </div>
      )}
    </>
  );
}