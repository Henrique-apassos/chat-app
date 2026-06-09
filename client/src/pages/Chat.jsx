import React, { useState, useEffect, useRef } from 'react';

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
                // Faz a requisição direta para a rota de usuários que criamos no FastAPI
                const resposta = await fetch('http://127.0.0.1:8000/auth/usuarios');

                if (resposta.ok) {
                    const dados = await resposta.json();
                    setContatos(dados);
                } else {
                    throw new Error("Rota não encontrada ou erro no servidor");
                }
            } catch (error) {
                console.error("Erro ao carregar os contatos reais:", error);

                // Mock de teste (Plano B) 
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
            let textoFinal = event.data; 

            try {
                const stringCorrigida = event.data.replace(/'/g, '"');

                
                const pacote = JSON.parse(stringCorrigida);

                if (typeof pacote === 'object' && pacote !== null) {
                    textoFinal = pacote.texto || pacote.mensagem || pacote.msg || pacote.content || stringCorrigida;
                }

            } catch (e) {
                const regex = /['"]?(?:texto|mensagem|msg|content)['"]?\s*:\s*['"](.*?)['"](?:}|$|,)/i;
                const match = event.data.match(regex);

                if (match && match[1]) {
                    textoFinal = match[1];
                }
            }

            setHistorico((prev) => [...prev, `[Recebido]: ${textoFinal}`]);
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
      // Se não houver contato selecionado, não faz nada
      if (!contatoAtivo) return;

      try {
        // Limpa a tela para não misturar mensagens de pessoas diferentes
        setHistorico([]);

        // O identificador do contato
        const destinatario = contatoAtivo.usuario;

        // Faz o pedido à nova rota do backend (que trará o histórico entre si e o contato)
        const resposta = await fetch(`http://127.0.0.1:8000/mensagens/${usuarioLogado}/${destinatario}`);

        if (resposta.ok) {
          const mensagensAntigas = await resposta.json();

          // Formata as mensagens vindas da base de dados
          const historicoFormatado = mensagensAntigas.map(msg => {
            if (msg.remetente === usuarioLogado) {
              return `[Você]: ${msg.texto}`;
            } 
            else {
              return `[Recebido]: ${msg.texto}`;
            }
          });
          setHistorico(historicoFormatado);
        }
      } catch (erro) {
        console.error("Erro ao carregar o histórico:", erro);
      }
    };

    carregarHistorico();
  }, [contatoAtivo, usuarioLogado]); // Este efeito dispara SEMPRE que o contatoAtivo mudar!

    // Função para Enviar a Mensagem
    const enviarMensagem = () => {
        if (!mensagem.trim() || !contatoAtivo) return;

        const pacote = {
            para: contatoAtivo.usuario || contatoAtivo.email, // Ajustado para aceitar email se for o caso
            texto: mensagem
        };

        ws.current.send(JSON.stringify(pacote));
        setHistorico((prev) => [...prev, `[Você]: ${mensagem}`]);
        setMensagem('');
    };

    // A Interface da Tela
    return (
        <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>

            {/* BARRA LATERAL */}
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
    );
}