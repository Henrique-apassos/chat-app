import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { API_URL, WS_URL } from "../services/api";

const STATUS_LABELS = {
    ENVIANDO: "Enviando",
    ENVIADO: "Enviada",
    ENTREGUE: "Entregue",
    LIDO: "Lida",
    PENDENTE: "Aguardando conexão",
    FALHA: "Falha ao enviar"
};

function statusParaLabel(status) {
    return STATUS_LABELS[status] || status || STATUS_LABELS.ENVIADO;
}

function statusParaCodigo(status) {
    if (status === STATUS_LABELS.PENDENTE) return "PENDENTE";
    if (status === STATUS_LABELS.ENVIANDO) return "ENVIANDO";
    if (status === STATUS_LABELS.ENVIADO) return "ENVIADO";
    if (status === STATUS_LABELS.ENTREGUE) return "ENTREGUE";
    if (status === STATUS_LABELS.LIDO) return "LIDO";
    return status || "ENVIADO";
}

function formatarVistoPorUltimo(lastSeen) {
    if (!lastSeen) return "Visto por último indisponível";

    const data = new Date(lastSeen);
    if (Number.isNaN(data.getTime())) {
        return `Visto por último ${lastSeen}`;
    }

    return `Visto por último ${data.toLocaleString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    })}`;
}

function criarClientId() {
    return `local-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export function useChatMotor(usuarioLogado, contatoAtivo) {
    const [historico, setHistorico] = useState([]);
    const [isOnline, setIsOnline] = useState(() => navigator.onLine);
    const [presencas, setPresencas] = useState({});
    const [erroEnvio, setErroEnvio] = useState("");
    const [socketVersion, setSocketVersion] = useState(0);

    const ws = useRef(null);
    const contatoAtivoRef = useRef(contatoAtivo);

    const contatoId = useCallback((contato) => {
        return contato?.usuario || contato?.email || "";
    }, []);

    const contatoSelecionadoId = contatoId(contatoAtivo);

    useEffect(() => {
        contatoAtivoRef.current = contatoAtivo;
    }, [contatoAtivo]);

    const enviarPacote = useCallback((pacote) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify(pacote));
            return true;
        }
        return false;
    }, []);

    const marcarConversaComoLida = useCallback(async (contatoDaConversa) => {
        if (!usuarioLogado || !contatoDaConversa) return;

        try {
            const resposta = await fetch(
                `${API_URL}/mensagens/${usuarioLogado}/${contatoDaConversa}/lidas`,
                { method: "POST" }
            );

            if (!resposta.ok) return;

            const dados = await resposta.json();
            if (dados.ids_mensagens?.length) {
                enviarPacote({
                    type: "read",
                    conversa_com: contatoDaConversa,
                    ids_mensagens: dados.ids_mensagens
                });
            }
        } catch (erro) {
            console.error("Erro ao marcar mensagens como lidas:", erro);
        }
    }, [enviarPacote, usuarioLogado]);

    const reenviarPendentes = useCallback(() => {
        setHistorico((historicoAtual) => {
            historicoAtual
                .filter((msg) => statusParaCodigo(msg.status) === "PENDENTE")
                .forEach((msg) => {
                    enviarPacote({
                        type: "message",
                        para: msg.para,
                        texto: msg.texto,
                        client_id: msg.client_id
                    });
                });

            return historicoAtual;
        });
    }, [enviarPacote]);

    useEffect(() => {
        if (!usuarioLogado) return;

        const socket = new WebSocket(`${WS_URL}/ws/${usuarioLogado}`);
        ws.current = socket;

        socket.onopen = () => {
            setErroEnvio("");
            reenviarPendentes();
        };

        socket.onmessage = (event) => {
            try {
                const pacote = JSON.parse(event.data);
                const tipo = pacote.type || (pacote.texto ? "message" : "");

                if (tipo === "presence_update") {
                    setPresencas((prev) => ({
                        ...prev,
                        [pacote.usuario]: pacote
                    }));
                    return;
                }

                if (tipo === "status_update") {
                    const ids = pacote.ids_mensagens || [pacote.id_mensagem];
                    setHistorico((prev) =>
                        prev.map((msg) =>
                            ids.includes(msg.id_mensagem)
                                ? { ...msg, status: statusParaLabel(pacote.status) }
                                : msg
                        )
                    );
                    return;
                }

                if (tipo !== "message" || !pacote.texto) return;

                const contatoAtualId = contatoId(contatoAtivoRef.current);
                const status = statusParaLabel(pacote.status);
                const pertenceAoChatAtual =
                    pacote.remetente === contatoAtualId ||
                    pacote.para === contatoAtualId;

                if (!pertenceAoChatAtual) return;

                const mensagemRecebida = {
                    id_mensagem: pacote.id_mensagem,
                    client_id: pacote.client_id,
                    texto: pacote.texto,
                    remetente: pacote.remetente,
                    para: pacote.para,
                    status,
                    timestamp: pacote.timestamp,
                    editada: pacote.editada || false
                };

                setHistorico((prev) => {
                    const indicePorClientId = pacote.client_id
                        ? prev.findIndex((msg) => msg.client_id === pacote.client_id)
                        : -1;
                    const indicePorId = pacote.id_mensagem
                        ? prev.findIndex((msg) => msg.id_mensagem === pacote.id_mensagem)
                        : -1;
                    const indice = indicePorClientId >= 0 ? indicePorClientId : indicePorId;

                    if (indice >= 0) {
                        return prev.map((msg, index) =>
                            index === indice ? { ...msg, ...mensagemRecebida } : msg
                        );
                    }

                    return [...prev, mensagemRecebida];
                });

                if (pacote.remetente === contatoAtualId && pacote.remetente !== usuarioLogado) {
                    marcarConversaComoLida(contatoAtualId);
                }
            } catch (erro) {
                console.error("Erro ao ler mensagem do websocket:", erro);
            }
        };

        socket.onclose = () => {
            if (ws.current === socket) {
                ws.current = null;
            }
        };

        return () => {
            socket.close();
            if (ws.current === socket) {
                ws.current = null;
            }
        };
    }, [contatoId, marcarConversaComoLida, reenviarPendentes, socketVersion, usuarioLogado]);

    useEffect(() => {
        const carregarHistorico = async () => {
            if (!contatoAtivo || !usuarioLogado) {
                setHistorico([]);
                return;
            }

            try {
                setHistorico([]);

                const destinatario = contatoId(contatoAtivo);
                if (!destinatario) return;

                const resposta = await fetch(`${API_URL}/mensagens/${usuarioLogado}/${destinatario}`);

                if (resposta.ok) {
                    const mensagensAntigas = await resposta.json();

                    const historicoFormatado = mensagensAntigas.map((msg) => ({
                        id_mensagem: msg.id_mensagem,
                        texto: msg.texto,
                        remetente: msg.remetente,
                        para: msg.para,
                        status: statusParaLabel(msg.status),
                        timestamp: msg.timestamp,
                        editada: msg.editada || false
                    }));

                    setHistorico(historicoFormatado);
                    marcarConversaComoLida(destinatario);
                }
            } catch (erro) {
                console.error("Erro ao carregar o histórico:", erro);
            }
        };

        carregarHistorico();
    }, [contatoAtivo, contatoId, marcarConversaComoLida, usuarioLogado]);

    useEffect(() => {
        const carregarPresenca = async () => {
            if (!contatoSelecionadoId) return;

            try {
                const resposta = await fetch(`${API_URL}/presenca/${contatoSelecionadoId}`);
                if (!resposta.ok) return;

                const dados = await resposta.json();
                setPresencas((prev) => ({
                    ...prev,
                    [contatoSelecionadoId]: dados
                }));
            } catch (erro) {
                console.error("Erro ao buscar presença:", erro);
            }
        };

        carregarPresenca();
    }, [contatoSelecionadoId]);

    useEffect(() => {
        const handleOffline = () => {
            setIsOnline(false);
            setErroEnvio("Envio falhou por falta de conexão. A mensagem ficará aguardando conexão.");
        };

        const handleOnline = () => {
            setIsOnline(true);
            setErroEnvio("");

            if (!ws.current || ws.current.readyState === WebSocket.CLOSED) {
                setSocketVersion((versao) => versao + 1);
                return;
            }

            reenviarPendentes();
        };

        window.addEventListener("offline", handleOffline);
        window.addEventListener("online", handleOnline);

        return () => {
            window.removeEventListener("offline", handleOffline);
            window.removeEventListener("online", handleOnline);
        };
    }, [reenviarPendentes]);

    const enviarMensagem = useCallback((textoMensagem) => {
        const texto = textoMensagem.trim();
        const destinatario = contatoId(contatoAtivo);
        if (!texto || !destinatario) return;

        const clientId = criarClientId();
        const pacote = {
            type: "message",
            para: destinatario,
            texto,
            client_id: clientId
        };

        const mensagemLocal = {
            id_mensagem: clientId,
            client_id: clientId,
            texto,
            remetente: usuarioLogado,
            para: destinatario,
            status: isOnline ? STATUS_LABELS.ENVIANDO : STATUS_LABELS.PENDENTE
        };

        setHistorico((prev) => [...prev, mensagemLocal]);

        if (!isOnline || !enviarPacote(pacote)) {
            setHistorico((prev) =>
                prev.map((msg) =>
                    msg.client_id === clientId
                        ? { ...msg, status: STATUS_LABELS.PENDENTE }
                        : msg
                )
            );
            setErroEnvio("Envio falhou por falta de conexão. A mensagem ficará aguardando conexão.");
        }
    }, [contatoAtivo, contatoId, enviarPacote, isOnline, usuarioLogado]);

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
                prev.map((mensagem) =>
                    mensagem.id_mensagem === msg.id_mensagem
                        ? { ...mensagem, texto: novoTexto, editada: true }
                        : mensagem
                )
            );
        }
    };

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
                prev.filter((mensagem) => mensagem.id_mensagem !== msg.id_mensagem)
            );
        }
    };

    const presencaContato = useMemo(() => {
        const dados = presencas[contatoSelecionadoId];
        if (!contatoSelecionadoId) {
            return { online: false, texto: "" };
        }

        if (dados?.online) {
            return { ...dados, texto: "Online" };
        }

        return {
            ...dados,
            online: false,
            texto: formatarVistoPorUltimo(dados?.last_seen)
        };
    }, [contatoSelecionadoId, presencas]);

    return {
        historico,
        isOnline,
        erroEnvio,
        presencas,
        presencaContato,
        enviarMensagem,
        editarMensagem,
        excluirMensagem
    };
}
