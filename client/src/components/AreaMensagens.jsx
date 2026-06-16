import { useEffect, useRef } from 'react';
import MensagemItem from './MensagemItem';

export function AreaMensagens({ historico, usuarioLogado, onEditar, onExcluir }) {
    const fimDoChatRef = useRef(null);

    useEffect(() => {
        fimDoChatRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [historico]);

    return (
        <div style={{ flex: 1, padding: '20px', overflowY: 'auto', backgroundColor: '#ece5dd' }}>
            {historico.map((msg, index) => (
                <MensagemItem
                    key={msg.client_id || msg.id_mensagem || index}
                    msg={msg}
                    usuarioLogado={usuarioLogado}
                    onEditar={onEditar}
                    onExcluir={onExcluir}
                />
            ))}
            <div ref={fimDoChatRef} />
        </div>
    );
}
