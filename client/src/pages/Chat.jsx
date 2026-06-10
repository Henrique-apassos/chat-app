import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Perfil from './Perfil';
import MensagemItem from '../components/MensagemItem';
import { API_URL, WS_URL } from '../services/api';

export default function Chat() {
    const navigate = useNavigate();

    // Quem sou eu? (Pega o usuário salvo no localStorage durante o Login)
    const [usuarioLogado] = useState(localStorage.getItem('usuario') || 'usuario_teste');

    // Estados da Interface
    const [contatos, setContatos] = useState([]);           
    const [contatoAtivo, setContatoAtivo] = useState(null); 
    const [mensagem, setMensagem] = useState('');           
    const [historico, setHistorico] = useState([]);         
    const [perfilAberto, setPerfilAberto] = useState(false);

    const ws = useRef(null);
    const fimDoChatRef = useRef(null);

    // Efeito para buscar a lista de contatos do backend
    useEffect(() => {
        const buscarContatos = async () => {
            try {
                const resposta = await fetch(`${API_URL}/auth/usuarios`);

                if (resposta.ok) {
                    const dados = await resposta.json();
                    setContatos(dados);
                } else {
                    throw new Error("Rota não encontrada ou erro no servidor");
                }
            } catch (error) {
                console.error("Erro ao carregar os contatos reais:", error);
                setContatos([
                    { usuario: 'maria', nome: 'Maria Silva' },
                    { usuario: 'joao', nome: 'João Pedro' },
                    { usuario: 'carlos', nome: 'Carlos Tech' }
                ]);
            }
        };

        buscarContatos();
    }, []);

    // Efeito para conectar no WebSocket (O Motor do Chat)
    useEffect(() => {
        if (!usuarioLogado) return;

        ws.current = new WebSocket(`${WS_URL}/ws/${usuarioLogado}`);
        ws.current.onopen = () => console.log("WebSocket Conectado como:", usuarioLogado);

        ws.current.onmessage = (event) => {
            try {
                // O backend agora manda um JSON perfeito com o ID real!
                const pacote = JSON.parse(event.data);

                if (pacote.texto) {
                    setHistorico((prev) => [...prev, {
                        id_mensagem: pacote.id_mensagem,
                        texto: pacote.texto,
                        remetente: pacote.remetente 
                    }]);
                }
            } catch (e) {
                console.error("Erro ao ler mensagem do websocket:", e);
            }
        };
        
        return () => ws.current?.close();
    }, [usuarioLogado]);

    // Efeito para rolar o chat para o fim sempre que chegar mensagem nova
    useEffect(() => {
        fimDoChatRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [historico]);

    // Efeito para carregar o histórico de mensagens quando muda de contato
    useEffect(() => {
        const carregarHistorico = async () => {
            if (!contatoAtivo) return;

            try {
                setHistorico([]);

                const destinatario = contatoAtivo.usuario || contatoAtivo.email;
                if (!destinatario) return; 

                const resposta = await fetch(`${API_URL}0/mensagens/${usuarioLogado}/${destinatario}`);

                if (resposta.ok) {
                    const mensagensAntigas = await resposta.json();

                    const historicoFormatado = mensagensAntigas.map(msg => ({
                        id_mensagem: msg.id_mensagem, 
                        texto: msg.texto,
                        remetente: msg.remetente,
                        editada: msg.editada || false
                    }));

                    setHistorico(historicoFormatado);
                }
            } catch (erro) {
                console.error("Erro ao carregar o histórico:", erro);
            }
        };

        carregarHistorico();
    }, [contatoAtivo, usuarioLogado]);

    // Função para Enviar a Mensagem
    const enviarMensagem = () => {
        if (!mensagem.trim() || !contatoAtivo) return;

        const pacote = {
            para: contatoAtivo.usuario || contatoAtivo.email,
            texto: mensagem
        };

        // Envia para o servidor. O WebSocket se encarregará de colocar na tela com o ID real!
        ws.current.send(JSON.stringify(pacote));
        setMensagem('');
    };

    // Função responsável por editar uma mensagem
    const editarMensagem = async (msg) => {
        const novoTexto = prompt("Novo texto da mensagem:", msg.texto);
        if (!novoTexto) return;

        const resposta = await fetch(`${API_URL}/mensagens/${msg.id_mensagem}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                usuario: usuarioLogado,
                novo_texto: novoTexto
            })
        });

        if (resposta.ok) {
            setHistorico((prev) =>
                prev.map((m) =>
                    m.id_mensagem === msg.id_mensagem
                        ? { ...m, texto: novoTexto, editada: true }
                        : m
                )
            );
        }
    };

    // Função responsável por excluir uma mensagem
    const excluirMensagem = async (msg) => {
        const resposta = await fetch(`${API_URL}/mensagens/${msg.id_mensagem}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                usuario: usuarioLogado
            })
        });

        if (resposta.ok) {
            setHistorico((prev) =>
                prev.filter((m) => m.id_mensagem !== msg.id_mensagem)
            );
        }
    };

    // A Interface da Tela
    return (
        <>
            <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>

                {/* BARRA LATERAL */}
                <div style={{ width: '300px', borderRight: '1px solid #ccc', backgroundColor: '#f9f9f9', display: 'flex', flexDirection: 'column' }}>
                    <div style={{ padding: '20px', borderBottom: '1px solid #ddd', backgroundColor: '#e2e2e2' }}>
                        <strong>Logado como:</strong> <br />
                        <span>{usuarioLogado}</span>

                        <button
                            data-cy="btn-configuracoes"
                            onClick={() => setPerfilAberto(true)}
                            style={{
                                marginTop: '12px',
                                width: '100%',
                                padding: '10px',
                                borderRadius: '20px',
                                border: 'none',
                                backgroundColor: '#0E49B5',
                                color: '#fff',
                                fontWeight: 'bold',
                                cursor: 'pointer'
                            }}
                        >
                            ⚙️ Configurações
                        </button>
                    </div>

                    <h3 style={{ padding: '10px 20px', margin: 0 }}>Contatos</h3>
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0, overflowY: 'auto', flex: 1 }}>
                        {contatos.map((contato, index) => (
                            <li
                                key={index}
                                onClick={() => setContatoAtivo(contato)}
                                style={{
                                    padding: '15px 20px',
                                    cursor: 'pointer',
                                    backgroundColor: contatoAtivo?.usuario === contato.usuario ? '#d1ecf1' : 'transparent',
                                    borderBottom: '1px solid #eee',
                                    transition: 'background-color 0.2s'
                                }}
                            >
                                <strong>{contato.nome || contato.usuario || contato.email}</strong> <br />
                                <small style={{ color: '#666' }}>@{contato.usuario || contato.email}</small>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* ÁREA DE MENSAGENS */}
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                    {contatoAtivo ? (
                        <>
                            <div style={{ padding: '20px', borderBottom: '1px solid #ccc', backgroundColor: '#fff' }}>
                                <h2>Conversando com: {contatoAtivo.nome || contatoAtivo.usuario || contatoAtivo.email}</h2>
                            </div>

                            <div style={{ flex: 1, padding: '20px', overflowY: 'auto', backgroundColor: '#ece5dd' }}>
                                {historico.map((msg, index) => (
                                    <MensagemItem
                                        key={msg.id_mensagem || index}
                                        msg={msg}
                                        usuarioLogado={usuarioLogado}
                                        onEditar={() => editarMensagem(msg)}
                                        onExcluir={() => excluirMensagem(msg)}
                                    />
                                ))}
                                <div ref={fimDoChatRef} />
                            </div>

                            <div style={{ padding: '20px', backgroundColor: '#f0f0f0', display: 'flex' }}>
                                <input
                                    type="text"
                                    value={mensagem}
                                    onChange={(e) => setMensagem(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && enviarMensagem()}
                                    placeholder="Escreva uma mensagem..."
                                    style={{ flex: 1, padding: '15px', borderRadius: '8px', border: '1px solid #ccc', marginRight: '10px', outline: 'none' }}
                                />
                                <button
                                    onClick={enviarMensagem}
                                    style={{ padding: '0 25px', borderRadius: '8px', border: 'none', backgroundColor: '#007bff', color: '#fff', cursor: 'pointer', fontWeight: 'bold' }}
                                >
                                    Enviar
                                </button>
                            </div>
                        </>
                    ) : (
                        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f4f4f4' }}>
                            <h2 style={{ color: '#888' }}>Clique em um contato na barra lateral para iniciar</h2>
                        </div>
                    )}
                </div>

            </div>

            {perfilAberto && (
                <div style={{
                    position: 'fixed',
                    inset: 0,
                    backgroundColor: 'rgba(6, 6, 93, 0.35)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 9999
                }}>
                    <Perfil onClose={() => setPerfilAberto(false)} />
                </div>
            )}
        </>
    );
}