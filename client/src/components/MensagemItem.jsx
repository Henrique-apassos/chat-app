function detalhesStatus(status) {
  if (status === 'Lida') {
    return { checks: '\u2713\u2713', cor: '#0b84ff' };
  }

  if (status === 'Entregue') {
    return { checks: '\u2713\u2713', cor: '#777' };
  }

  if (status === 'Enviada') {
    return { checks: '\u2713', cor: '#777' };
  }

  return { checks: '', cor: '#888' };
}

export default function MensagemItem({ msg, usuarioLogado, onEditar, onExcluir }) {
  const minhaMensagem = msg.remetente === usuarioLogado;
  const status = msg.status || 'Enviada';
  const statusInfo = detalhesStatus(status);
  const podeAlterar = minhaMensagem && Number.isInteger(msg.id_mensagem);

  return (
    <div
      data-cy="mensagem-chat"
      style={{
        marginBottom: '10px',
        textAlign: minhaMensagem ? 'right' : 'left'
      }}
    >
      <span
        style={{
          display: 'inline-block',
          maxWidth: 'min(78%, 560px)',
          padding: '10px 15px',
          borderRadius: '8px',
          backgroundColor: minhaMensagem ? '#dcf8c6' : '#fff',
          boxShadow: '0 1px 1px rgba(0,0,0,0.1)',
          overflowWrap: 'anywhere'
        }}
      >
        <strong>{minhaMensagem ? 'Você: ' : `${msg.remetente}: `}</strong>
        {msg.texto}
        {msg.editada && ' (editada)'}

        {minhaMensagem && (
          <small
            data-cy="status-mensagem"
            style={{
              display: 'flex',
              justifyContent: 'flex-end',
              alignItems: 'center',
              gap: '6px',
              color: statusInfo.cor,
              marginTop: '5px'
            }}
          >
            {statusInfo.checks && (
              <span
                aria-label={`checks-${status.toLowerCase()}`}
                style={{ fontWeight: 700, letterSpacing: 0 }}
              >
                {statusInfo.checks}
              </span>
            )}
            <span>{status}</span>
          </small>
        )}
      </span>

      {podeAlterar && (
        <div style={{
          marginTop: '6px',
          display: 'flex',
          justifyContent: 'flex-end',
          alignItems: 'center',
          gap: '6px',
          fontSize: '0.85em',
          fontWeight: 'bold'
        }}>
          <button
            data-cy="btn-editar-mensagem"
            onClick={() => onEditar(msg)}
            style={{
              border: 'none',
              background: 'transparent',
              color: '#007bff',
              cursor: 'pointer',
              padding: 0
            }}
          >
            Editar
          </button>

          <span style={{ color: '#aaa', fontWeight: 'normal' }}>|</span>

          <button
            data-cy="btn-excluir-mensagem"
            onClick={() => onExcluir(msg)}
            style={{
              border: 'none',
              background: 'transparent',
              color: '#dc3545',
              cursor: 'pointer',
              padding: 0
            }}
          >
            Excluir
          </button>
        </div>
      )}
    </div>
  );
}
