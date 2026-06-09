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
        {minhaMensagem ? '[Você]: ' : '[Recebido]: '}
        {msg.texto}
        {msg.editada && ' (editada)'}
      </span>

      {minhaMensagem && (
        <div style={{ marginTop: '4px' }}>
          <button
            data-cy="btn-editar-mensagem"
            onClick={() => onEditar(msg)}
          >
            Editar
          </button>

          <button
            data-cy="btn-excluir-mensagem"
            onClick={() => onExcluir(msg)}
          >
            Excluir
          </button>
        </div>
      )}
    </div>
  );
}