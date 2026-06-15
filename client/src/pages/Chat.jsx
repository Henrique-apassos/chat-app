import React, { useState } from 'react';
import Perfil from '../components/Perfil';
import { Sidebar } from '../components/Sidebar';
import { ChatHeader } from '../components/ChatHeader';
import { AreaMensagens } from '../components/AreaMensagens';
import { ChatInput } from '../components/ChatInput';

// Importação dos seus Hooks de Negócio
import { useContatos } from '../hooks/useContatos';
import { useChatMotor } from '../hooks/useChatMotor';
import { useMobile } from '../hooks/useMobile';

export default function Chat() {
    // Estados Simples da Interface
    const [usuarioLogado] = useState(localStorage.getItem('usuario') || 'usuario_teste');
    const [contatoAtivo, setContatoAtivo] = useState(null);
    const [perfilAberto, setPerfilAberto] = useState(false);

    // Regras de Negócio (Consumindo os seus Hooks)
    const contatos = useContatos();
    const {
        historico,
        isOnline,
        enviarMensagem,
        editarMensagem,
        excluirMensagem
    } = useChatMotor(usuarioLogado, contatoAtivo);

    // Ajuste para celular
    const isMobile = useMobile();
    const mostrarSidebar = !isMobile || (isMobile && !contatoAtivo);
    const mostrarChat = !isMobile || (isMobile && contatoAtivo);

    return (
        <>
            <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>
                {mostrarSidebar && (
                    <Sidebar
                        usuarioLogado={usuarioLogado}
                        contatos={contatos}
                        contatoAtivo={contatoAtivo}
                        onSelectContato={setContatoAtivo}
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
                                    isMobile={isMobile}
                                    onVoltar={() => setContatoAtivo(null)} // Botão para fechar o chat no celula
                                />

                                <AreaMensagens
                                    historico={historico}
                                    usuarioLogado={usuarioLogado}
                                    onEditar={editarMensagem}
                                    onExcluir={excluirMensagem}
                                />

                                <ChatInput
                                    isOnline={isOnline}
                                    onEnviar={enviarMensagem}
                                    isMobile={isMobile}
                                />
                            </>
                        ) : (
                            // Esta mensagem agora só aparece no Desktop
                            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f4f4f4' }}>
                                <h2 style={{ color: '#888' }}>Clique em um contato na barra lateral para iniciar</h2>
                            </div>
                        )}
                    </div>
                )}
            </div>
            {/* ... Modal do Perfil ... */}
            {perfilAberto && (
                <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(6, 6, 93, 0.35)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
                    <Perfil onClose={() => setPerfilAberto(false)} />
                </div>
            )}
        </>
    );
}