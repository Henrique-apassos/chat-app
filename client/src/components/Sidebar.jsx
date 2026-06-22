import BadgeNotificacao from './BadgeNotificacao';

function textoPresenca(presenca) {
    if (presenca?.online) return 'Online';
    if (presenca?.last_seen) return 'Visto por ultimo';
    return 'Offline';
}

export function Sidebar({
    usuarioLogado,
    contatos,
    contatoAtivo,
    presencas = {},
    badges = {},
    onSelectContato,
    onOpenPerfil,
    isMobile
}) {
    return (
        <div style={{
            width: isMobile ? '100%' : '300px',
            borderRight: isMobile ? 'none' : '1px solid #ccc',
            backgroundColor: '#f9f9f9',
            display: 'flex',
            flexDirection: 'column'
        }}>
            <div style={{ padding: '20px', borderBottom: '1px solid #ddd', backgroundColor: '#e2e2e2' }}>
                <strong>Logado como:</strong> <br />
                <span>{usuarioLogado}</span>
                <button
                    data-cy="btn-configuracoes"
                    onClick={onOpenPerfil}
                    style={{
                        marginTop: '12px',
                        width: '100%',
                        padding: '10px',
                        borderRadius: '8px',
                        border: 'none',
                        backgroundColor: '#0E49B5',
                        color: '#fff',
                        fontWeight: 'bold',
                        cursor: 'pointer'
                    }}
                >
                    Configuracoes
                </button>
            </div>
            <h3 style={{ padding: '10px 20px', margin: 0 }}>Contatos</h3>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, overflowY: 'auto', flex: 1 }}>
                {contatos.map((contato, index) => {
                    const idContato = contato.usuario || contato.email;
                    const presenca = presencas[idContato];
                    const ativo = contatoAtivo?.usuario === contato.usuario;
                    const badgeQuantidade = badges[idContato] || 0;
                    
                    return (
                        <li
                            key={idContato || index}
                            data-cy={`contato-${idContato}`}
                            onClick={() => onSelectContato(contato)}
                            style={{
                                padding: '15px 20px',
                                cursor: 'pointer',
                                backgroundColor: ativo ? '#d1ecf1' : 'transparent',
                                borderBottom: '1px solid #eee',
                                transition: 'background-color 0.2s'
                            }}
                        >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div style={{ flex: 1, minWidth: 0 }}>
                                    <strong>{contato.nome || contato.usuario || contato.email}</strong> <br />
                                    <small style={{ color: '#666' }}>@{idContato}</small>
                                    <small
                                        data-cy={`status-presenca-${idContato}`}
                                        style={{
                                            display: 'block',
                                            color: presenca?.online ? '#16803c' : '#777',
                                            marginTop: '3px'
                                        }}
                                    >
                                        {textoPresenca(presenca)}
                                    </small>
                                </div>
                                <BadgeNotificacao quantidade={badgeQuantidade} />
                            </div>
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}