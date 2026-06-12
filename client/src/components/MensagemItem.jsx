export default function MensagemItem({ msg, usuarioLogado, onEditar, onExcluir }) {
  const minhaMensagem = msg.remetente === usuarioLogado;

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
          padding: '10px 15px',
          borderRadius: '8px',
          backgroundColor: minhaMensagem ? '#dcf8c6' : '#fff',
          boxShadow: '0 1px 1px rgba(0,0,0,0.1)'
        }}
      >
        {minhaMensagem ? 'Você: ' : `${msg.remetente}: `}
        {msg.texto}
        {msg.editada && ' (editada)'}
        {minhaMensagem && <small style={{display: 'block', color: '#888'}}>Enviada</small>}
      </span>

      {minhaMensagem && (
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
              color: '#007bff', // Azul
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
              color: '#dc3545', // Vermelho
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