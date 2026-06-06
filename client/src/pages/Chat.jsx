import React, { useState, useEffect, useRef } from 'react';
import api from "../services/api";

export default function Chat() {
    // Quem sou eu? (Pega o usuário salvo no localStorage durante o Login)
    const [usuarioLogado] = useState(localStorage.getItem('usuario') || 'usuario_teste');

    // Estados da Interface
    const [contatos, setContatos] = useState([]);           // Lista da barra lateral
    const [contatoAtivo, setContatoAtivo] = useState(null); // Com quem estou falando
    const [mensagem, setMensagem] = useState('');           // O texto do input
    const [historico, setHistorico] = useState([]);         // As mensagens na tela

    const ws = useRef(null);
    const fimDoChatRef = useRef(null);

    // Efeito para buscar a lista de contatos do backend
    useEffect(() => {
        const buscarContatos = async () => {
            try {
                // Faz a requisição para o seu FastAPI usando a configuração do api.js
                const resposta = await api.get('/usuarios');
                setContatos(resposta.data);
            } catch (error) {
                console.error("Erro ao carregar os contatos reais:", error);

                // Mock de teste (Plano B) para a tela não quebrar se a rota ainda não existir no backend
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

        // Conecta no backend enviando o nome do usuário na URL
        ws.current = new WebSocket(`ws://127.0.0.1:8000/ws/${usuarioLogado}`);

        ws.current.onopen = () => console.log("WebSocket Conectado como:", usuarioLogado);

        ws.current.onmessage = (event) => {
            // Quando recebe mensagem do servidor, adiciona à tela
            setHistorico((prev) => [...prev, event.data]);
        };

        // Limpa a conexão se o usuário fechar a aba ou sair da página
        return () => ws.current?.close();
    }, [usuarioLogado]);

    // Efeito para rolar o chat para o fim sempre que chegar mensagem nova
    useEffect(() => {
        fimDoChatRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [historico]);

    // Função para Enviar a Mensagem
    const enviarMensagem = () => {
        if (!mensagem.trim() || !contatoAtivo) return;

        // O pacote JSON no formato exato para mensagens diretas
        const pacote = {
            para: contatoAtivo.usuario,
            texto: mensagem
        };

        // Envia o pacote convertido para texto pelo WebSocket
        ws.current.send(JSON.stringify(pacote));

        // Adiciona a própria mensagem na tela imediatamente
        setHistorico((prev) => [...prev, `[Você]: ${mensagem}`]);
        setMensagem(''); // Limpa o input
    };
    // 7. A Interface da Tela
    return (
        <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>

            {/* BARRA LATERAL (Sidebar) */}
            <div style={{ width: '300px', borderRight: '1px solid #ccc', backgroundColor: '#f9f9f9', display: 'flex', flexDirection: 'column' }}>
                <div style={{ padding: '20px', borderBottom: '1px solid #ddd', backgroundColor: '#e2e2e2' }}>
                    <strong>Logado como:</strong> <br /> {usuarioLogado}
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
                            <strong>{contato.nome || contato.usuario}</strong> <br />
                            <small style={{ color: '#666' }}>@{contato.usuario}</small>
                        </li>
                    ))}
                </ul>
            </div>

            {/* ÁREA PRINCIPAL DO CHAT */}
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                {contatoAtivo ? (
                    <>
                        {/* Cabeçalho com o nome do contato */}
                        <div style={{ padding: '20px', borderBottom: '1px solid #ccc', backgroundColor: '#fff' }}>
                            <h2>Conversando com: {contatoAtivo.nome || contatoAtivo.usuario}</h2>
                        </div>

                        {/* Caixa de Mensagens */}
                        <div style={{ flex: 1, padding: '20px', overflowY: 'auto', backgroundColor: '#ece5dd' }}>
                            {historico.map((msg, index) => (
                                <div key={index} style={{ marginBottom: '10px', textAlign: msg.startsWith('[Você]') ? 'right' : 'left' }}>
                                    <span style={{
                                        display: 'inline-block',
                                        padding: '10px 15px',
                                        borderRadius: '8px',
                                        backgroundColor: msg.startsWith('[Você]') ? '#dcf8c6' : '#fff',
                                        boxShadow: '0 1px 1px rgba(0,0,0,0.1)'
                                    }}>
                                        {msg}
                                    </span>
                                </div>
                            ))}
                            <div ref={fimDoChatRef} />
                        </div>

                        {/* Input de Digitação e Botão de Envio */}
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
                    /* Tela de Espera quando não há contato selecionado */
                    <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f4f4f4' }}>
                        <h2 style={{ color: '#888' }}>Clique em um contato na barra lateral para iniciar</h2>
                    </div>
                )}
            </div>

        </div>
    );
}