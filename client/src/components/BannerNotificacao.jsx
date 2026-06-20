export default function BannerNotificacao({ bannerAtivo, onFechar }) {
  if (!bannerAtivo) return null;

  return (
    <div
      data-cy="banner-notificacao"
      style={{
        position: 'fixed',
        top: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        backgroundColor: '#007bff',
        color: '#fff',
        padding: '15px 25px',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        zIndex: 9999,
        maxWidth: '400px',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <strong>{bannerAtivo.remetente}:</strong> {bannerAtivo.texto}
        </div>
        <button
          onClick={onFechar}
          style={{
            background: 'transparent',
            border: 'none',
            color: '#fff',
            fontSize: '1.2rem',
            cursor: 'pointer',
            marginLeft: '15px',
          }}
        >
          ×
        </button>
      </div>
    </div>
  );
}