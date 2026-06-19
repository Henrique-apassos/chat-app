import { useState } from 'react';

export function ChatInput({ onEnviar, isMobile }) {
    // O estado da mensagem agora vive apenas aqui dentro
    const [mensagem, setMensagem] = useState('');

    const handleEnviar = () => {
        if (!mensagem.trim()) return;

        // Dispara a função do pai (o Hook useChatMotor) passando o texto
        onEnviar(mensagem);

        // Limpa o campo após o envio (fazendo o cenário do Cypress passar)
        setMensagem('');
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleEnviar();
        }
    };

    return (
        <div style={{
            padding: isMobile ? '10px' : '20px',
            backgroundColor: '#f0f0f0',
            display: 'flex',
            boxSizing: 'border-box',
            width: '100%'
        }}>
            <input
                data-cy="input-mensagem"
                type="text"
                value={mensagem}
                onChange={(e) => setMensagem(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Escreva uma mensagem..."
                style={{
                    flex: 1,
                    padding: isMobile ? '12px' : '15px',
                    borderRadius: '8px',
                    border: '1px solid #ccc',
                    marginRight: isMobile ? '8px' : '10px',
                    outline: 'none',
                    boxSizing: 'border-box',
                    minWidth: 0
                }}
            />
            <button
                data-cy="btn-enviar"
                disabled={!mensagem.trim()} // Bloqueia o clique se estiver vazio
                onClick={handleEnviar}
                style={{
                    padding: isMobile ? '0 15px' : '0 25px',
                    borderRadius: '8px',
                    border: 'none',
                    backgroundColor: '#007bff',
                    color: '#fff',
                    fontWeight: 'bold',
                    // Feedback visual extra para quando está desabilitado
                    cursor: !mensagem.trim() ? 'not-allowed' : 'pointer',
                    opacity: !mensagem.trim() ? 0.6 : 1, 
                    boxSizing: 'border-box',
                    whiteSpace: 'nowrap'

                }}
            >
                Enviar
            </button>
        </div>
    );
}
