export function ChatHeader({ contatoAtivo, isMobile, onVoltar, presencaContato }) {
    if (!contatoAtivo) return null;

    return (
        <div style={{
            padding: '16px 20px',
            borderBottom: '1px solid #ccc',
            backgroundColor: '#fff',
            display: 'flex',
            alignItems: 'center'
        }}>
            {isMobile && (
                <button
                    onClick={onVoltar}
                    style={{
                        marginRight: '15px',
                        padding: '8px 12px',
                        border: 'none',
                        borderRadius: '5px',
                        backgroundColor: '#e2e2e2',
                        cursor: 'pointer',
                        fontWeight: 'bold'
                    }}
                >
                    Voltar
                </button>
            )}

            <div style={{ minWidth: 0 }}>
                <h2 style={{ margin: 0, color: '#333', fontSize: '1.25rem' }}>
                    {contatoAtivo.nome || contatoAtivo.usuario || contatoAtivo.email}
                </h2>
                <small
                    data-cy="status-presenca-contato"
                    style={{
                        display: 'block',
                        color: presencaContato?.online ? '#16803c' : '#666',
                        marginTop: '3px',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis'
                    }}
                >
                    {presencaContato?.texto || 'Visto por último indisponível'}
                </small>
            </div>
        </div>
    );
}
